#!/usr/bin/env python3
"""
CommandBrain - Smart Command Reference Tool
Search Linux commands by name, purpose, category, or related tools.

Usage:  cb ssh                  Search for SSH
        cb password cracking    Search by purpose/task
        cb -d grep              Detailed view
        cb -e nmap              Examples only
        cb --setup              Initialize database
        cb --setup --kali       Include Kali security tools
"""

import sqlite3
import os
import sys
import argparse
import platform
import difflib
import re
from typing import List, Tuple

# ─────────────────────────────────────────────────────────────────────────────
# COLOR SUPPORT - works on Bash, ZSH, Fish, and Windows Terminal
# ─────────────────────────────────────────────────────────────────────────────

def _supports_color():
    """Detect if the terminal supports ANSI colors."""
    # Respect NO_COLOR convention (https://no-color.org)
    if os.environ.get("NO_COLOR") is not None:
        return False
    # Not a TTY (piped output) = no color
    if not hasattr(sys.stdout, "isatty") or not sys.stdout.isatty():
        return False
    # Dumb terminals don't support color
    if os.environ.get("TERM") == "dumb":
        return False
    return True

# Enable ANSI on Windows 10+
if platform.system() == "Windows":
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        pass

_USE_COLOR = _supports_color()

class Colors:
    """ANSI color codes. Automatically disabled when terminal doesn't support them."""
    HEADER    = '\033[95m' if _USE_COLOR else ''
    BLUE      = '\033[94m' if _USE_COLOR else ''
    CYAN      = '\033[96m' if _USE_COLOR else ''
    GREEN     = '\033[92m' if _USE_COLOR else ''
    YELLOW    = '\033[93m' if _USE_COLOR else ''
    RED       = '\033[91m' if _USE_COLOR else ''
    BOLD      = '\033[1m'  if _USE_COLOR else ''
    UNDERLINE = '\033[4m'  if _USE_COLOR else ''
    END       = '\033[0m'  if _USE_COLOR else ''

C = Colors  # Short alias used throughout

# ─────────────────────────────────────────────────────────────────────────────
# DATABASE
# ─────────────────────────────────────────────────────────────────────────────

DB_PATH = os.path.expanduser("~/.commandbrain.db")

def _connect(must_exist=True):
    """Return a connection to the SQLite database."""
    if must_exist and not os.path.exists(DB_PATH):
        print(f"{C.RED}Database not found! Run:  cb --setup{C.END}")
        sys.exit(1)
    try:
        return sqlite3.connect(DB_PATH)
    except sqlite3.Error as e:
        print(f"{C.RED}Database error: {e}{C.END}")
        sys.exit(1)

# ─────────────────────────────────────────────────────────────────────────────
# SETUP  (replaces setup_commandbrain.py, add_kali_tools.py, enhance_slang_tags.py)
# ─────────────────────────────────────────────────────────────────────────────

def setup_database(include_kali=False):
    """Create DB, populate commands, and apply slang tags. All-in-one setup."""
    from data import (BASIC_COMMANDS, KALI_TOOLS, SLANG_MAPPINGS,
                        KALI_TOOLS_EXTENDED, SLANG_MAPPINGS_EXTENDED)

    conn = _connect(must_exist=False)
    cur = conn.cursor()

    # Create schema
    cur.execute("""
        CREATE TABLE IF NOT EXISTS commands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            usage TEXT,
            examples TEXT,
            related_commands TEXT,
            notes TEXT,
            tags TEXT
        )
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_name ON commands(name)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_category ON commands(category)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_tags ON commands(tags)")

    # Insert basic commands
    cur.executemany("""
        INSERT OR IGNORE INTO commands
        (name,category,description,usage,examples,related_commands,notes,tags)
        VALUES (?,?,?,?,?,?,?,?)
    """, BASIC_COMMANDS)
    basic_count = len(BASIC_COMMANDS)

    # Insert Kali tools (original + extended)
    kali_count = 0
    if include_kali:
        all_kali = KALI_TOOLS + KALI_TOOLS_EXTENDED
        cur.executemany("""
            INSERT OR IGNORE INTO commands
            (name,category,description,usage,examples,related_commands,notes,tags)
            VALUES (?,?,?,?,?,?,?,?)
        """, all_kali)
        kali_count = len(all_kali)

    # Apply slang / purpose-based search terms (original + extended)
    all_slang = {**SLANG_MAPPINGS, **SLANG_MAPPINGS_EXTENDED}
    enhanced = 0
    for cmd_name, slang_list in all_slang.items():
        cur.execute("SELECT tags FROM commands WHERE name = ?", (cmd_name,))
        row = cur.fetchone()
        if not row:
            continue
        current = row[0] or ""
        new_slang = ", ".join(slang_list)
        combined = f"{current}, {new_slang}" if current else new_slang
        cur.execute("UPDATE commands SET tags = ? WHERE name = ?", (combined, cmd_name))
        enhanced += 1

    conn.commit()
    conn.close()

    # Report
    print(f"\n{C.BOLD}CommandBrain Setup Complete!{C.END}\n")
    print(f"  Database:    {C.CYAN}{DB_PATH}{C.END}")
    print(f"  Commands:    {C.CYAN}{basic_count} basic Linux commands{C.END}")
    if include_kali:
        print(f"  Kali tools:  {C.CYAN}{kali_count} security tools{C.END}")
    print(f"  Search tags: {C.CYAN}{enhanced} commands enhanced with purpose-based search{C.END}")
    print(f"\n  Try it:  {C.GREEN}cb ssh{C.END}")
    print(f"           {C.GREEN}cb password cracking{C.END}")
    if not include_kali:
        print(f"\n  Want Kali tools?  {C.YELLOW}cb --setup --kali{C.END}")
    print()

# ─────────────────────────────────────────────────────────────────────────────
# SEARCH — Relevance-scored search with pagination and suggestions
# ─────────────────────────────────────────────────────────────────────────────

def _score_result(row, term):
    """Score how relevant a database row is to the search term.
    Higher score = more relevant. Used to rank results so students see
    the most useful commands first instead of wading through huge lists."""
    score = 0
    term_lower = term.lower().strip()
    words = [w for w in term_lower.split() if len(w) > 1]

    name        = (row[1] or "").lower()
    category    = (row[2] or "").lower().replace("-", " ").replace("_", " ")
    description = (row[3] or "").lower()
    tags        = (row[8] or "").lower() if len(row) > 8 else ""
    related     = (row[6] or "").lower() if len(row) > 6 else ""
    notes       = (row[7] or "").lower() if len(row) > 7 else ""

    # ── Name matching (highest priority) ──────────────────────────────
    if name == term_lower:
        score += 100                          # Exact name match
    elif term_lower in name:
        score += 60                           # Partial name match
    elif any(w == name for w in words):
        score += 55                           # A search word IS the command name

    # ── Category matching ─────────────────────────────────────────────
    if term_lower == category:
        score += 45                           # Exact category match
    elif term_lower in category or category in term_lower:
        score += 30                           # Partial category match
    elif any(w in category for w in words):
        score += 20                           # Word in category

    # ── Core tags (first ~120 chars = original purpose tags) ──────────
    core_tags = tags[:120]
    extended_tags = tags[120:]

    if term_lower in core_tags:
        score += 35                           # Full phrase in core tags
    elif any(w in core_tags for w in words if len(w) > 2):
        score += 25                           # Word in core tags

    # ── Description matching ──────────────────────────────────────────
    if term_lower in description:
        score += 20
        # Bonus if term appears early (more likely the primary purpose)
        pos = description.find(term_lower)
        if pos < 40:
            score += 10
    elif any(w in description for w in words if len(w) > 2):
        score += 10

    # ── Extended tags (slang/purpose mappings) ────────────────────────
    if extended_tags:
        if term_lower in extended_tags:
            score += 12
        elif any(w in extended_tags for w in words if len(w) > 2):
            score += 6

    # ── Notes matching ────────────────────────────────────────────────
    if term_lower in notes:
        score += 8
    elif any(w in notes for w in words if len(w) > 2):
        score += 4

    # ── Related commands ──────────────────────────────────────────────
    if term_lower in related:
        score += 5

    return score


def search_commands(term: str, mode: str = "all", page: int = 1,
                    per_page: int = 10) -> tuple:
    """Search commands with relevance scoring and pagination.

    Returns: (page_results, total_count, suggestions)
      - page_results: list of DB rows for the current page
      - total_count: total number of matching results
      - suggestions: list of related search term strings
    """
    conn = _connect()
    cur = conn.cursor()
    p = f"%{term}%"

    if mode == "name":
        cur.execute("SELECT * FROM commands WHERE name LIKE ?", (p,))
        all_results = cur.fetchall()
    elif mode == "category":
        cur.execute("SELECT * FROM commands WHERE category LIKE ?", (p,))
        all_results = cur.fetchall()
    elif mode == "tags":
        cur.execute("SELECT * FROM commands WHERE tags LIKE ?", (p,))
        all_results = cur.fetchall()
    elif mode == "description":
        cur.execute("SELECT * FROM commands WHERE description LIKE ? OR notes LIKE ?", (p, p))
        all_results = cur.fetchall()
    else:
        # Search all fields for the full phrase
        cur.execute("""
            SELECT * FROM commands
            WHERE name LIKE ? OR description LIKE ? OR tags LIKE ?
               OR related_commands LIKE ? OR category LIKE ? OR notes LIKE ?
        """, (p, p, p, p, p, p))
        all_results = list(cur.fetchall())
        seen_ids = {r[0] for r in all_results}

        # For multi-word searches, also find results matching individual words
        # (catches results that match some but not all words)
        words = [w for w in term.split() if len(w) > 1]
        if len(words) > 1:
            for word in words:
                wp = f"%{word}%"
                cur.execute("""
                    SELECT * FROM commands
                    WHERE name LIKE ? OR description LIKE ? OR tags LIKE ?
                       OR category LIKE ?
                """, (wp, wp, wp, wp))
                for r in cur.fetchall():
                    if r[0] not in seen_ids:
                        all_results.append(r)
                        seen_ids.add(r[0])

    conn.close()

    # Score and sort by relevance
    scored = [(row, _score_result(row, term)) for row in all_results]
    scored.sort(key=lambda x: (-x[1], x[0][1]))  # Score desc, then name asc

    total = len(scored)

    # Paginate
    start = (page - 1) * per_page
    end = start + per_page
    page_results = [row for row, score in scored[start:end]]

    # Get search suggestions
    suggestions = _get_search_suggestions(term, all_results)

    return page_results, total, suggestions


def _get_search_suggestions(term, all_results):
    """Generate related search suggestions for the bottom of results.
    Checks the SEARCH_TAXONOMY first for curated suggestions, then falls back
    to dynamically generating suggestions from result categories and tags."""
    try:
        from data import SEARCH_TAXONOMY
    except ImportError:
        SEARCH_TAXONOMY = {}

    term_lower = term.lower().strip()
    suggestions = []

    # 1. Check taxonomy for exact match (term or alias)
    for key, entry in SEARCH_TAXONOMY.items():
        aliases = [a.lower() for a in entry.get("aliases", [])]
        if term_lower == key.lower() or term_lower in aliases:
            suggestions = list(entry.get("related_searches", []))
            break

    # 2. If no exact match, check for partial/fuzzy taxonomy matches
    if not suggestions:
        partial = []
        for key, entry in SEARCH_TAXONOMY.items():
            aliases = [a.lower() for a in entry.get("aliases", [])]
            all_terms = [key.lower()] + aliases
            if any(term_lower in t or t in term_lower for t in all_terms):
                for s in entry.get("related_searches", []):
                    if s.lower() != term_lower and s not in partial:
                        partial.append(s)
                if len(partial) >= 8:
                    break
        suggestions = partial

    # 3. If still nothing, generate from result categories/tags dynamically
    if not suggestions and all_results:
        cats = set()
        tag_words = set()
        for r in all_results[:20]:
            cat = (r[2] or "").replace("-", " ").replace("_", " ").lower()
            if cat and cat != term_lower:
                cats.add(cat)
            raw_tags = (r[8] or "").split(",") if len(r) > 8 else []
            for t in raw_tags[:5]:
                word = t.strip().lower()
                if word and word != term_lower and len(word) > 3:
                    tag_words.add(word)
        suggestions = list(cats)[:4] + list(tag_words - cats)[:4]

    # Deduplicate and remove the search term itself
    seen = set()
    clean = []
    for s in suggestions:
        sl = s.lower()
        if sl != term_lower and sl not in seen:
            seen.add(sl)
            clean.append(s)

    return clean[:8]


def _suggest(term: str, limit: int = 5) -> List[str]:
    """Fuzzy-match against all command names."""
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT name FROM commands ORDER BY name")
    names = [r[0] for r in cur.fetchall()]
    conn.close()
    return difflib.get_close_matches(term, names, n=limit, cutoff=0.6)

# ─────────────────────────────────────────────────────────────────────────────
# DISPLAY HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _print_no_results(term: str):
    """Shared 'no results + did you mean?' block used by every display mode."""
    print(f"{C.YELLOW}No commands found for '{term}'.{C.END}")
    if not term:
        return
    # Show fuzzy name suggestions
    suggestions = _suggest(term)
    if suggestions:
        print(f"\n{C.CYAN}Did you mean:{C.END}")
        conn = _connect()
        cur = conn.cursor()
        for cmd in suggestions:
            cur.execute("SELECT description FROM commands WHERE name = ?", (cmd,))
            row = cur.fetchone()
            if row:
                desc = row[0][:57] + "..." if len(row[0]) > 60 else row[0]
                print(f"  {C.GREEN}{cmd}{C.END} - {desc}")
        conn.close()
        print(f"\n{C.BOLD}Try:{C.END} cb {suggestions[0]}")
    # Also show taxonomy-based suggestions even when no results
    tax_suggestions = _get_search_suggestions(term, [])
    if tax_suggestions:
        print(f"\n{C.CYAN}Related searches:{C.END} {', '.join(tax_suggestions)}")


def _print_search_footer(total, page, per_page, suggestions, term):
    """Print pagination info and 'Also try' related search suggestions."""
    total_pages = max(1, (total + per_page - 1) // per_page)

    # Pagination info
    start = (page - 1) * per_page + 1
    end = min(page * per_page, total)
    if total > per_page:
        print(f"{C.BOLD}Showing {start}-{end} of {total} results{C.END}", end="")
        if page < total_pages:
            print(f"  {C.CYAN}(next: cb {term} --page {page + 1}){C.END}")
        else:
            print()
    elif total > 0:
        print(f"{C.BOLD}{total} result(s){C.END}")

    # Related search suggestions
    if suggestions:
        suggestion_strs = [f"{C.GREEN}{s}{C.END}" for s in suggestions]
        print(f"\n{C.CYAN}Also try:{C.END} {', '.join(suggestion_strs)}")
    print()


def display_short(results: List[Tuple], term: str = "", total: int = 0,
                  page: int = 1, per_page: int = 10, suggestions=None):
    """List view: name, category, one-liner."""
    if not results:
        return _print_no_results(term)
    print(f"\n{C.BOLD}Found {total} command(s):{C.END}\n")
    for r in results:
        print(f"{C.CYAN}{C.BOLD}{r[1]}{C.END} {C.YELLOW}[{r[2]}]{C.END}")
        print(f"  {r[3]}\n")
    _print_search_footer(total, page, per_page, suggestions or [], term)


def display_detailed(results: List[Tuple], term: str = "", total: int = 0,
                     page: int = 1, per_page: int = 10, suggestions=None):
    """Full info: description, usage, examples, notes, tags."""
    if not results:
        return _print_no_results(term)
    print(f"\n{C.BOLD}Found {total} command(s):{C.END}\n")
    for i, r in enumerate(results, 1):
        if i > 1:
            print(f"\n{C.BLUE}{'─' * 70}{C.END}\n")
        name, cat, desc, usage, examples, related, notes, tags = r[1:9]
        print(f"{C.CYAN}{C.BOLD}{name}{C.END} {C.YELLOW}[{cat}]{C.END}")
        print(f"{C.BOLD}Description:{C.END} {desc}")
        if usage:
            print(f"\n{C.BOLD}Usage:{C.END}\n  {usage}")
        if examples:
            print(f"\n{C.BOLD}Examples:{C.END}")
            for ex in examples.split('\n'):
                print(f"  {C.GREEN}${C.END} {ex}")
        if related:
            print(f"\n{C.BOLD}Related:{C.END} {C.CYAN}{related}{C.END}")
        if notes:
            print(f"\n{C.BOLD}Notes:{C.END}\n  {notes}")
        if tags:
            print(f"\n{C.BOLD}Tags:{C.END} {tags}")
    print()
    _print_search_footer(total, page, per_page, suggestions or [], term)


def display_examples(results: List[Tuple], term: str = "", total: int = 0,
                     page: int = 1, per_page: int = 10, suggestions=None):
    """Quick-reference: just name + examples."""
    if not results:
        return _print_no_results(term)
    print(f"\n{C.BOLD}Examples for {total} command(s):{C.END}\n")
    for i, r in enumerate(results, 1):
        if i > 1:
            print(f"{C.BLUE}{'─' * 50}{C.END}\n")
        print(f"{C.CYAN}{C.BOLD}{r[1]}{C.END}")
        if r[4]:
            print(f"  {C.BOLD}Usage:{C.END} {r[4]}")
        if r[5]:
            for ex in r[5].split('\n'):
                if ex.strip():
                    print(f"  {C.GREEN}${C.END} {ex}")
        else:
            print(f"  {C.YELLOW}(No examples available){C.END}")
        print()
    _print_search_footer(total, page, per_page, suggestions or [], term)

# ─────────────────────────────────────────────────────────────────────────────
# CATEGORIES & STATS
# ─────────────────────────────────────────────────────────────────────────────

def list_categories():
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT category FROM commands ORDER BY category")
    cats = cur.fetchall()
    print(f"\n{C.BOLD}Available Categories:{C.END}\n")
    for (cat,) in cats:
        cur.execute("SELECT COUNT(*) FROM commands WHERE category = ?", (cat,))
        print(f"  {C.CYAN}{cat}{C.END} ({cur.fetchone()[0]} commands)")
    conn.close()
    print()


def show_stats():
    conn = _connect()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM commands")
    total = cur.fetchone()[0]
    cur.execute("SELECT COUNT(DISTINCT name) FROM commands")
    unique = cur.fetchone()[0]
    cur.execute("SELECT COUNT(DISTINCT category) FROM commands")
    cats = cur.fetchone()[0]

    # Top categories
    cur.execute("""SELECT category, COUNT(*) as cnt FROM commands
                   GROUP BY category ORDER BY cnt DESC LIMIT 10""")
    top_cats = cur.fetchall()

    # DB file size
    db_size = "N/A"
    if os.path.exists(DB_PATH):
        size_bytes = os.path.getsize(DB_PATH)
        if size_bytes < 1024:
            db_size = f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            db_size = f"{size_bytes / 1024:.1f} KB"
        else:
            db_size = f"{size_bytes / (1024 * 1024):.1f} MB"

    # Commands with examples vs without
    cur.execute("SELECT COUNT(*) FROM commands WHERE examples IS NOT NULL AND examples != ''")
    with_examples = cur.fetchone()[0]

    conn.close()

    print(f"\n{C.CYAN}{'═' * 50}{C.END}")
    print(f"{C.CYAN}  COMMANDBRAIN STATISTICS{C.END}")
    print(f"{C.CYAN}{'═' * 50}{C.END}\n")
    print(f"  {C.BOLD}Total entries:{C.END}   {C.CYAN}{total}{C.END}")
    print(f"  {C.BOLD}Unique tools:{C.END}    {C.CYAN}{unique}{C.END}")
    print(f"  {C.BOLD}Categories:{C.END}      {C.CYAN}{cats}{C.END}")
    print(f"  {C.BOLD}With examples:{C.END}   {C.CYAN}{with_examples}{C.END} / {total}")
    print(f"  {C.BOLD}Database:{C.END}        {C.CYAN}{DB_PATH}{C.END}")
    print(f"  {C.BOLD}Database size:{C.END}   {C.CYAN}{db_size}{C.END}")

    print(f"\n  {C.BOLD}Top Categories:{C.END}")
    for cat, cnt in top_cats:
        bar = '█' * min(cnt, 30)
        print(f"    {C.GREEN}{cat:<28}{C.END} {C.CYAN}{cnt:>3}{C.END}  {bar}")
    print()


def dump_all_commands(group_by_cat=True):
    """List every command in the database, optionally grouped by category."""
    conn = _connect()
    cur = conn.cursor()

    if group_by_cat:
        cur.execute("SELECT DISTINCT category FROM commands ORDER BY category")
        cats = [r[0] for r in cur.fetchall()]

        print(f"\n{C.CYAN}{'═' * 60}{C.END}")
        print(f"{C.CYAN}  ALL COMMANDS IN DATABASE{C.END}")
        print(f"{C.CYAN}{'═' * 60}{C.END}")

        grand_total = 0
        for cat in cats:
            cur.execute("SELECT name, description FROM commands WHERE category = ? ORDER BY name", (cat,))
            rows = cur.fetchall()
            grand_total += len(rows)
            print(f"\n  {C.YELLOW}{C.BOLD}{cat}{C.END} ({len(rows)})")
            for name, desc in rows:
                short = desc[:55] + "..." if len(desc) > 58 else desc
                print(f"    {C.GREEN}{name:<20}{C.END} {short}")

        print(f"\n  {C.BOLD}Total: {C.CYAN}{grand_total}{C.END} {C.BOLD}commands{C.END}\n")
    else:
        cur.execute("SELECT name, category, description FROM commands ORDER BY name")
        rows = cur.fetchall()
        print(f"\n{C.BOLD}All {len(rows)} commands (alphabetical):{C.END}\n")
        for name, cat, desc in rows:
            short = desc[:45] + "..." if len(desc) > 48 else desc
            print(f"  {C.GREEN}{name:<20}{C.END} {C.YELLOW}[{cat}]{C.END} {short}")
        print()

    conn.close()


def interactive_db():
    """Interactive SQL shell for power users to query/modify the database directly."""
    if not os.path.exists(DB_PATH):
        print(f"{C.RED}Database not found! Run:  cb --setup{C.END}")
        return

    print(f"\n{C.CYAN}{'═' * 60}{C.END}")
    print(f"{C.CYAN}  COMMANDBRAIN INTERACTIVE DATABASE{C.END}")
    print(f"{C.CYAN}{'═' * 60}{C.END}\n")
    print(f"  {C.BOLD}Database:{C.END} {C.CYAN}{DB_PATH}{C.END}")
    print(f"  {C.BOLD}Table:{C.END}    {C.CYAN}commands{C.END} (id, name, category, description,")
    print(f"           usage, examples, related_commands, notes, tags)\n")
    print(f"  {C.YELLOW}Quick commands:{C.END}")
    print(f"    {C.GREEN}.tables{C.END}    - Show tables")
    print(f"    {C.GREEN}.schema{C.END}    - Show table schema")
    print(f"    {C.GREEN}.count{C.END}     - Count all commands")
    print(f"    {C.GREEN}.categories{C.END} - List categories")
    print(f"    {C.GREEN}.quit{C.END}      - Exit")
    print(f"\n  Type any SQL (SELECT, INSERT, UPDATE, DELETE).")
    print(f"  {C.RED}WARNING: Changes are permanent. Use with care.{C.END}\n")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    while True:
        try:
            sql = input(f"{C.CYAN}cb-sql>{C.END} ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{C.YELLOW}Exiting database shell.{C.END}\n")
            break

        if not sql:
            continue

        # Dot-commands (shortcuts)
        if sql.lower() in ('.quit', '.exit', 'exit', 'quit'):
            print(f"{C.YELLOW}Exiting database shell.{C.END}\n")
            break
        elif sql.lower() == '.tables':
            sql = "SELECT name FROM sqlite_master WHERE type='table'"
        elif sql.lower() == '.schema':
            sql = "SELECT sql FROM sqlite_master WHERE type='table' AND name='commands'"
        elif sql.lower() == '.count':
            sql = "SELECT COUNT(*) AS total_commands FROM commands"
        elif sql.lower() == '.categories':
            sql = "SELECT category, COUNT(*) AS count FROM commands GROUP BY category ORDER BY count DESC"

        try:
            cur = conn.execute(sql)

            # If it's a query that returns rows
            if cur.description:
                cols = [d[0] for d in cur.description]
                rows = cur.fetchall()

                if not rows:
                    print(f"  {C.YELLOW}(0 rows){C.END}")
                    continue

                # Calculate column widths
                widths = [len(c) for c in cols]
                str_rows = []
                for row in rows:
                    str_row = [str(v) if v is not None else "NULL" for v in row]
                    # Truncate long values for display
                    str_row = [v[:60] + "..." if len(v) > 63 else v for v in str_row]
                    for i, v in enumerate(str_row):
                        widths[i] = max(widths[i], len(v))
                    str_rows.append(str_row)

                # Limit column widths
                widths = [min(w, 63) for w in widths]

                # Print header
                header = " | ".join(c.ljust(widths[i]) for i, c in enumerate(cols))
                print(f"  {C.BOLD}{header}{C.END}")
                print(f"  {'─' * len(header)}")

                # Print rows
                for sr in str_rows:
                    line = " | ".join(sr[i].ljust(widths[i]) for i in range(len(cols)))
                    print(f"  {line}")

                print(f"\n  {C.CYAN}({len(rows)} row{'s' if len(rows) != 1 else ''}){C.END}")
            else:
                conn.commit()
                print(f"  {C.GREEN}OK — {cur.rowcount} row(s) affected{C.END}")

        except sqlite3.Error as e:
            print(f"  {C.RED}SQL Error: {e}{C.END}")

    conn.close()


# ─────────────────────────────────────────────────────────────────────────────
# COMPARE, ADD, UPDATE  (interactive commands)
# ─────────────────────────────────────────────────────────────────────────────

def compare_commands(cmd1: str, cmd2: str):
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM commands WHERE name = ?", (cmd1,))
    r1 = cur.fetchone()
    cur.execute("SELECT * FROM commands WHERE name = ?", (cmd2,))
    r2 = cur.fetchone()
    conn.close()

    if not r1:
        print(f"{C.RED}Command '{cmd1}' not found{C.END}"); return
    if not r2:
        print(f"{C.RED}Command '{cmd2}' not found{C.END}"); return

    print(f"\n{C.BOLD}Comparing {C.CYAN}{cmd1}{C.END} {C.BOLD}vs{C.END} {C.CYAN}{cmd2}{C.END}\n")
    print(f"{C.BLUE}{'═' * 70}{C.END}\n")

    for label, idx in [("Description", 3), ("Usage", 4)]:
        print(f"{C.BOLD}{label}:{C.END}")
        print(f"  {C.CYAN}{cmd1}:{C.END} {r1[idx] or '(none)'}")
        print(f"  {C.CYAN}{cmd2}:{C.END} {r2[idx] or '(none)'}\n")

    print(f"{C.BOLD}Examples:{C.END}")
    for name, r in [(cmd1, r1), (cmd2, r2)]:
        if r[5]:
            print(f"  {C.CYAN}{name}:{C.END}")
            for ex in r[5].split('\n')[:2]:
                if ex.strip():
                    print(f"    {C.GREEN}${C.END} {ex}")
    print()


def add_command():
    """Interactive command addition."""
    print(f"\n{C.BOLD}Add New Command{C.END}\n")
    try:
        name = input("Command name: ").strip()
        if not name:
            return print(f"{C.RED}Name required{C.END}")
        cat   = input("Category [General]: ").strip() or "General"
        desc  = input("Description: ").strip()
        if not desc:
            return print(f"{C.RED}Description required{C.END}")
        usage = input("Usage (optional): ").strip()
        examp = input("Examples (\\n separated): ").strip()
        rel   = input("Related commands: ").strip()
        notes = input("Notes: ").strip()
        tags  = input("Tags (comma-separated): ").strip()

        conn = _connect()
        cur = conn.cursor()
        try:
            cur.execute("""INSERT INTO commands
                (name,category,description,usage,examples,related_commands,notes,tags)
                VALUES (?,?,?,?,?,?,?,?)""",
                (name, cat, desc, usage, examp, rel, notes, tags))
            conn.commit()
            print(f"\n{C.GREEN}Added '{name}'{C.END}\n")
        except sqlite3.IntegrityError:
            print(f"\n{C.RED}'{name}' already exists{C.END}\n")
        finally:
            conn.close()
    except KeyboardInterrupt:
        print(f"\n{C.YELLOW}Cancelled{C.END}\n")


def update_command():
    """Interactive command update (add your own notes/examples)."""
    print(f"\n{C.BOLD}Update Command{C.END}\n")
    try:
        name = input("Command name: ").strip()
        if not name:
            return print(f"{C.RED}Name required{C.END}")

        conn = _connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM commands WHERE name = ?", (name,))
        r = cur.fetchone()
        if not r:
            conn.close()
            return print(f"{C.RED}'{name}' not found. Use --add to create it.{C.END}")

        print(f"\n{C.CYAN}Current info for '{name}':{C.END}")
        print(f"  Description: {r[3]}")
        if r[5]: print(f"  Examples: {r[5][:80]}...")
        if r[7]: print(f"  Notes: {r[7][:80]}...")
        print(f"\n{C.YELLOW}Leave blank to keep current value{C.END}\n")

        updates, params = [], []
        for field, col in [("examples", "examples"), ("notes", "notes"), ("tags", "tags")]:
            val = input(f"New {field}: ").strip()
            if val:
                updates.append(f"{col} = ?")
                params.append(val)

        if updates:
            params.append(name)
            cur.execute(f"UPDATE commands SET {', '.join(updates)} WHERE name = ?", params)
            conn.commit()
            print(f"\n{C.GREEN}Updated '{name}'{C.END}\n")
        else:
            print(f"\n{C.YELLOW}No changes{C.END}\n")
        conn.close()
    except KeyboardInterrupt:
        print(f"\n{C.YELLOW}Cancelled{C.END}\n")

# ─────────────────────────────────────────────────────────────────────────────
# IMPORT  (replaces import_commands.py)
# ─────────────────────────────────────────────────────────────────────────────

def import_from_file(path: str):
    """Bulk import commands from a text file. Format: 'command: description' per line."""
    if not os.path.exists(path):
        return print(f"{C.RED}File not found: {path}{C.END}")

    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Strip RTF codes if present
    content = re.sub(r'\\[a-z]+\d*\s?', '', content)
    content = re.sub(r'[{}]', '', content)

    commands, category = [], "General"
    for line in content.split('\n'):
        line = line.strip()
        if not line:
            continue
        # Detect category headers
        if len(line) > 3 and ':' not in line and (
            line.isupper() or any(kw in line for kw in ['Commands','Management','Information','Permissions','Control'])):
            category = line.replace('Commands', '').replace('and', '').strip()
            continue
        # Parse 'command: description'
        if ':' in line:
            parts = line.split(':', 1)
            cmd = parts[0].strip().split()[0].split('<')[0] if parts[0].strip() else ""
            desc = parts[1].strip()
            if cmd and len(cmd) > 1 and not cmd.startswith('-'):
                commands.append((cmd, category, desc, '', '', '', '', category.lower().replace(' ', ',')))

    if not commands:
        return print(f"{C.YELLOW}No commands found in file{C.END}")

    conn = _connect()
    cur = conn.cursor()
    added = skipped = 0
    for c in commands:
        try:
            cur.execute("""INSERT INTO commands
                (name,category,description,usage,examples,related_commands,notes,tags)
                VALUES (?,?,?,?,?,?,?,?)""", c)
            added += 1
        except sqlite3.IntegrityError:
            skipped += 1
    conn.commit()
    conn.close()
    print(f"\n{C.GREEN}Imported {added} commands ({skipped} skipped/existing){C.END}\n")

# ─────────────────────────────────────────────────────────────────────────────
# WORKFLOWS  (data lives in data.py, display logic here)
# ─────────────────────────────────────────────────────────────────────────────

def _load_workflows():
    try:
        from data import WORKFLOWS
        return WORKFLOWS
    except ImportError:
        return None

def list_workflows():
    wf = _load_workflows()
    if not wf:
        return print(f"{C.RED}Workflow data not available{C.END}")

    print(f"\n{C.CYAN}{'═' * 60}{C.END}")
    print(f"{C.CYAN}  AVAILABLE COMMAND CHAINS (WORKFLOWS){C.END}")
    print(f"{C.CYAN}{'═' * 60}{C.END}\n")

    for wid, w in wf.items():
        print(f"  {C.YELLOW}{C.BOLD}{wid}{C.END}")
        print(f"    {w['name']}  [{w['difficulty']}]  ({len(w['steps'])} steps)")
        print(f"    {w['description']}\n")

    print(f"  {C.CYAN}Usage: cb --chain <workflow-id>{C.END}")
    print(f"  {C.CYAN}Example: cb --chain web-pentest{C.END}\n")


def display_workflow(wid: str):
    wf = _load_workflows()
    if not wf:
        return print(f"{C.RED}Workflow data not available{C.END}")
    if wid not in wf:
        print(f"{C.RED}Workflow '{wid}' not found.{C.END}")
        return print(f"{C.YELLOW}Use 'cb --list-chains' to see options.{C.END}")

    w = wf[wid]
    title = w['name'].upper()
    pad = (60 - len(title)) // 2

    print(f"\n{C.CYAN}{'═' * 60}{C.END}")
    print(f"{C.CYAN}{' ' * pad}{title}{C.END}")
    print(f"{C.CYAN}{'═' * 60}{C.END}\n")
    print(f"  {w['description']}")
    print(f"  {C.CYAN}Level: {w['difficulty']}{C.END}  |  {C.GREEN}Steps: {len(w['steps'])}{C.END}\n")

    for s in w['steps']:
        print(f"{C.YELLOW}  Step {s['number']}: {s['title']}{C.END}")
        print(f"    Command:  {C.GREEN}{C.BOLD}{s['command']}{C.END}")
        print(f"    Purpose:  {s['purpose']}")
        if s.get('look_for'):
            print(f"    Look for:")
            for item in s['look_for']:
                print(f"      - {item}")
        tips = s.get('tips', '')
        if tips:
            if isinstance(tips, str):
                print(f"    Tip: {tips}")
            else:
                for t in tips:
                    print(f"    Tip: {t}")
        print()

    print(f"  {C.GREEN}{C.BOLD}Workflow complete!{C.END} Test in a safe, legal environment.")
    print(f"  {C.CYAN}Learn more: cb <command-name>{C.END}\n")

# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(
        prog="cb",
        description="CommandBrain - Smart Linux Command Reference",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  cb ssh                     Search for ssh
  cb password cracking       Search by purpose/task
  cb networking              Top 10 networking tools + related searches
  cb networking --page 2     Page 2 of networking results
  cb -d grep                 Detailed view
  cb -e ssh                  Examples only (quick reference)
  cb --compare grep egrep    Compare two commands
  cb --list                  List all categories
  cb --dump                  List every command (grouped by category)
  cb --stats                 Show database statistics
  cb --db                    Interactive SQL shell (power users)
  cb --chain web-pentest     Show pentest workflow
  cb --workflows             List all workflows
  cb --setup                 Initialize database
  cb --setup --kali          Initialize with Kali tools
        """)

    # Actions
    p.add_argument('--setup',       action='store_true', help='Initialize/reset the command database')
    p.add_argument('--kali',        action='store_true', help='Include Kali security tools (use with --setup)')
    p.add_argument('--list',        action='store_true', help='List all categories')
    p.add_argument('--add',         action='store_true', help='Add a new command interactively')
    p.add_argument('--update',      action='store_true', help='Update a command with your notes')
    p.add_argument('--compare',     nargs=2, metavar=('CMD1', 'CMD2'), help='Compare two commands')
    p.add_argument('--stats',       action='store_true', help='Show database statistics')
    p.add_argument('--dump',        action='store_true', help='List every command in the database')
    p.add_argument('--db',          action='store_true', help='Interactive SQL shell (power users)')
    p.add_argument('--chain', '--workflow',        metavar='WORKFLOW',  help='Show a step-by-step workflow')
    p.add_argument('--list-chains', '--workflows',  action='store_true', help='List all workflows')
    p.add_argument('--import-file', metavar='FILE',      help='Bulk import commands from a text file')

    # Search options
    p.add_argument('query', nargs='*', help='Search term(s)')
    p.add_argument('-d', '--detailed', action='store_true', help='Detailed output')
    p.add_argument('-e', '--examples', action='store_true', help='Examples only')
    p.add_argument('-t', '--type', choices=['all','name','category','tags','description'],
                   default='all', help='Search field (default: all)')
    p.add_argument('--page', '-p', type=int, default=1,
                   help='Page number for search results (default: 1)')
    p.add_argument('--per-page', type=int, default=10,
                   help='Results per page (default: 10, max: 25)')
    p.add_argument('--no-color', action='store_true', help='Disable colored output')

    args = p.parse_args()

    # Handle --no-color
    if args.no_color:
        for attr in vars(Colors):
            if not attr.startswith('_'):
                setattr(Colors, attr, '')

    # Clamp per_page between 5 and 25
    per_page = max(5, min(25, args.per_page))

    # Route to the right action
    if args.setup:
        setup_database(include_kali=args.kali)
    elif args.list_chains:
        list_workflows()
    elif args.chain:
        display_workflow(args.chain)
    elif args.list:
        list_categories()
    elif args.add:
        add_command()
    elif args.update:
        update_command()
    elif args.compare:
        compare_commands(*args.compare)
    elif args.stats:
        show_stats()
    elif args.dump:
        dump_all_commands()
    elif args.db:
        interactive_db()
    elif args.import_file:
        import_from_file(args.import_file)
    elif args.query:
        term = ' '.join(args.query)
        results, total, suggestions = search_commands(
            term, args.type, page=args.page, per_page=per_page)
        if args.examples:
            display_examples(results, term, total, args.page, per_page, suggestions)
        elif args.detailed:
            display_detailed(results, term, total, args.page, per_page, suggestions)
        else:
            display_short(results, term, total, args.page, per_page, suggestions)
    else:
        p.print_help()


if __name__ == "__main__":
    main()

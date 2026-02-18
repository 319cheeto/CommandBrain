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
# SEARCH
# ─────────────────────────────────────────────────────────────────────────────

def search_commands(term: str, mode: str = "all") -> List[Tuple]:
    """Search commands. mode: all | name | category | tags | description"""
    conn = _connect()
    cur = conn.cursor()
    p = f"%{term}%"

    if mode == "name":
        cur.execute("SELECT * FROM commands WHERE name LIKE ? ORDER BY name", (p,))
    elif mode == "category":
        cur.execute("SELECT * FROM commands WHERE category LIKE ? ORDER BY name", (p,))
    elif mode == "tags":
        cur.execute("SELECT * FROM commands WHERE tags LIKE ? ORDER BY name", (p,))
    elif mode == "description":
        cur.execute("SELECT * FROM commands WHERE description LIKE ? OR notes LIKE ? ORDER BY name", (p, p))
    else:
        cur.execute("""
            SELECT * FROM commands
            WHERE name LIKE ? OR description LIKE ? OR tags LIKE ?
               OR related_commands LIKE ? OR category LIKE ?
            ORDER BY
                CASE WHEN name LIKE ? THEN 1 WHEN tags LIKE ? THEN 2 ELSE 3 END,
                name
        """, (p, p, p, p, p, p, p))

    results = cur.fetchall()
    conn.close()
    return results


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
    suggestions = _suggest(term)
    if not suggestions:
        return
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


def display_short(results: List[Tuple], term: str = ""):
    """List view: name, category, one-liner."""
    if not results:
        return _print_no_results(term)
    print(f"\n{C.BOLD}Found {len(results)} command(s):{C.END}\n")
    for r in results:
        print(f"{C.CYAN}{C.BOLD}{r[1]}{C.END} {C.YELLOW}[{r[2]}]{C.END}")
        print(f"  {r[3]}\n")


def display_detailed(results: List[Tuple], term: str = ""):
    """Full info: description, usage, examples, notes, tags."""
    if not results:
        return _print_no_results(term)
    print(f"\n{C.BOLD}Found {len(results)} command(s):{C.END}\n")
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


def display_examples(results: List[Tuple], term: str = ""):
    """Quick-reference: just name + examples."""
    if not results:
        return _print_no_results(term)
    print(f"\n{C.BOLD}Examples for {len(results)} command(s):{C.END}\n")
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
    p.add_argument('--no-color', action='store_true', help='Disable colored output')

    args = p.parse_args()

    # Handle --no-color
    if args.no_color:
        for attr in vars(Colors):
            if not attr.startswith('_'):
                setattr(Colors, attr, '')

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
        results = search_commands(term, args.type)
        if args.examples:
            display_examples(results, term)
        elif args.detailed:
            display_detailed(results, term)
        else:
            display_short(results, term)
    else:
        p.print_help()


if __name__ == "__main__":
    main()

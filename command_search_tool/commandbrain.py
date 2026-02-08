#!/usr/bin/env python3
"""
CommandBrain - Smart Command Reference Tool
Search Linux commands by name, purpose, category, or related tools

ADHD-Friendly Features:
- Instant search results
- Color-coded output for easy scanning
- Multiple search modes
- Short and long format views
"""

import sqlite3
import os
import sys
import argparse
import platform
import difflib
from typing import List, Tuple

# Enable ANSI colors on Windows
if platform.system() == 'Windows':
    try:
        # Windows 10+ supports ANSI escape codes
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        pass  # Fallback to no colors on older Windows

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def get_db_path():
    """Get the database file path"""
    return os.path.expanduser("~/.commandbrain.db")

def connect_db():
    """Connect to the database"""
    db_path = get_db_path()
    if not os.path.exists(db_path):
        print(f"{Colors.RED}Error: Database not found!{Colors.END}")
        print(f"Run setup first: python3 setup_commandbrain.py")
        sys.exit(1)
    try:
        return sqlite3.connect(db_path)
    except sqlite3.Error as e:
        print(f"{Colors.RED}Error connecting to database: {e}{Colors.END}")
        sys.exit(1)

def get_all_command_names() -> List[str]:
    """
    Get all command names from the database for fuzzy matching
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT name FROM commands ORDER BY name")
        names = [row[0] for row in cursor.fetchall()]
        return names
    except sqlite3.Error:
        return []
    finally:
        conn.close()

def suggest_similar_commands(search_term: str, max_suggestions: int = 5) -> List[str]:
    """
    Suggest similar command names using fuzzy matching
    Returns up to max_suggestions similar commands
    """
    all_commands = get_all_command_names()
    if not all_commands:
        return []
    
    # Use difflib to find close matches
    # cutoff=0.6 means 60% similarity required
    suggestions = difflib.get_close_matches(search_term, all_commands, n=max_suggestions, cutoff=0.6)
    return suggestions

def search_commands(search_term: str, search_type: str = "all") -> List[Tuple]:
    """
    Search for commands in the database
    
    search_type options:
    - all: Search name, description, tags, related commands
    - name: Search only command names
    - category: Search by category
    - tags: Search by tags
    - description: Search in descriptions
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    search_pattern = f"%{search_term}%"
    
    if search_type == "name":
        query = "SELECT * FROM commands WHERE name LIKE ? ORDER BY name"
        cursor.execute(query, (search_pattern,))
    
    elif search_type == "category":
        query = "SELECT * FROM commands WHERE category LIKE ? ORDER BY name"
        cursor.execute(query, (search_pattern,))
    
    elif search_type == "tags":
        query = "SELECT * FROM commands WHERE tags LIKE ? ORDER BY name"
        cursor.execute(query, (search_pattern,))
    
    elif search_type == "description":
        query = "SELECT * FROM commands WHERE description LIKE ? OR notes LIKE ? ORDER BY name"
        cursor.execute(query, (search_pattern, search_pattern))
    
    else:  # "all"
        query = """
            SELECT * FROM commands 
            WHERE name LIKE ? 
               OR description LIKE ? 
               OR tags LIKE ? 
               OR related_commands LIKE ?
               OR category LIKE ?
            ORDER BY 
                CASE 
                    WHEN name LIKE ? THEN 1
                    WHEN tags LIKE ? THEN 2
                    ELSE 3
                END,
                name
        """
        cursor.execute(query, (search_pattern, search_pattern, search_pattern, 
                               search_pattern, search_pattern, search_pattern, search_pattern))
    
    results = cursor.fetchall()
    conn.close()
    
    return results

def display_short(results: List[Tuple], search_term: str = ""):
    """Display results in short format (list view)"""
    if not results:
        print(f"{Colors.YELLOW}No commands found for '{search_term}'.{Colors.END}")
        
        # Suggest similar commands using fuzzy matching
        if search_term:
            suggestions = suggest_similar_commands(search_term)
            if suggestions:
                print(f"\n{Colors.CYAN}💡 Did you mean:{Colors.END}")
                
                # Get brief info for each suggestion
                conn = connect_db()
                cursor = conn.cursor()
                for cmd in suggestions:
                    cursor.execute("SELECT description FROM commands WHERE name = ?", (cmd,))
                    result = cursor.fetchone()
                    if result:
                        desc = result[0]
                        # Truncate long descriptions
                        if len(desc) > 60:
                            desc = desc[:57] + "..."
                        print(f"  {Colors.GREEN}{cmd}{Colors.END} - {desc}")
                conn.close()
                print(f"\n{Colors.BOLD}Try:{Colors.END} cb {suggestions[0]}")
        return
    
    print(f"\n{Colors.BOLD}Found {len(results)} command(s):{Colors.END}\n")
    
    for row in results:
        name = row[1]
        category = row[2]
        description = row[3]
        
        print(f"{Colors.CYAN}{Colors.BOLD}{name}{Colors.END} "
              f"{Colors.YELLOW}[{category}]{Colors.END}")
        print(f"  {description}")
        print()

def display_detailed(results: List[Tuple], search_term: str = ""):
    """Display results in detailed format"""
    if not results:
        print(f"{Colors.YELLOW}No commands found for '{search_term}'.{Colors.END}")
        
        # Suggest similar commands using fuzzy matching
        if search_term:
            suggestions = suggest_similar_commands(search_term)
            if suggestions:
                print(f"\n{Colors.CYAN}💡 Did you mean:{Colors.END}")
                
                # Get brief info for each suggestion
                conn = connect_db()
                cursor = conn.cursor()
                for cmd in suggestions:
                    cursor.execute("SELECT description FROM commands WHERE name = ?", (cmd,))
                    result = cursor.fetchone()
                    if result:
                        desc = result[0]
                        # Truncate long descriptions
                        if len(desc) > 60:
                            desc = desc[:57] + "..."
                        print(f"  {Colors.GREEN}{cmd}{Colors.END} - {desc}")
                conn.close()
                print(f"\n{Colors.BOLD}Try:{Colors.END} cb {suggestions[0]}")
        return
    
    print(f"\n{Colors.BOLD}Found {len(results)} command(s):{Colors.END}\n")
    
    for i, row in enumerate(results, 1):
        if i > 1:
            print(f"\n{Colors.BLUE}{'─' * 70}{Colors.END}\n")
        
        name = row[1]
        category = row[2]
        description = row[3]
        usage = row[4]
        examples = row[5]
        related = row[6]
        notes = row[7]
        tags = row[8]
        
        # Command name and category
        print(f"{Colors.CYAN}{Colors.BOLD}{name}{Colors.END} "
              f"{Colors.YELLOW}[{category}]{Colors.END}")
        print(f"{Colors.BOLD}Description:{Colors.END} {description}")
        
        # Usage
        if usage:
            print(f"\n{Colors.BOLD}Usage:{Colors.END}")
            print(f"  {usage}")
        
        # Examples
        if examples:
            print(f"\n{Colors.BOLD}Examples:{Colors.END}")
            for example in examples.split('\n'):
                print(f"  {Colors.GREEN}${Colors.END} {example}")
        
        # Related commands
        if related:
            print(f"\n{Colors.BOLD}Related Commands:{Colors.END} {Colors.CYAN}{related}{Colors.END}")
        
        # Notes
        if notes:
            print(f"\n{Colors.BOLD}Notes:{Colors.END}")
            print(f"  💡 {notes}")
        
        # Tags
        if tags:
            print(f"\n{Colors.BOLD}Tags:{Colors.END} {tags}")

def display_examples_only(results: List[Tuple], search_term: str = ""):
    """Display only examples in a quick-reference format"""
    if not results:
        print(f"{Colors.YELLOW}No commands found for '{search_term}'.{Colors.END}")
        
        # Suggest similar commands using fuzzy matching
        if search_term:
            suggestions = suggest_similar_commands(search_term)
            if suggestions:
                print(f"\n{Colors.CYAN}💡 Did you mean:{Colors.END}")
                
                # Get brief info for each suggestion
                conn = connect_db()
                cursor = conn.cursor()
                for cmd in suggestions:
                    cursor.execute("SELECT description FROM commands WHERE name = ?", (cmd,))
                    result = cursor.fetchone()
                    if result:
                        desc = result[0]
                        # Truncate long descriptions
                        if len(desc) > 60:
                            desc = desc[:57] + "..."
                        print(f"  {Colors.GREEN}{cmd}{Colors.END} - {desc}")
                conn.close()
                print(f"\n{Colors.BOLD}Try:{Colors.END} cb {suggestions[0]}")
        return
    
    print(f"\n{Colors.BOLD}Examples for {len(results)} command(s):{Colors.END}\n")
    
    for i, row in enumerate(results, 1):
        if i > 1:
            print(f"{Colors.BLUE}{'─' * 50}{Colors.END}\n")
        
        name = row[1]
        examples = row[5]
        usage = row[4]
        
        # Command name
        print(f"{Colors.CYAN}{Colors.BOLD}{name}{Colors.END}")
        
        # Usage (brief)
        if usage:
            print(f"  {Colors.BOLD}Usage:{Colors.END} {usage}")
        
        # Examples (main focus)
        if examples:
            for example in examples.split('\n'):
                if example.strip():
                    print(f"  {Colors.GREEN}${Colors.END} {example}")
        else:
            print(f"  {Colors.YELLOW}(No examples available){Colors.END}")
        
        print()

def list_categories():
    """List all available categories"""
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT DISTINCT category FROM commands ORDER BY category")
        categories = cursor.fetchall()
        
        print(f"\n{Colors.BOLD}Available Categories:{Colors.END}\n")
        for cat in categories:
            cursor.execute("SELECT COUNT(*) FROM commands WHERE category = ?", (cat[0],))
            count = cursor.fetchone()[0]
            print(f"  {Colors.CYAN}{cat[0]}{Colors.END} ({count} commands)")
        print()
    except sqlite3.Error as e:
        print(f"{Colors.RED}Database error: {e}{Colors.END}")
    finally:
        conn.close()

def update_command_interactive():
    """Update an existing command with personal notes/examples"""
    print(f"\n{Colors.BOLD}Update Command{Colors.END}\n")
    
    try:
        name = input("Command name to update: ").strip()
        if not name:
            print(f"{Colors.RED}Command name is required{Colors.END}")
            return
        
        conn = connect_db()
        cursor = conn.cursor()
        
        # Check if command exists
        cursor.execute("SELECT * FROM commands WHERE name = ?", (name,))
        result = cursor.fetchone()
        
        if not result:
            print(f"{Colors.RED}✗ Command '{name}' not found{Colors.END}")
            print(f"\nUse --add to create a new command")
            conn.close()
            return
        
        # Display current info
        print(f"\n{Colors.CYAN}Current info for '{name}':{Colors.END}")
        print(f"Description: {result[3]}")
        if result[5]:  # examples
            print(f"Examples: {result[5][:100]}...")
        if result[7]:  # notes
            print(f"Notes: {result[7][:100]}...")
        
        print(f"\n{Colors.YELLOW}Leave blank to keep existing value{Colors.END}\n")
        
        # Get updates
        new_examples = input("Add/replace examples (separate with \\n): ").strip()
        new_notes = input("Add/replace notes: ").strip()
        new_tags = input("Add/replace tags (comma-separated): ").strip()
        
        # Update database
        updates = []
        params = []
        
        if new_examples:
            updates.append("examples = ?")
            params.append(new_examples)
        if new_notes:
            updates.append("notes = ?")
            params.append(new_notes)
        if new_tags:
            updates.append("tags = ?")
            params.append(new_tags)
        
        if updates:
            params.append(name)
            query = f"UPDATE commands SET {', '.join(updates)} WHERE name = ?"
            cursor.execute(query, params)
            conn.commit()
            print(f"\n{Colors.GREEN}✓ Command '{name}' updated successfully!{Colors.END}\n")
        else:
            print(f"\n{Colors.YELLOW}No changes made{Colors.END}\n")
        
        conn.close()
    
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Cancelled{Colors.END}\n")
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.END}\n")

def compare_commands(cmd1: str, cmd2: str):
    """Compare two commands side-by-side"""
    conn = connect_db()
    cursor = conn.cursor()
    
    # Get both commands
    cursor.execute("SELECT * FROM commands WHERE name = ?", (cmd1,))
    result1 = cursor.fetchone()
    
    cursor.execute("SELECT * FROM commands WHERE name = ?", (cmd2,))
    result2 = cursor.fetchone()
    
    conn.close()
    
    if not result1:
        print(f"{Colors.RED}Command '{cmd1}' not found{Colors.END}")
        return
    if not result2:
        print(f"{Colors.RED}Command '{cmd2}' not found{Colors.END}")
        return
    
    # Display comparison
    print(f"\n{Colors.BOLD}Comparing {Colors.CYAN}{cmd1}{Colors.END} {Colors.BOLD}vs{Colors.END} {Colors.CYAN}{cmd2}{Colors.END}\n")
    print(f"{Colors.BLUE}{'═' * 70}{Colors.END}\n")
    
    # Description
    print(f"{Colors.BOLD}Description:{Colors.END}")
    print(f"  {Colors.CYAN}{cmd1}:{Colors.END} {result1[3]}")
    print(f"  {Colors.CYAN}{cmd2}:{Colors.END} {result2[3]}")
    print()
    
    # Usage
    print(f"{Colors.BOLD}Usage:{Colors.END}")
    print(f"  {Colors.CYAN}{cmd1}:{Colors.END} {result1[4] if result1[4] else '(not specified)'}")
    print(f"  {Colors.CYAN}{cmd2}:{Colors.END} {result2[4] if result2[4] else '(not specified)'}")
    print()
    
    # Examples
    print(f"{Colors.BOLD}Examples:{Colors.END}")
    if result1[5]:
        print(f"  {Colors.CYAN}{cmd1}:{Colors.END}")
        for ex in result1[5].split('\n')[:2]:  # Show first 2 examples
            if ex.strip():
                print(f"    {Colors.GREEN}${Colors.END} {ex}")
    if result2[5]:
        print(f"  {Colors.CYAN}{cmd2}:{Colors.END}")
        for ex in result2[5].split('\n')[:2]:
            if ex.strip():
                print(f"    {Colors.GREEN}${Colors.END} {ex}")
    print()
    
    # Key differences in notes
    if result1[7] or result2[7]:
        print(f"{Colors.BOLD}Key Differences:{Colors.END}")
        if result1[7]:
            print(f"  {Colors.CYAN}{cmd1}:{Colors.END} {result1[7]}")
        if result2[7]:
            print(f"  {Colors.CYAN}{cmd2}:{Colors.END} {result2[7]}")
        print()
    
    # Related commands
    print(f"{Colors.BOLD}See also:{Colors.END}")
    if result1[6]:
        print(f"  From {cmd1}: {Colors.CYAN}{result1[6]}{Colors.END}")
    if result2[6]:
        print(f"  From {cmd2}: {Colors.CYAN}{result2[6]}{Colors.END}")
    print()

def add_command_interactive():
    """Interactive command addition"""
    print(f"\n{Colors.BOLD}Add New Command{Colors.END}\n")
    
    try:
        name = input("Command name: ").strip()
        if not name:
            print(f"{Colors.RED}Command name is required{Colors.END}")
            return
        
        category = input("Category: ").strip()
        if not category:
            category = "General"
        
        description = input("Description: ").strip()
        if not description:
            print(f"{Colors.RED}Description is required{Colors.END}")
            return
        
        usage = input("Usage (optional): ").strip()
        examples = input("Examples (separate multiple with \\n): ").strip()
        related = input("Related commands (comma-separated): ").strip()
        notes = input("Notes/tips (optional): ").strip()
        tags = input("Tags (comma-separated): ").strip()
        
        conn = connect_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO commands 
                (name, category, description, usage, examples, related_commands, notes, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, category, description, usage, examples, related, notes, tags))
            
            conn.commit()
            print(f"\n{Colors.GREEN}✓ Command '{name}' added successfully!{Colors.END}\n")
        
        except sqlite3.IntegrityError:
            print(f"\n{Colors.RED}✗ Command '{name}' already exists{Colors.END}\n")
        except sqlite3.Error as e:
            print(f"\n{Colors.RED}Database error: {e}{Colors.END}\n")
        finally:
            conn.close()
    
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Cancelled{Colors.END}\n")
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.END}\n")

def show_stats():
    """Show database statistics"""
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT COUNT(*) FROM commands")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT category) FROM commands")
        categories = cursor.fetchone()[0]
        
        print(f"\n{Colors.BOLD}CommandBrain Statistics{Colors.END}\n")
        print(f"  Total commands: {Colors.CYAN}{total}{Colors.END}")
        print(f"  Categories: {Colors.CYAN}{categories}{Colors.END}")
        print(f"  Database: {Colors.CYAN}{get_db_path()}{Colors.END}")
        print()
    except sqlite3.Error as e:
        print(f"{Colors.RED}Database error: {e}{Colors.END}")
    finally:
        conn.close()

def main():
    parser = argparse.ArgumentParser(
        description="CommandBrain - Smart Linux Command Reference",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  cb ssh                     # Search for ssh
  cb password cracking       # Search by purpose/task
  cb -d grep                 # Detailed view with full info
  cb -e ssh                  # Examples only (quick reference)
  cb --compare grep egrep    # Compare two commands
  cb --list                  # List all categories
  cb --update ssh            # Add your own notes/examples
  
  # Advanced:
  cb -t name ssh             # Search command names only
  cb -t category network     # Search by category
        """
    )
    
    # Global flags that work without subcommands
    parser.add_argument('--list', action='store_true',
                       help='List all categories')
    parser.add_argument('--add', action='store_true',
                       help='Add a new command interactively')
    parser.add_argument('--update', action='store_true',
                       help='Update an existing command with your own notes/examples')
    parser.add_argument('--compare', nargs=2, metavar=('CMD1', 'CMD2'),
                       help='Compare two commands side-by-side')
    parser.add_argument('--stats', action='store_true',
                       help='Show database statistics')
    
    # Search options (default action)
    parser.add_argument('query', nargs='*', 
                       help='Search term(s) - can be multiple words')
    parser.add_argument('-d', '--detailed', action='store_true',
                       help='Show detailed output with full information')
    parser.add_argument('-e', '--examples', action='store_true',
                       help='Show examples only (quick reference mode)')
    parser.add_argument('-t', '--type', 
                       choices=['all', 'name', 'category', 'tags', 'description'],
                       default='all',
                       help='Search type: all(default), name, category, tags, description')
    
    args = parser.parse_args()
    
    # Handle special commands first
    if args.list:
        list_categories()
    elif args.add:
        add_command_interactive()
    elif args.update:
        update_command_interactive()
    elif args.compare:
        compare_commands(args.compare[0], args.compare[1])
    elif args.stats:
        show_stats()
    elif args.query:
        # Join all query words into a single search string
        search_term = ' '.join(args.query)
        results = search_commands(search_term, args.type)
        
        # Choose display mode
        if args.examples:
            display_examples_only(results, search_term)
        elif args.detailed:
            display_detailed(results, search_term)
        else:
            display_short(results, search_term)
    else:
        # No arguments provided
        parser.print_help()

if __name__ == "__main__":
    main()

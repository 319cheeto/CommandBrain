#!/usr/bin/env python3
"""
Bulk Command Importer for CommandBrain
Import commands from structured text files
"""

import sqlite3
import os
import sys
import re

def get_db_path():
    """Get the database file path"""
    return os.path.expanduser("~/.commandbrain.db")

def connect_db():
    """Connect to the database"""
    db_path = get_db_path()
    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}")
        print("Please run setup_commandbrain.py first to create the database.")
        sys.exit(1)
    try:
        return sqlite3.connect(db_path)
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)

def parse_rtf_commands(file_path):
    """
    Parse commands from your RTF file format
    Expected format:
    command: Description text.
    """
    commands = []
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Remove RTF formatting codes
        content = re.sub(r'\\[a-z]+\d*\s?', '', content)
        content = re.sub(r'[{}]', '', content)
        
        # Split into sections by headers
        current_category = "Uncategorized"
        
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            
            # Detect category headers (lines that are mostly capitalized or end with specific patterns)
            if line and len(line) > 3 and not ':' in line and (
                line.isupper() or 
                'Commands' in line or 
                'Management' in line or
                'Information' in line or
                'Permissions' in line or
                'Control' in line
            ):
                current_category = line.replace('Commands', '').replace('and', '').strip()
                continue
            
            # Parse command entries (format: "command: description")
            if ':' in line:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    cmd_name = parts[0].strip()
                    description = parts[1].strip()
                    
                    # Skip if it looks like a subcommand or option
                    if cmd_name and not cmd_name.startswith('-') and ' ' not in cmd_name.split()[0]:
                        # Extract the actual command (first word before any <> or options)
                        actual_cmd = cmd_name.split()[0].split('<')[0].strip()
                        
                        if actual_cmd and len(actual_cmd) > 1:
                            commands.append({
                                'name': actual_cmd,
                                'category': current_category if current_category != "Uncategorized" else "General",
                                'description': description,
                                'usage': '',
                                'examples': '',
                                'related_commands': '',
                                'notes': '',
                                'tags': current_category.lower().replace(' ', ',')
                            })
        
        return commands
    
    except Exception as e:
        print(f"Error parsing file: {e}")
        return []

def import_commands(commands):
    """Import commands into the database"""
    conn = connect_db()
    cursor = conn.cursor()
    
    added = 0
    skipped = 0
    
    for cmd in commands:
        try:
            cursor.execute("""
                INSERT INTO commands 
                (name, category, description, usage, examples, related_commands, notes, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                cmd['name'],
                cmd['category'],
                cmd['description'],
                cmd['usage'],
                cmd['examples'],
                cmd['related_commands'],
                cmd['notes'],
                cmd['tags']
            ))
            added += 1
            print(f"✓ Added: {cmd['name']}")
        
        except sqlite3.IntegrityError:
            skipped += 1
            print(f"- Skipped (exists): {cmd['name']}")
        except sqlite3.Error as e:
            print(f"! Error importing {cmd['name']}: {e}")
            skipped += 1
    
    try:
        conn.commit()
    except sqlite3.Error as e:
        print(f"\nError committing changes: {e}")
        conn.rollback()
    finally:
        conn.close()
    
    print(f"\n{'='*50}")
    print(f"Import complete!")
    print(f"Added: {added} commands")
    print(f"Skipped: {skipped} commands (already exist)")
    print(f"{'='*50}\n")

def main():
    print("CommandBrain Bulk Importer")
    print("="*50)
    
    try:
        file_path = input("\nEnter the path to your command list file: ").strip()
        
        # Remove quotes if user wrapped path in quotes
        file_path = file_path.strip('"\'')
        
        if not file_path:
            print("Error: No file path provided")
            return
        
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}")
            return
        
        print(f"\nParsing commands from: {file_path}")
        commands = parse_rtf_commands(file_path)
        
        print(f"Found {len(commands)} commands to import\n")
        
        if commands:
            confirm = input("Import these commands? (y/n): ").strip().lower()
            if confirm == 'y':
                import_commands(commands)
            else:
                print("Import cancelled")
        else:
            print("No commands found to import")
    
    except KeyboardInterrupt:
        print("\n\nImport cancelled by user")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

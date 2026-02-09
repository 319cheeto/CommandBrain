#!/usr/bin/env python3
"""
CommandBrain Setup Script
Creates and populates the command database
"""

import sqlite3
import os
import sys

def create_database():
    """Create the SQLite database with proper schema"""
    
    # Database location - portable to home directory
    db_path = os.path.expanduser("~/.commandbrain.db")
    
    print(f"Creating database at: {db_path}")
    
    try:
        # Connect to database (creates if doesn't exist)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create the commands table
        cursor.execute("""
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
        
        # Create index for faster searching
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_name ON commands(name)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_category ON commands(category)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tags ON commands(tags)")
        
        print("✓ Database schema created")
        
        conn.commit()
        return conn, cursor
    
    except sqlite3.Error as e:
        print(f"Error creating database: {e}")
        sys.exit(1)

def populate_basic_commands(cursor):
    """Populate database with basic Linux commands from your list"""
    
    commands = [
        # Basic Commands
        ("ls", "Basic", "Lists files and directories in the current directory", 
         "ls [options] [path]", "ls -la /home", "dir, tree, find", 
         "Use -l for detailed view, -a to show hidden files", "file-listing,directory,navigation"),
        
        ("cd", "Basic", "Changes the current directory", 
         "cd [path]", "cd /home/user\ncd ..\ncd ~", "pwd, pushd, popd", 
         "cd ~ goes to home directory, cd - goes to previous directory", "navigation,directory"),
        
        ("pwd", "Basic", "Prints the current working directory", 
         "pwd", "pwd", "cd, ls", 
         "Shows full path from root (/)", "navigation,directory,path"),
        
        ("mkdir", "Basic", "Creates a new directory", 
         "mkdir [options] directory", "mkdir newfolder\nmkdir -p path/to/nested/dir", "rmdir, rm", 
         "Use -p to create parent directories if they don't exist", "directory,file-management,creation"),
        
        ("rm", "Basic", "Removes files or directories", 
         "rm [options] file/directory", "rm file.txt\nrm -r folder\nrm -rf folder", "rmdir, unlink, shred", 
         "DANGEROUS! -r for directories, -f to force. No recycle bin!", "file-management,deletion,dangerous"),
        
        ("cp", "Basic", "Copies files or directories", 
         "cp [options] source destination", "cp file.txt backup.txt\ncp -r folder newfolder", "mv, rsync, scp", 
         "Use -r for directories, -p to preserve permissions", "file-management,copy"),
        
        ("mv", "Basic", "Moves or renames files or directories", 
         "mv source destination", "mv old.txt new.txt\nmv file.txt /home/user/", "cp, rename", 
         "Same command for both moving and renaming", "file-management,move,rename"),
        
        ("cat", "Basic", "Concatenates and displays file content", 
         "cat [files]", "cat file.txt\ncat file1.txt file2.txt > combined.txt", "more, less, head, tail, tac", 
         "tac displays file in reverse. Use for small files only", "file-viewing,text"),
        
        ("grep", "Searching", "Searches for patterns in files", 
         "grep [options] pattern [files]", "grep 'error' log.txt\ngrep -r 'password' /etc/", "egrep, fgrep, ack, ag, ripgrep", 
         "Use -i for case-insensitive, -r for recursive, -n for line numbers", "search,text-processing,pattern-matching"),
        
        ("find", "Searching", "Searches for files and directories", 
         "find [path] [options]", "find /home -name '*.txt'\nfind . -type f -mtime -7", "locate, which, whereis", 
         "Very powerful but slow on large directories. locate is faster but less current", "search,file-finding"),
        
        # Permissions
        ("chmod", "Permissions", "Changes file/directory permissions", 
         "chmod [options] mode file", "chmod 755 script.sh\nchmod u+x file.sh\nchmod -R 644 folder/", "chown, chgrp", 
         "755 = rwxr-xr-x (owner full, others read+execute). 644 = rw-r--r--", "permissions,security,file-management"),
        
        ("chown", "Permissions", "Changes file/directory owner", 
         "chown [options] user[:group] file", "chown user file.txt\nchown user:group file.txt", "chmod, chgrp", 
         "Need sudo for files you don't own", "permissions,security,ownership"),
        
        # System Info
        ("top", "System-Info", "Displays real-time system processes and resource usage", 
         "top", "top\ntop -u username", "htop, ps, atop", 
         "Press 'q' to quit, 'k' to kill process. htop is more user-friendly", "monitoring,processes,performance"),
        
        ("ps", "System-Info", "Shows current processes", 
         "ps [options]", "ps aux\nps -ef\nps -u username", "top, htop, pgrep, pidof", 
         "ps aux shows all processes. Common for finding PIDs", "processes,monitoring"),
        
        ("df", "System-Info", "Displays disk space usage", 
         "df [options]", "df -h\ndf -h /home", "du, lsblk, fdisk", 
         "-h flag makes output human-readable (GB instead of blocks)", "disk,storage,monitoring"),
        
        # Networking
        ("ping", "Networking", "Tests connectivity to a host", 
         "ping [options] host", "ping google.com\nping -c 4 192.168.1.1", "traceroute, mtr, nmap", 
         "Use -c to limit count, otherwise it runs forever. CTRL+C to stop", "network,troubleshooting,connectivity"),
        
        ("ifconfig", "Networking", "Displays network interface configuration (deprecated)", 
         "ifconfig [interface]", "ifconfig\nifconfig eth0", "ip, nmcli", 
         "DEPRECATED - use 'ip a' instead on modern systems", "network,configuration,deprecated"),
        
        ("ip", "Networking", "Shows/manipulates routing, devices, policy routing and tunnels", 
         "ip [options] object command", "ip a\nip link show\nip route", "ifconfig, route", 
         "Modern replacement for ifconfig. 'ip a' = show all addresses", "network,configuration,routing"),
        
        ("netstat", "Networking", "Displays network connections, routing tables, interface stats", 
         "netstat [options]", "netstat -tuln\nnetstat -antp", "ss, lsof, nmap", 
         "-tuln shows TCP/UDP listening ports. ss is the modern replacement", "network,monitoring,connections"),
        
        ("ss", "Networking", "Socket statistics - modern netstat replacement", 
         "ss [options]", "ss -tuln\nss -tanp", "netstat, lsof", 
         "Faster than netstat. -t=TCP, -u=UDP, -l=listening, -n=numeric", "network,monitoring,sockets"),
        
        # User Management
        ("sudo", "User-Management", "Executes command with superuser privileges", 
         "sudo command", "sudo apt update\nsudo -i", "su, pkexec", 
         "Logs all commands. sudo -i gives root shell. Use carefully!", "permissions,security,admin"),
        
        ("passwd", "User-Management", "Changes user password", 
         "passwd [username]", "passwd\nsudo passwd username", "chpasswd", 
         "Without username changes your own password", "security,user-management,authentication"),
        
        # Package Management
        ("apt", "Package-Management", "Debian/Ubuntu package manager", 
         "apt [command] [options]", "apt update\napt install package\napt search keyword", "dpkg, apt-get, aptitude", 
         "update refreshes package list, upgrade installs updates, install adds new packages", "packages,software,installation"),
        
        # System Control
        ("systemctl", "System-Control", "Controls systemd services and system", 
         "systemctl [command] [service]", "systemctl status ssh\nsystemctl restart nginx\nsystemctl enable apache2", "service, chkconfig", 
         "enable = start on boot, disable = don't start on boot, status shows if running", "services,system,management"),
        
        ("shutdown", "System-Control", "Shuts down or reboots the system", 
         "shutdown [options] [time]", "shutdown -h now\nshutdown -r +5\nshutdown -c", "reboot, halt, poweroff", 
         "-h = halt, -r = reboot, -c = cancel scheduled shutdown, 'now' or +minutes", "system,power,shutdown"),
        
        # Text Processing
        ("awk", "Text-Processing", "Pattern scanning and text processing language", 
         "awk 'pattern {action}' file", "awk '{print $1}' file.txt\nawk -F: '{print $1}' /etc/passwd", "sed, cut, grep", 
         "Powerful for column-based data. $1 = first column, $2 = second, etc.", "text,processing,scripting"),
        
        ("sed", "Text-Processing", "Stream editor for filtering and transforming text", 
         "sed 's/pattern/replacement/' file", "sed 's/old/new/g' file.txt\nsed -i 's/foo/bar/' file.txt", "awk, tr, grep", 
         "-i edits file in-place. s = substitute, g = global (all occurrences)", "text,processing,editing"),
        
        # Archiving
        ("tar", "Archiving", "Creates and extracts archive files", 
         "tar [options] archive files", "tar -czf archive.tar.gz folder/\ntar -xzf archive.tar.gz", "gzip, zip, 7z", 
         "-c=create, -x=extract, -z=gzip, -f=file, -v=verbose. Remember: 'eXtract Ze Files'", "compression,archiving,backup"),
        
        # Security
        ("ssh", "Security", "Secure Shell - remote login protocol", 
         "ssh [user@]host [command]", "ssh user@192.168.1.10\nssh -p 2222 user@host", "scp, sftp, telnet", 
         "Use -p for custom port. Keys are more secure than passwords. Telnet is UNENCRYPTED (bad!)", "network,remote-access,security"),
        
        ("scp", "Security", "Secure copy - transfers files over SSH", 
         "scp source destination", "scp file.txt user@host:/path/\nscp -r folder user@host:/path/", "rsync, sftp, ftp", 
         "Use -r for directories. rsync is better for large/frequent transfers", "network,file-transfer,security"),
    ]
    
    # Insert commands
    try:
        cursor.executemany("""
            INSERT OR IGNORE INTO commands 
            (name, category, description, usage, examples, related_commands, notes, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, commands)
        
        print(f"✓ Populated {len(commands)} basic commands")
    except sqlite3.Error as e:
        print(f"Error populating commands: {e}")
        raise

def main():
    """Main setup function"""
    print("=" * 60)
    print("CommandBrain Database Setup")
    print("=" * 60)
    print()
    
    try:
        conn, cursor = create_database()
        populate_basic_commands(cursor)
        
        conn.commit()
        conn.close()
        
        print()
        print("=" * 60)
        print("✓ Setup Complete!")
        print("=" * 60)
        print()
        print("Next steps:")
        if os.name != 'nt':  # Not Windows
            print("1. Make commandbrain.py executable: chmod +x commandbrain.py")
            print("2. Search for commands: ./commandbrain.py search ssh")
        else:  # Windows
            print("1. Search for commands: python commandbrain.py search ssh")
        print("3. Add to PATH for easy access (optional)")
        print()
    
    except Exception as e:
        print(f"\nSetup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user")
        sys.exit(0)

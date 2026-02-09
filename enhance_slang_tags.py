#!/usr/bin/env python3
"""
CommandBrain Slang & Purpose Enhancement Script
Adds student-friendly search terms, slang, and purpose-based keywords

Run this to make CommandBrain searchable by PURPOSE, not just command names!
"""

import sqlite3
import os
import sys

def get_db_path():
    return os.path.expanduser("~/.commandbrain.db")

def enhance_slang_tags():
    """Add comprehensive slang terms and purpose-based keywords"""
    
    db_path = get_db_path()
    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}")
        print("Please run setup_commandbrain.py first.")
        sys.exit(1)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)
    
    print("=" * 70)
    print("CommandBrain Slang Enhancement")
    print("=" * 70)
    print()
    print("Adding student-friendly search terms...")
    print()
    
    # Comprehensive slang mappings for EVERY command
    # Format: command_name: [slang terms, purposes, student language, misspellings]
    slang_mappings = {
        # BASIC COMMANDS - Purpose-based
        "ls": ["list, listing, show files, see files, what files, dir, directory, view files"],
        "cd": ["change dir, go to, navigate, move to, switch folder, goto"],
        "pwd": ["where am i, current location, current directory, print directory, path"],
        "mkdir": ["make folder, create folder, new folder, make directory, new dir"],
        "rm": ["delete, remove, erase, del, destroy, delete file, remove file"],
        "cp": ["copy, duplicate, backup, clone"],
        "mv": ["move, rename, relocate, transfer"],
        "cat": ["read, view, show, display, print, see file, open file"],
        "grep": ["search, find text, search text, find in file, pattern search, filter, regex, regular expression"],
        "find": ["search files, locate, find file, file search, where is, locate file"],
        
        # PERMISSIONS
        "chmod": ["permissions, change permissions, file permissions, access, rights, executable, make executable"],
        "chown": ["owner, ownership, change owner, file owner"],
        
        # SYSTEM INFO
        "top": ["processes, cpu, memory, performance, running, tasks, resource usage, what's running"],
        "ps": ["processes, running, tasks, process list, show processes"],
        "df": ["disk, disk space, storage, free space, how much space, disk usage"],
        
        # NETWORKING - CRITICAL FOR STUDENTS
        "ping": ["test connection, check connection, reachability, alive, test network, can i reach, connectivity, test ping"],
        "ifconfig": ["ip address, my ip, network config, interface, network card, nic"],
        "ip": ["ip address, my ip, network, routing, interface, network config"],
        "netstat": ["connections, ports, network connections, listening, open ports, network status"],
        "ss": ["sockets, connections, ports, listening, open ports, network"],
        
        # USER MANAGEMENT
        "sudo": ["root, admin, administrator, superuser, privilege, elevated, run as admin, permission"],
        "passwd": ["password, change password, set password, pw, reset password"],
        
        # PACKAGES
        "apt": ["install, software, package, program, application, update, upgrade"],
        
        # SYSTEM CONTROL
        "systemctl": ["service, daemon, start, stop, restart, enable, disable"],
        "shutdown": ["reboot, restart, power off, turn off, halt"],
        
        # TEXT PROCESSING
        "awk": ["text processing, columns, fields, parse, extract"],
        "sed": ["replace, substitute, edit, text edit, find replace, stream editor"],
        
        # ARCHIVING
        "tar": ["compress, archive, zip, extract, unzip, backup, package"],
        
        # SECURITY - BASIC
        "ssh": ["remote, remote login, secure shell, connect, remote access, login remotely"],
        "scp": ["copy, transfer, file transfer, secure copy, send file, remote copy"],
        
        # KALI TOOLS - NETWORK SCANNING (HIGH PRIORITY!)
        "nmap": ["scan, scanning, port scan, network scan, reconnaissance, recon, enum, enumeration, discovery, find hosts, find ports, service detection, port scanner, network scanner, probe"],
        "masscan": ["fast scan, speed scan, quick scan, port scan, network scan, scanning, mass scanning"],
        
        # WEB HACKING (CRITICAL!)
        "burpsuite": ["web test, web testing, web hacking, web pentest, web proxy, intercepting proxy, http proxy, https proxy, web security, web app, webapp, intercept, proxy"],
        "sqlmap": ["sql injection, sqli, sql inject, database hack, db hack, sql attack, inject sql, sql vuln, database attack, automated sql"],
        "nikto": ["web scan, website scan, web vulnerability, web vuln, web scanner, site scan, vulnerability scanner"],
        "dirb": ["directory, dir scan, directory brute force, dir bruteforce, hidden directories, find directories, web directories, directory enumeration"],
        "gobuster": ["directory, dir scan, brute force, bruteforce, enumeration, enum, hidden files, find directories, directory discovery, subdomain, vhost"],
        
        # EXPLOITATION (MUST HAVE!)
        "metasploit": ["exploit, exploiting, exploitation, framework, payload, shell, reverse shell, meterpreter, post exploitation, post-exploitation, msf, msfconsole"],
        "searchsploit": ["exploit, exploit search, find exploit, vulnerability, cve, exploit database, exploit-db"],
        
        # PASSWORD ATTACKS (TOP PRIORITY!)
        "hydra": ["brute force, bruteforce, brute-force, brute forcing, password attack, password crack, password cracking, login attack, credential attack, breaking passwords, crack login, crack password, dictionary attack, password guess, pw crack"],
        "john": ["password crack, password cracking, hash crack, hash cracking, crack hash, break password, john the ripper, jtr, password recovery, pw crack, hash breaking"],
        "hashcat": ["hash crack, hash cracking, password crack, password cracking, gpu crack, fast crack, crack hash, break hash, hash breaking, pw crack"],
        
        # WIRELESS (COMMON STUDENT INTEREST)
        "aircrack-ng": ["wifi hack, wifi crack, wireless hack, wireless crack, wpa crack, wep crack, wifi security, wireless security, crack wifi, break wifi"],
        
        # SNIFFING/MONITORING (IMPORTANT!)
        "wireshark": ["packet capture, packet sniffing, sniff, sniffer, network monitor, traffic analysis, pcap, packet analyzer, capture traffic, see traffic, network traffic"],
        "tcpdump": ["packet capture, sniff, sniffer, capture, network capture, traffic capture, dump traffic, capture packets"],
        
        # ENUMERATION (KEY CONCEPT!)
        "enum4linux": ["enumeration, enum, smb enum, windows enum, share enumeration, samba enum"],
        "dnsenum": ["dns, dns enumeration, dns enum, subdomain, subdomain enum, dns recon"],
        
        # EXPLOITATION FRAMEWORKS
        "beef": ["browser exploit, xss, browser hook, client side, web exploit"],
        
        # FILE TRANSFER
        "netcat": ["nc, swiss army knife, reverse shell, bind shell, file transfer, port forward, banner grab, listener, connect back"],
        
        # VULNERABILITY SCANNING
        "openvas": ["vulnerability scan, vuln scan, security scan, scan for vulns, find vulnerabilities"],
        
        # REVERSE ENGINEERING
        "gdb": ["debugger, debugging, reverse engineering, reversing, disassemble"],
        
        # FORENSICS
        "autopsy": ["forensics, digital forensics, disk analysis, file recovery, investigate"],
        "volatility": ["memory forensics, memory analysis, ram analysis, memory dump"],
        
        # WEB TOOLS
        "wpscan": ["wordpress, wp scan, wordpress scan, cms scan"],
        "whatweb": ["fingerprint, website fingerprint, identify cms, web fingerprint"],
        
        # INFORMATION GATHERING (RECON PHASE!)
        "whois": ["domain info, domain information, registration, owner, who owns, domain lookup, dns info"],
        "nslookup": ["dns, dns lookup, resolve, ip lookup, domain lookup"],
        "dig": ["dns, dns query, dns lookup, domain lookup, resolve"],
        "traceroute": ["route, path, trace, network path, hops, routing"],
        
        # MALWARE
        "msfvenom": ["payload, payload generation, reverse shell, meterpreter, generate payload, create payload, shellcode"],
        
        # SOCIAL ENGINEERING
        "setoolkit": ["social engineering, phishing, clone site, fake site, credential harvest"],
        
        # CRACKING TOOLS
        "crunch": ["wordlist, password list, generate wordlist, custom wordlist, dictionary"],
        "cewl": ["wordlist, web wordlist, scrape wordlist, generate wordlist from website"],
        
        # MISC SECURITY
        "socat": ["relay, forward, tunnel, port forward, reverse shell"],
        "proxychains": ["proxy, tunnel, anonymity, chain, route through proxy, hide ip"],
    }
    
    updated = 0
    skipped = 0
    
    for cmd_name, slang_list in slang_mappings.items():
        try:
            # Get current tags
            cursor.execute("SELECT tags FROM commands WHERE name = ?", (cmd_name,))
            result = cursor.fetchone()
            
            if not result:
                print(f"  - Skipped {cmd_name} (not in database)")
                skipped += 1
                continue
            
            current_tags = result[0] if result[0] else ""
            
            # Combine with new slang terms
            new_slang = ", ".join(slang_list)
            
            # Merge tags (avoid duplicates)
            if current_tags:
                combined = f"{current_tags}, {new_slang}"
            else:
                combined = new_slang
            
            # Update database
            cursor.execute("UPDATE commands SET tags = ? WHERE name = ?", (combined, cmd_name))
            print(f"  ✓ Enhanced {cmd_name}")
            updated += 1
            
        except sqlite3.Error as e:
            print(f"  ! Error updating {cmd_name}: {e}")
            skipped += 1
    
    try:
        conn.commit()
        print()
        print("=" * 70)
        print(f"✓ Enhancement Complete!")
        print("=" * 70)
        print()
        print(f"Updated: {updated} commands")
        print(f"Skipped: {skipped} commands")
        print()
        print("Students can now search by PURPOSE!")
        print()
        print("Try these searches:")
        print("  cb brute force      → Find password attack tools")
        print("  cb password crack   → Find hash/password crackers")
        print("  cb network scan     → Find nmap, masscan")
        print("  cb web hack         → Find burpsuite, sqlmap, nikto")
        print("  cb sniffing         → Find wireshark, tcpdump")
        print("  cb exploit          → Find metasploit, searchsploit")
        print()
    except sqlite3.Error as e:
        print(f"\nError committing changes: {e}")
        conn.rollback()
        sys.exit(1)
    finally:
        conn.close()

if __name__ == "__main__":
    try:
        enhance_slang_tags()
    except KeyboardInterrupt:
        print("\n\nCancelled by user")
        sys.exit(0)

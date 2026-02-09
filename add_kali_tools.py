#!/usr/bin/env python3
"""
Kali Tools Importer for CommandBrain
Pre-populated with essential Kali Linux security tools
"""

import sqlite3
import os
import sys

def get_db_path():
    return os.path.expanduser("~/.commandbrain.db")

def add_kali_tools():
    """Add essential Kali Linux tools to the database"""
    
    db_path = get_db_path()
    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}")
        print("Please run setup_commandbrain.py first to create the database.")
        sys.exit(1)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)
    
    kali_tools = [
        # Network Scanning
        ("nmap", "Network-Scanning", "Network exploration and security auditing tool",
         "nmap [options] [target]", 
         "nmap -sV 192.168.1.1\nnmap -sS -p 1-65535 target.com\nnmap -A -T4 192.168.1.0/24",
         "masscan, zmap, unicornscan",
         "The ULTIMATE network scanner. -sV = version detection, -sS = stealth SYN scan, -A = aggressive (OS detection, version, scripts), -T4 = faster timing. Can be LOUD - use carefully!",
         "network,scanning,reconnaissance,exam,essential"),
        
        ("masscan", "Network-Scanning", "Ultra-fast port scanner (scans entire internet in 6 minutes)",
         "masscan [targets] -p[ports]",
         "masscan 192.168.1.0/24 -p80,443\nmasscan 0.0.0.0/0 -p443 --rate 10000",
         "nmap, zmap",
         "INSANELY fast but less detailed than nmap. Can overwhelm networks. Good for initial recon of large ranges.",
         "network,scanning,fast,reconnaissance"),
        
        # Web Application Testing
        ("burpsuite", "Web-Testing", "Integrated platform for web application security testing",
         "burpsuite (GUI application)",
         "Launch from Kali menu or: burpsuite",
         "OWASP ZAP, mitmproxy, sqlmap",
         "Industry standard web proxy. Intercepts HTTP/HTTPS traffic. Use Repeater for testing, Intruder for fuzzing, Scanner for auto-testing. Community edition is free but limited.",
         "web,proxy,testing,exam,essential,gui"),
        
        ("sqlmap", "Web-Testing", "Automatic SQL injection and database takeover tool",
         "sqlmap -u [URL] [options]",
         "sqlmap -u 'http://site.com/page?id=1'\nsqlmap -u URL --dbs\nsqlmap -u URL -D database --tables\nsqlmap -u URL --os-shell",
         "havij, burpsuite, NoSQLMap",
         "Automates SQL injection attacks. --dbs lists databases, --tables shows tables, --os-shell tries to get command execution. VERY noisy - will show up in logs!",
         "web,sql-injection,database,exploitation,exam"),
        
        ("nikto", "Web-Testing", "Web server scanner for vulnerabilities and misconfigurations",
         "nikto -h [host]",
         "nikto -h http://target.com\nnikto -h 192.168.1.1 -p 80,443\nnikto -h target.com -Tuning 123bde",
         "wpscan, dirb, gobuster",
         "Checks for 6700+ dangerous files/programs. LOUD and SLOW. Good for finding low-hanging fruit. Not stealthy at all!",
         "web,scanning,vulnerabilities,reconnaissance"),
        
        ("dirb", "Web-Testing", "Web content scanner (directory brute-forcing)",
         "dirb [URL] [wordlist]",
         "dirb http://target.com\ndirb http://target.com /usr/share/wordlists/dirb/common.txt",
         "gobuster, dirbuster, ffuf",
         "Finds hidden directories and files. Uses wordlists to guess URLs. gobuster is faster, ffuf is more flexible.",
         "web,enumeration,brute-force,reconnaissance"),
        
        ("gobuster", "Web-Testing", "Fast directory/file & DNS brute-forcing tool",
         "gobuster [mode] [options]",
         "gobuster dir -u http://target.com -w wordlist.txt\ngobuster dns -d target.com -w wordlist.txt\ngobuster vhost -u http://target.com -w wordlist.txt",
         "dirb, ffuf, wfuzz",
         "MUCH faster than dirb. Written in Go. 'dir' mode for directories, 'dns' for subdomain enumeration, 'vhost' for virtual hosts. Great for CTFs!",
         "web,enumeration,brute-force,fast,exam"),
        
        # Exploitation
        ("metasploit", "Exploitation", "Penetration testing framework with exploits and payloads",
         "msfconsole",
         "msfconsole\nuse exploit/windows/smb/ms17_010_eternalblue\nset RHOST 192.168.1.10\nrun",
         "exploit-db, searchsploit, armitage",
         "The KING of exploit frameworks. msfconsole = command line, armitage = GUI. Contains 1000s of exploits, payloads, encoders. 'search' finds exploits, 'use' selects one, 'set' configures, 'run/exploit' launches.",
         "exploitation,framework,exam,essential,post-exploitation"),
        
        ("searchsploit", "Exploitation", "Searches Exploit-DB archive from command line",
         "searchsploit [term]",
         "searchsploit apache\nsearchsploit -m 12345\nsearchsploit --nmap nmap_scan.xml",
         "metasploit, exploit-db",
         "Offline search of exploit-db.com. -m mirrors exploit to current dir. Can parse nmap XML files to find exploits for discovered services!",
         "exploitation,search,research,exam"),
        
        # Password Attacks
        ("hydra", "Password-Attacks", "Fast network logon cracker (brute-force authentication)",
         "hydra [options] [target] [service]",
         "hydra -l admin -P passwords.txt ssh://192.168.1.1\nhydra -L users.txt -P pass.txt ftp://target.com\nhydra -l admin -P rockyou.txt 192.168.1.1 http-post-form '/login:user=^USER^&pass=^PASS^:F=failed'",
         "medusa, ncrack, patator",
         "Supports 50+ protocols. -l = single user, -L = user list, -p = single pass, -P = password list. http-post-form is tricky - study the syntax! Can be SLOW and LOUD.",
         "password,brute-force,authentication,exam"),
        
        ("john", "Password-Attacks", "John the Ripper - password cracking tool",
         "john [options] [file]",
         "john --wordlist=rockyou.txt hashes.txt\njohn --show hashes.txt\nunshadow /etc/passwd /etc/shadow > mypasswd.txt && john mypasswd.txt",
         "hashcat, hydra, medusa",
         "Cracks password hashes offline. Auto-detects hash types. --show displays cracked passwords. unshadow combines /etc/passwd and /etc/shadow for cracking. Hashcat is faster with GPU.",
         "password,hash-cracking,offline,exam"),
        
        ("hashcat", "Password-Attacks", "Advanced password recovery tool (GPU-accelerated)",
         "hashcat -m [hash_type] [hash_file] [wordlist]",
         "hashcat -m 0 hashes.txt rockyou.txt\nhashcat -m 1000 hashes.txt rockyou.txt\nhashcat -a 3 hash.txt ?a?a?a?a?a?a",
         "john, mdxfind",
         "FASTEST hash cracker (uses GPU). -m = hash type (0=MD5, 1000=NTLM, 1800=SHA512). -a = attack mode (0=dictionary, 3=brute-force). ?a=all chars, ?l=lowercase, ?d=digits. Can be slow on weak hardware!",
         "password,hash-cracking,gpu,fast,exam"),
        
        # Wireless
        ("aircrack-ng", "Wireless", "Suite of tools for WiFi network security testing",
         "airmon-ng, airodump-ng, aireplay-ng, aircrack-ng",
         "airmon-ng start wlan0\nairodump-ng wlan0mon\naireplay-ng -0 10 -a [BSSAP] wlan0mon\naircrack-ng -w wordlist.txt capture.cap",
         "wifite, reaver, fern-wifi-cracker",
         "4-step WiFi attack: 1) airmon-ng puts card in monitor mode 2) airodump-ng captures packets 3) aireplay-ng deauths clients (forces handshake) 4) aircrack-ng cracks WPA key. Needs compatible WiFi card!",
         "wireless,wifi,cracking,exam"),
        
        # Sniffing & Spoofing
        ("wireshark", "Sniffing", "Network protocol analyzer (packet sniffer)",
         "wireshark (GUI) or tshark (CLI)",
         "wireshark\ntshark -i eth0\ntshark -r capture.pcap -Y 'http.request.method==POST'",
         "tcpdump, ettercap, bettercap",
         "The KING of packet sniffers. Can decode 1000+ protocols. Use filters: http, tcp.port==80, ip.addr==192.168.1.1. tshark = CLI version. Essential for analyzing network traffic and CTF challenges!",
         "sniffing,network,analysis,exam,essential,gui"),
        
        ("tcpdump", "Sniffing", "Command-line packet analyzer",
         "tcpdump [options]",
         "tcpdump -i eth0\ntcpdump -i eth0 port 80\ntcpdump -i eth0 -w capture.pcap\ntcpdump -r capture.pcap",
         "wireshark, tshark",
         "Lightweight packet sniffer. -i = interface, -w = write to file, -r = read from file. Good for quick captures without GUI. Less detailed than Wireshark.",
         "sniffing,network,cli,lightweight"),
        
        ("ettercap", "Sniffing", "Suite for man-in-the-middle attacks on LANs",
         "ettercap [options]",
         "ettercap -T -M arp:remote /192.168.1.1// /192.168.1.5//\nettercap -G (GUI mode)",
         "bettercap, arpspoof, mitmproxy",
         "ARP poisoning for MITM attacks. Can sniff passwords, inject packets, modify traffic. -T = text mode, -G = GUI, -M = MITM mode. bettercap is the modern alternative.",
         "sniffing,mitm,arp-poisoning,dangerous"),
        
        # Information Gathering
        ("whois", "Information-Gathering", "Queries WHOIS database for domain registration info",
         "whois [domain]",
         "whois google.com\nwhois 8.8.8.8",
         "dig, nslookup, fierce",
         "Shows domain owner, registration date, nameservers. Good for recon. Some domains have privacy protection enabled.",
         "reconnaissance,osint,information-gathering,exam"),
        
        ("dnsenum", "Information-Gathering", "DNS enumeration tool (finds subdomains)",
         "dnsenum [domain]",
         "dnsenum target.com\ndnsenum --enum target.com",
         "dnsrecon, fierce, sublist3r",
         "Finds subdomains via brute-force and Google scraping. Can discover hidden servers. --enum does full enumeration.",
         "reconnaissance,dns,enumeration,subdomain"),
        
        ("theHarvester", "Information-Gathering", "OSINT tool for gathering emails, names, subdomains",
         "theHarvester -d [domain] -b [source]",
         "theHarvester -d target.com -b google\ntheHarvester -d target.com -b all",
         "recon-ng, maltego, spiderfoot",
         "Searches public sources (Google, Bing, Shodan, etc.) for email addresses, employee names, subdomains. Great for recon phase. -b = source (use 'all' to search everything).",
         "reconnaissance,osint,information-gathering,email,exam"),
        
        # Social Engineering
        ("setoolkit", "Social-Engineering", "Social Engineering Toolkit (phishing, payloads, attacks)",
         "setoolkit or se-toolkit",
         "setoolkit (then follow menu)",
         "gophish, king-phisher",
         "Creates phishing pages, malicious PDFs, infected USBs, etc. Menu-driven interface. Used for authorized social engineering tests ONLY. Very powerful but ethically sensitive!",
         "social-engineering,phishing,payload,exam,dangerous"),
        
        # Forensics
        ("binwalk", "Forensics", "Firmware analysis and file extraction tool",
         "binwalk [file]",
         "binwalk firmware.bin\nbinwalk -e firmware.bin\nbinwalk --dd='.*' firmware.bin",
         "foremost, strings, hexdump",
         "Extracts files embedded in firmware/images. Good for CTFs (steganography challenges). -e = extract files. Looks for file signatures in binary data.",
         "forensics,analysis,extraction,ctf,exam"),
        
        ("volatility", "Forensics", "Memory forensics framework",
         "volatility -f [memory_dump] --profile=[OS] [plugin]",
         "volatility -f memory.raw imageinfo\nvolatility -f memory.raw --profile=Win7SP1x64 pslist\nvolatility -f memory.raw --profile=Win7SP1x64 netscan",
         "rekall, redline",
         "Analyzes RAM dumps. imageinfo detects OS, pslist shows processes, netscan shows network connections. Essential for incident response! Need correct --profile or results are garbage.",
         "forensics,memory,incident-response,exam"),
    ]
    
    added = 0
    skipped = 0
    errors = 0
    
    print("\nAdding Kali Linux tools to CommandBrain...")
    print("=" * 60)
    
    for tool in kali_tools:
        try:
            cursor.execute("""
                INSERT INTO commands 
                (name, category, description, usage, examples, related_commands, notes, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, tool)
            added += 1
            print(f"✓ Added: {tool[0]}")
        except sqlite3.IntegrityError:
            skipped += 1
            print(f"- Skipped (exists): {tool[0]}")
        except sqlite3.Error as e:
            errors += 1
            print(f"! Error adding {tool[0]}: {e}")
    
    try:
        conn.commit()
    except sqlite3.Error as e:
        print(f"\nError committing changes: {e}")
        conn.rollback()
    finally:
        conn.close()
    
    print("=" * 60)
    print(f"\n✓ Import complete!")
    print(f"  Added: {added} tools")
    print(f"  Skipped: {skipped} tools (already existed)")
    if errors > 0:
        print(f"  Errors: {errors} tools failed")
    print(f"\nTry: ./commandbrain.py search -t category exploitation")
    print()

if __name__ == "__main__":
    try:
        add_kali_tools()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

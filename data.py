#!/usr/bin/env python3
"""
CommandBrain Data Module
All command definitions, workflow data, and search enhancements in one place.

Each command tuple follows this format:
  (name, category, description, usage, examples, related_commands, notes, tags)
"""

# ─────────────────────────────────────────────────────────────────────────────
# BASIC LINUX COMMANDS (30 essential commands)
# ─────────────────────────────────────────────────────────────────────────────

BASIC_COMMANDS = [
    # Basic File Operations
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

    # Searching
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


# ─────────────────────────────────────────────────────────────────────────────
# KALI LINUX SECURITY TOOLS (22 essential tools)
# ─────────────────────────────────────────────────────────────────────────────

KALI_TOOLS = [
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


# ─────────────────────────────────────────────────────────────────────────────
# SLANG / PURPOSE-BASED SEARCH TERMS
# Maps command names to student-friendly search terms that get appended to tags
# ─────────────────────────────────────────────────────────────────────────────

SLANG_MAPPINGS = {
    # BASIC COMMANDS
    "ls":        ["list, listing, show files, see files, what files, dir, directory, view files"],
    "cd":        ["change dir, go to, navigate, move to, switch folder, goto"],
    "pwd":       ["where am i, current location, current directory, print directory, path"],
    "mkdir":     ["make folder, create folder, new folder, make directory, new dir"],
    "rm":        ["delete, remove, erase, del, destroy, delete file, remove file"],
    "cp":        ["copy, duplicate, backup, clone"],
    "mv":        ["move, rename, relocate, transfer"],
    "cat":       ["read, view, show, display, print, see file, open file"],
    "grep":      ["search, find text, search text, find in file, pattern search, filter, regex, regular expression"],
    "find":      ["search files, locate, find file, file search, where is, locate file"],

    # PERMISSIONS
    "chmod":     ["permissions, change permissions, file permissions, access, rights, executable, make executable"],
    "chown":     ["owner, ownership, change owner, file owner"],

    # SYSTEM INFO
    "top":       ["processes, cpu, memory, performance, running, tasks, resource usage, what's running"],
    "ps":        ["processes, running, tasks, process list, show processes"],
    "df":        ["disk, disk space, storage, free space, how much space, disk usage"],

    # NETWORKING
    "ping":      ["test connection, check connection, reachability, alive, test network, can i reach, connectivity, test ping"],
    "ifconfig":  ["ip address, my ip, network config, interface, network card, nic"],
    "ip":        ["ip address, my ip, network, routing, interface, network config"],
    "netstat":   ["connections, ports, network connections, listening, open ports, network status"],
    "ss":        ["sockets, connections, ports, listening, open ports, network"],

    # USER MANAGEMENT
    "sudo":      ["root, admin, administrator, superuser, privilege, elevated, run as admin, permission"],
    "passwd":    ["password, change password, set password, pw, reset password"],

    # PACKAGES
    "apt":       ["install, software, package, program, application, update, upgrade"],

    # SYSTEM CONTROL
    "systemctl": ["service, daemon, start, stop, restart, enable, disable"],
    "shutdown":  ["reboot, restart, power off, turn off, halt"],

    # TEXT PROCESSING
    "awk":       ["text processing, columns, fields, parse, extract"],
    "sed":       ["replace, substitute, edit, text edit, find replace, stream editor"],

    # ARCHIVING
    "tar":       ["compress, archive, zip, extract, unzip, backup, package"],

    # SECURITY
    "ssh":       ["remote, remote login, secure shell, connect, remote access, login remotely"],
    "scp":       ["copy, transfer, file transfer, secure copy, send file, remote copy"],

    # KALI: NETWORK SCANNING
    "nmap":      ["scan, scanning, port scan, network scan, reconnaissance, recon, enum, enumeration, discovery, find hosts, find ports, service detection, port scanner, network scanner, probe"],
    "masscan":   ["fast scan, speed scan, quick scan, port scan, network scan, scanning, mass scanning"],

    # KALI: WEB HACKING
    "burpsuite": ["web test, web testing, web hacking, web pentest, web proxy, intercepting proxy, http proxy, https proxy, web security, web app, webapp, intercept, proxy"],
    "sqlmap":    ["sql injection, sqli, sql inject, database hack, db hack, sql attack, inject sql, sql vuln, database attack, automated sql"],
    "nikto":     ["web scan, website scan, web vulnerability, web vuln, web scanner, site scan, vulnerability scanner"],
    "dirb":      ["directory, dir scan, directory brute force, dir bruteforce, hidden directories, find directories, web directories, directory enumeration"],
    "gobuster":  ["directory, dir scan, brute force, bruteforce, enumeration, enum, hidden files, find directories, directory discovery, subdomain, vhost"],

    # KALI: EXPLOITATION
    "metasploit":   ["exploit, exploiting, exploitation, framework, payload, shell, reverse shell, meterpreter, post exploitation, post-exploitation, msf, msfconsole"],
    "searchsploit": ["exploit, exploit search, find exploit, vulnerability, cve, exploit database, exploit-db"],

    # KALI: PASSWORD ATTACKS
    "hydra":     ["brute force, bruteforce, brute-force, brute forcing, password attack, password crack, password cracking, login attack, credential attack, breaking passwords, crack login, crack password, dictionary attack, password guess, pw crack"],
    "john":      ["password crack, password cracking, hash crack, hash cracking, crack hash, break password, john the ripper, jtr, password recovery, pw crack, hash breaking"],
    "hashcat":   ["hash crack, hash cracking, password crack, password cracking, gpu crack, fast crack, crack hash, break hash, hash breaking, pw crack"],

    # KALI: WIRELESS
    "aircrack-ng": ["wifi hack, wifi crack, wireless hack, wireless crack, wpa crack, wep crack, wifi security, wireless security, crack wifi, break wifi"],

    # KALI: SNIFFING
    "wireshark": ["packet capture, packet sniffing, sniff, sniffer, network monitor, traffic analysis, pcap, packet analyzer, capture traffic, see traffic, network traffic"],
    "tcpdump":   ["packet capture, sniff, sniffer, capture, network capture, traffic capture, dump traffic, capture packets"],
    "ettercap":  ["man in the middle, mitm, arp poison, arp poisoning, sniff passwords, intercept traffic"],

    # KALI: INFO GATHERING
    "whois":       ["domain info, domain information, registration, owner, who owns, domain lookup, dns info"],
    "dnsenum":     ["dns, dns enumeration, dns enum, subdomain, subdomain enum, dns recon"],
    "theHarvester": ["email harvest, osint, open source intelligence, email gathering, recon"],
    "setoolkit":   ["social engineering, phishing, clone site, fake site, credential harvest"],

    # KALI: FORENSICS
    "binwalk":     ["firmware, extract, embedded, steganography, stego, ctf"],
    "volatility":  ["memory forensics, memory analysis, ram analysis, memory dump"],
}


# ─────────────────────────────────────────────────────────────────────────────
# PENETRATION TESTING WORKFLOWS
# Step-by-step command chains that teach methodology, not just tools
# ─────────────────────────────────────────────────────────────────────────────

WORKFLOWS = {
    "web-pentest": {
        "name": "Web Application Penetration Testing",
        "description": "Complete workflow for testing web application security",
        "difficulty": "Intermediate",
        "steps": [
            {"number": 1, "title": "Reconnaissance - Domain Information",
             "command": "whois target.com",
             "purpose": "Gather domain registration info, name servers, and contact details",
             "look_for": ["Registration date (newer domains = potentially less secure)",
                          "Name servers and DNS provider", "Admin contact information", "Expiration date"],
             "tips": "Save this info - it's useful for social engineering later"},
            {"number": 2, "title": "DNS Enumeration",
             "command": "nslookup target.com\ndig target.com ANY",
             "purpose": "Find all DNS records - subdomains, mail servers, etc.",
             "look_for": ["A records (IP addresses)", "MX records (mail servers - often vulnerable)",
                          "TXT records (may reveal tech stack)", "Subdomains (dev.target.com, admin.target.com)"],
             "tips": "Subdomains are often less secure than main site"},
            {"number": 3, "title": "Port Scanning - Service Discovery",
             "command": "nmap -sV -p- target.com",
             "purpose": "Find ALL open ports and identify running services",
             "look_for": ["Web ports: 80 (HTTP), 443 (HTTPS), 8080, 8443",
                          "Admin panels: 8000, 9000, 3000",
                          "Database ports: 3306 (MySQL), 5432 (PostgreSQL), 27017 (MongoDB)",
                          "FTP, SSH, SMB for lateral movement later"],
             "tips": "Use -p- to scan ALL 65535 ports, not just common ones"},
            {"number": 4, "title": "Web Vulnerability Scanning",
             "command": "nikto -h http://target.com",
             "purpose": "Automated detection of common web vulnerabilities",
             "look_for": ["Outdated software versions (check for CVEs)",
                          "Misconfigurations (directory listings, debug mode)",
                          "Dangerous HTTP methods (PUT, DELETE enabled)",
                          "Known vulnerable paths and files"],
             "tips": "Nikto is NOISY - use only when you don't care about detection"},
            {"number": 5, "title": "Directory & File Enumeration",
             "command": "dirb http://target.com /usr/share/wordlists/dirb/common.txt",
             "purpose": "Find hidden directories, admin panels, and backup files",
             "look_for": ["/admin, /administrator, /wp-admin (admin panels)",
                          "/backup, /.git, /config (sensitive data)",
                          "/api, /v1, /swagger (API endpoints)",
                          ".bak, .old, .zip files (backups with source code)"],
             "tips": "Alternative: Use gobuster for faster scanning"},
            {"number": 6, "title": "Technology Fingerprinting",
             "command": "whatweb http://target.com",
             "purpose": "Identify web technologies, frameworks, and versions",
             "look_for": ["CMS (WordPress, Joomla, Drupal - check for known exploits)",
                          "Web servers (Apache, Nginx - version vulnerabilities)",
                          "Programming languages (PHP, Python, ASP.NET)",
                          "JavaScript frameworks (React, Angular, Vue)"],
             "tips": "Match versions to CVE databases like exploit-db"},
            {"number": 7, "title": "SQL Injection Testing",
             "command": 'sqlmap -u "http://target.com/page?id=1" --batch --dbs',
             "purpose": "Test for SQL injection vulnerabilities in URL parameters",
             "look_for": ["Successful injection (shows database names)",
                          "Database type (MySQL, PostgreSQL, MSSQL)",
                          "Error messages revealing structure",
                          "Number of injectable parameters"],
             "tips": "If found, use --dump to extract data, but check legality first!"},
            {"number": 8, "title": "Cross-Site Scripting (XSS) Testing",
             "command": "# Manual testing - inject: <script>alert('XSS')</script>\n# In search boxes, comment fields, URL parameters",
             "purpose": "Test if user input is properly sanitized",
             "look_for": ["Alert box appears (reflected XSS)",
                          "Payload executes after page reload (stored XSS)",
                          "DOM manipulation (DOM-based XSS)",
                          "Input validation weaknesses"],
             "tips": "Try different payloads - filters may block simple attempts"},
            {"number": 9, "title": "Authentication Testing",
             "command": 'hydra -L users.txt -P passwords.txt target.com http-post-form "/login:user=^USER^&pass=^PASS^:F=failed"',
             "purpose": "Test for weak passwords and brute-force vulnerabilities",
             "look_for": ["Successful login attempts", "No rate limiting (unlimited attempts)",
                          "Predictable session tokens", "Default credentials (admin/admin)"],
             "tips": "Check for account lockout - don't lock out real users!"},
            {"number": 10, "title": "Document Findings",
             "command": "# Create a report with:\n# - Executive summary\n# - Vulnerability details\n# - Proof of concept\n# - Remediation steps",
             "purpose": "Professional documentation of discovered vulnerabilities",
             "look_for": ["CVSS scores for each vulnerability", "Screenshots/evidence of issues",
                          "Steps to reproduce", "Business impact assessment"],
             "tips": "Clear documentation = clients take action = you get paid!"},
        ]
    },

    "network-recon": {
        "name": "Network Reconnaissance",
        "description": "Discover and map network hosts, services, and vulnerabilities",
        "difficulty": "Beginner",
        "steps": [
            {"number": 1, "title": "Host Discovery - Find Live Hosts",
             "command": "nmap -sn 192.168.1.0/24",
             "purpose": "Discover which hosts are online in the network",
             "look_for": ["Number of live hosts", "IP addresses and hostnames",
                          "MAC addresses (for OS fingerprinting)", "Response times (network topology clues)"],
             "tips": "-sn = ping scan only, no port scanning yet (fast and stealthy)"},
            {"number": 2, "title": "Port Scanning - Quick Scan",
             "command": "nmap -F <target-ip>",
             "purpose": "Fast scan of the 100 most common ports",
             "look_for": ["Open ports on target", "Filtered ports (firewall present)",
                          "Common services (SSH, HTTP, SMB, RDP)", "Unusual high ports"],
             "tips": "-F scans top 100 ports. Use -p- for all 65535 ports (slower)"},
            {"number": 3, "title": "Service Version Detection",
             "command": "nmap -sV <target-ip>",
             "purpose": "Identify exact versions of running services",
             "look_for": ["Service names and versions", "Operating system clues",
                          "Outdated software (check for CVEs)", "Banner information"],
             "tips": "Versions = exploit opportunities. Always match to CVE databases"},
            {"number": 4, "title": "OS Fingerprinting",
             "command": "nmap -O <target-ip>",
             "purpose": "Detect target operating system",
             "look_for": ["OS type (Windows, Linux, macOS)", "OS version",
                          "Confidence percentage", "Device type (router, printer, server)"],
             "tips": "Requires root/admin privileges. Use with -sV for best results"},
            {"number": 5, "title": "Vulnerability Scanning",
             "command": "nmap --script vuln <target-ip>",
             "purpose": "Check for known vulnerabilities using NSE scripts",
             "look_for": ["CVE numbers and descriptions", "Severity ratings (Critical, High, Medium)",
                          "Exploit availability", "Patch status"],
             "tips": "This is NOISY - defender will see this. Use carefully"},
            {"number": 6, "title": "SMB Enumeration (Windows Networks)",
             "command": "nmap --script smb-os-discovery <target-ip>",
             "purpose": "Gather information from Windows SMB shares",
             "look_for": ["Computer name and domain", "Workgroup information",
                          "OS version details", "System time (for time-based attacks)"],
             "tips": "SMB is a goldmine for Windows network enumeration"},
            {"number": 7, "title": "Save Results",
             "command": "nmap -sV -oA scan_results <target-ip>",
             "purpose": "Export scan results in multiple formats",
             "look_for": [".nmap file (human readable)", ".xml file (for tools like Metasploit)",
                          ".gnmap file (grep-friendly)"],
             "tips": "Always save scans! You'll reference them throughout the test"},
        ]
    },

    "password-attack": {
        "name": "Password Attack Workflow",
        "description": "Crack passwords using various techniques",
        "difficulty": "Beginner",
        "steps": [
            {"number": 1, "title": "Identify Authentication Mechanism",
             "command": "nmap -p 22,21,3389,445 <target-ip>",
             "purpose": "Find services that use password authentication",
             "look_for": ["SSH (port 22)", "FTP (port 21)", "RDP (port 3389)", "SMB (port 445)"],
             "tips": "Each service needs different attack tools"},
            {"number": 2, "title": "Username Enumeration",
             "command": "# For SSH: check if user exists by timing\n# For web: look for 'user not found' vs 'wrong password'",
             "purpose": "Identify valid usernames before password attacks",
             "look_for": ["Error message differences", "Response time variations",
                          "Default admin accounts (admin, root, administrator)", "User lists from OSINT"],
             "tips": "Try common usernames: admin, root, user, test, guest"},
            {"number": 3, "title": "Online Brute Force - SSH",
             "command": "hydra -l root -P /usr/share/wordlists/rockyou.txt ssh://<target-ip>",
             "purpose": "Attempt to crack SSH password using wordlist",
             "look_for": ["Successful login credentials", "Account lockout (stop immediately!)",
                          "Rate limiting responses", "Connection throttling"],
             "tips": "SLOW down attacks to avoid detection: -t 4 limits threads"},
            {"number": 4, "title": "Hash Capture",
             "command": "# If you have system access:\n# Linux: cat /etc/shadow\n# Windows: mimikatz or secretsdump.py",
             "purpose": "Extract password hashes for offline cracking",
             "look_for": ["Hash format (MD5, SHA, NTLM)", "Salt presence",
                          "Number of user accounts", "Hash file permissions"],
             "tips": "Offline cracking = faster and stealthier than online attacks"},
            {"number": 5, "title": "Hash Identification",
             "command": "hashid <hash>\nhash-identifier",
             "purpose": "Determine hash type before cracking",
             "look_for": ["Hash algorithm name", "Hashcat mode number", "John format", "Salt indication"],
             "tips": "Wrong hash type = wasted cracking time. Identify first!"},
            {"number": 6, "title": "Offline Cracking - John the Ripper",
             "command": "john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt",
             "purpose": "Crack extracted hashes using wordlist",
             "look_for": ["Cracked passwords in john.pot", "Cracking speed (passwords/second)",
                          "Progress percentage", "Estimated completion time"],
             "tips": "Show cracked: john --show hashes.txt"},
            {"number": 7, "title": "Offline Cracking - Hashcat (GPU)",
             "command": "hashcat -m 1000 -a 0 hashes.txt /usr/share/wordlists/rockyou.txt",
             "purpose": "GPU-accelerated password cracking (much faster)",
             "look_for": ["Hash type mode (-m value)", "Cracking speed (GH/s with GPU)",
                          "Recovered passwords", "GPU temperature (don't melt your card!)"],
             "tips": "Hashcat is WAY faster than John if you have a GPU"},
            {"number": 8, "title": "Rule-Based Attacks",
             "command": "john --wordlist=words.txt --rules hashes.txt",
             "purpose": "Apply mutations to wordlist (Password -> P@ssw0rd!)",
             "look_for": ["Additional cracked passwords", "Common password patterns",
                          "Complexity requirements hints", "Password policy clues"],
             "tips": "Rules catch passwords that aren't directly in wordlists"},
        ]
    },

    "wireless-pentest": {
        "name": "Wireless Network Penetration Testing",
        "description": "Attack and secure wireless networks (WPA/WPA2)",
        "difficulty": "Intermediate",
        "steps": [
            {"number": 1, "title": "Enable Monitor Mode",
             "command": "airmon-ng start wlan0",
             "purpose": "Put wireless card into monitor mode to capture packets",
             "look_for": ["Monitor interface name (usually wlan0mon)", "No interfering processes",
                          "Chipset compatibility confirmed", "Success message"],
             "tips": "Kill interfering processes: airmon-ng check kill"},
            {"number": 2, "title": "Discover Wireless Networks",
             "command": "airodump-ng wlan0mon",
             "purpose": "Scan for nearby wireless networks and clients",
             "look_for": ["BSSID (router MAC address)", "Channel number",
                          "Encryption type (WPA/WPA2/WEP)", "Signal strength (PWR)",
                          "Connected clients (STATION)"],
             "tips": "Press Ctrl+C to stop scanning once you find your target"},
            {"number": 3, "title": "Capture Handshake",
             "command": "airodump-ng -c <channel> --bssid <BSSID> -w capture wlan0mon",
             "purpose": "Capture WPA handshake when client connects",
             "look_for": ["'WPA handshake' message in top right", "Connected clients (need at least one)",
                          "Data packets increasing", "Capture file being written"],
             "tips": "No clients? Deauth attack forces reconnection (see next step)"},
            {"number": 4, "title": "Deauthentication Attack (Force Handshake)",
             "command": "aireplay-ng --deauth 10 -a <BSSID> wlan0mon",
             "purpose": "Kick clients off network to capture handshake on reconnect",
             "look_for": ["ACKs received (deauth packets sent successfully)",
                          "Client disconnects on airodump-ng",
                          "Client reconnects (handshake captured)",
                          "WPA handshake message appearing"],
             "tips": "This is ILLEGAL on networks you don't own. Lab use only!"},
            {"number": 5, "title": "Crack WPA Password",
             "command": "aircrack-ng -w /usr/share/wordlists/rockyou.txt -b <BSSID> capture*.cap",
             "purpose": "Crack WPA password using captured handshake",
             "look_for": ["Handshake validation (must be present)", "Keys tested per second",
                          "KEY FOUND! message with password", "Progress indication"],
             "tips": "No match? Try bigger wordlist or use hashcat (faster)"},
            {"number": 6, "title": "Alternative: Hashcat Cracking",
             "command": "# Convert first:\nhccapx capture.cap converted.hccapx\n# Then crack:\nhashcat -m 2500 converted.hccapx wordlist.txt",
             "purpose": "GPU-accelerated WPA cracking (much faster than aircrack)",
             "look_for": ["Conversion success", "GPU utilization",
                          "Cracking speed (hashes/sec)", "Recovered passphrase"],
             "tips": "Hashcat can be 100x faster with a good GPU"},
        ]
    },

    "post-exploitation": {
        "name": "Post-Exploitation & Privilege Escalation",
        "description": "What to do after gaining initial access to a system",
        "difficulty": "Advanced",
        "steps": [
            {"number": 1, "title": "Establish Persistent Access",
             "command": "# Create reverse shell that survives reboot\n# Linux: Add to crontab\n# Windows: Create scheduled task",
             "purpose": "Ensure you can get back in even if session dies",
             "look_for": ["Cron job or scheduled task created", "Backdoor service running",
                          "SSH key added to authorized_keys", "Persistence mechanism hidden"],
             "tips": "Be stealthy - defenders check common persistence locations"},
            {"number": 2, "title": "Gather System Information",
             "command": "# Linux: uname -a, cat /etc/*release\n# Windows: systeminfo",
             "purpose": "Understand what system you've compromised",
             "look_for": ["OS version and architecture", "Kernel version (Linux privilege escalation)",
                          "Installed patches", "System role (workstation, server, domain controller)"],
             "tips": "Outdated kernel = likely privilege escalation path"},
            {"number": 3, "title": "Enumerate Users",
             "command": "# Linux: cat /etc/passwd, w, last\n# Windows: net user, net localgroup administrators",
             "purpose": "Find other user accounts and admin users",
             "look_for": ["Admin/root accounts", "Currently logged-in users",
                          "Recently logged-in users", "Service accounts"],
             "tips": "Target admin users for credential theft or lateral movement"},
            {"number": 4, "title": "Check Privileges",
             "command": "# Linux: sudo -l, id\n# Windows: whoami /priv, whoami /groups",
             "purpose": "See what commands you can run with elevated privileges",
             "look_for": ["NOPASSWD sudo entries (instant privilege escalation)",
                          "Dangerous permissions (SeDebugPrivilege, SeImpersonate)",
                          "Group memberships", "Capabilities"],
             "tips": "sudo -l often reveals privilege escalation paths"},
            {"number": 5, "title": "Find SUID/SGID Files (Linux)",
             "command": "find / -perm -4000 -type f 2>/dev/null",
             "purpose": "Find files that run with owner's privileges",
             "look_for": ["Unusual SUID binaries", "Custom applications with SUID",
                          "Known vulnerable SUID programs", "World-writable SUID files"],
             "tips": "Check GTFOBins for privilege escalation techniques"},
            {"number": 6, "title": "Search for Credentials",
             "command": "# Look for:\n# - Configuration files (.conf, .config)\n# - History files (.bash_history, .mysql_history)\n# - Notes (notes.txt, passwords.txt)\n# - Database connection strings",
             "purpose": "Find hardcoded passwords and credentials",
             "look_for": ["Database passwords in config files", "API keys and tokens",
                          "SSH private keys", "Browser saved passwords"],
             "tips": "Developers often hardcode credentials - check config files!"},
            {"number": 7, "title": "Network Enumeration",
             "command": "# Linux: ifconfig, netstat -antlp, arp -a\n# Windows: ipconfig /all, netstat -ano",
             "purpose": "Map internal network and find other hosts",
             "look_for": ["Additional network interfaces", "Internal IP ranges",
                          "Listening services", "Established connections"],
             "tips": "Multi-homed hosts = pivot points to other networks"},
            {"number": 8, "title": "Escalate Privileges",
             "command": "# Use tools like:\n# Linux: LinPEAS, linuxprivchecker\n# Windows: WinPEAS, PowerUp, Sherlock",
             "purpose": "Gain root/SYSTEM privileges",
             "look_for": ["Kernel exploits", "Misconfigurations",
                          "Weak service permissions", "DLL hijacking opportunities"],
             "tips": "Automated tools find 90% of privesc vectors instantly"},
        ]
    },
}

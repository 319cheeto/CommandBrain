#!/usr/bin/env python3
"""
Workflow/Command Chain data for CommandBrain
Shows students complete penetration testing workflows step-by-step
"""

# Workflow structure: Each workflow has steps with commands, explanations, and what to look for
WORKFLOWS = {
    "web-pentest": {
        "name": "Web Application Penetration Testing",
        "description": "Complete workflow for testing web application security",
        "difficulty": "Intermediate",
        "steps": [
            {
                "number": 1,
                "title": "Reconnaissance - Domain Information",
                "command": "whois target.com",
                "purpose": "Gather domain registration info, name servers, and contact details",
                "look_for": [
                    "Registration date (newer domains = potentially less secure)",
                    "Name servers and DNS provider",
                    "Admin contact information",
                    "Expiration date"
                ],
                "tips": "Save this info - it's useful for social engineering later"
            },
            {
                "number": 2,
                "title": "DNS Enumeration",
                "command": "nslookup target.com\ndig target.com ANY",
                "purpose": "Find all DNS records - subdomains, mail servers, etc.",
                "look_for": [
                    "A records (IP addresses)",
                    "MX records (mail servers - often vulnerable)",
                    "TXT records (may reveal tech stack)",
                    "Subdomains (dev.target.com, admin.target.com)"
                ],
                "tips": "Subdomains are often less secure than main site"
            },
            {
                "number": 3,
                "title": "Port Scanning - Service Discovery",
                "command": "nmap -sV -p- target.com",
                "purpose": "Find ALL open ports and identify running services",
                "look_for": [
                    "Web ports: 80 (HTTP), 443 (HTTPS), 8080, 8443",
                    "Admin panels: 8000, 9000, 3000",
                    "Database ports: 3306 (MySQL), 5432 (PostgreSQL), 27017 (MongoDB)",
                    "FTP, SSH, SMB for lateral movement later"
                ],
                "tips": "Use -p- to scan ALL 65535 ports, not just common ones"
            },
            {
                "number": 4,
                "title": "Web Vulnerability Scanning",
                "command": "nikto -h http://target.com",
                "purpose": "Automated detection of common web vulnerabilities",
                "look_for": [
                    "Outdated software versions (check for CVEs)",
                    "Misconfigurations (directory listings, debug mode)",
                    "Dangerous HTTP methods (PUT, DELETE enabled)",
                    "Known vulnerable paths and files"
                ],
                "tips": "Nikto is NOISY - use only when you don't care about detection"
            },
            {
                "number": 5,
                "title": "Directory & File Enumeration",
                "command": "dirb http://target.com /usr/share/wordlists/dirb/common.txt",
                "purpose": "Find hidden directories, admin panels, and backup files",
                "look_for": [
                    "/admin, /administrator, /wp-admin (admin panels)",
                    "/backup, /.git, /config (sensitive data)",
                    "/api, /v1, /swagger (API endpoints)",
                    ".bak, .old, .zip files (backups with source code)"
                ],
                "tips": "Alternative: Use gobuster for faster scanning"
            },
            {
                "number": 6,
                "title": "Technology Fingerprinting",
                "command": "whatweb http://target.com",
                "purpose": "Identify web technologies, frameworks, and versions",
                "look_for": [
                    "CMS (WordPress, Joomla, Drupal - check for known exploits)",
                    "Web servers (Apache, Nginx - version vulnerabilities)",
                    "Programming languages (PHP, Python, ASP.NET)",
                    "JavaScript frameworks (React, Angular, Vue)"
                ],
                "tips": "Match versions to CVE databases like exploit-db"
            },
            {
                "number": 7,
                "title": "SQL Injection Testing",
                "command": "sqlmap -u \"http://target.com/page?id=1\" --batch --dbs",
                "purpose": "Test for SQL injection vulnerabilities in URL parameters",
                "look_for": [
                    "Successful injection (shows database names)",
                    "Database type (MySQL, PostgreSQL, MSSQL)",
                    "Error messages revealing structure",
                    "Number of injectable parameters"
                ],
                "tips": "If found, use --dump to extract data, but check legality first!"
            },
            {
                "number": 8,
                "title": "Cross-Site Scripting (XSS) Testing",
                "command": "# Manual testing - inject: <script>alert('XSS')</script>\n# In search boxes, comment fields, URL parameters",
                "purpose": "Test if user input is properly sanitized",
                "look_for": [
                    "Alert box appears (reflected XSS)",
                    "Payload executes after page reload (stored XSS)",
                    "DOM manipulation (DOM-based XSS)",
                    "Input validation weaknesses"
                ],
                "tips": "Try different payloads - filters may block simple attempts"
            },
            {
                "number": 9,
                "title": "Authentication Testing",
                "command": "hydra -L users.txt -P passwords.txt target.com http-post-form \"/login:user=^USER^&pass=^PASS^:F=failed\"",
                "purpose": "Test for weak passwords and brute-force vulnerabilities",
                "look_for": [
                    "Successful login attempts",
                    "No rate limiting (unlimited attempts)",
                    "Predictable session tokens",
                    "Default credentials (admin/admin)"
                ],
                "tips": "Check for account lockout - don't lock out real users!"
            },
            {
                "number": 10,
                "title": "Document Findings",
                "command": "# Create a report with:\n# - Executive summary\n# - Vulnerability details\n# - Proof of concept\n# - Remediation steps",
                "purpose": "Professional documentation of discovered vulnerabilities",
                "look_for": [
                    "CVSS scores for each vulnerability",
                    "Screenshots/evidence of issues",
                    "Steps to reproduce",
                    "Business impact assessment"
                ],
                "tips": "Clear documentation = clients take action = you get paid!"
            }
        ]
    },

    "network-recon": {
        "name": "Network Reconnaissance",
        "description": "Discover and map network hosts, services, and vulnerabilities",
        "difficulty": "Beginner",
        "steps": [
            {
                "number": 1,
                "title": "Host Discovery - Find Live Hosts",
                "command": "nmap -sn 192.168.1.0/24",
                "purpose": "Discover which hosts are online in the network",
                "look_for": [
                    "Number of live hosts",
                    "IP addresses and hostnames",
                    "MAC addresses (for OS fingerprinting)",
                    "Response times (network topology clues)"
                ],
                "tips": "-sn = ping scan only, no port scanning yet (fast and stealthy)"
            },
            {
                "number": 2,
                "title": "Port Scanning - Quick Scan",
                "command": "nmap -F <target-ip>",
                "purpose": "Fast scan of the 100 most common ports",
                "look_for": [
                    "Open ports on target",
                    "Filtered ports (firewall present)",
                    "Common services (SSH, HTTP, SMB, RDP)",
                    "Unusual high ports"
                ],
                "tips": "-F scans top 100 ports. Use -p- for all 65535 ports (slower)"
            },
            {
                "number": 3,
                "title": "Service Version Detection",
                "command": "nmap -sV <target-ip>",
                "purpose": "Identify exact versions of running services",
                "look_for": [
                    "Service names and versions",
                    "Operating system clues",
                    "Outdated software (check for CVEs)",
                    "Banner information"
                ],
                "tips": "Versions = exploit opportunities. Always match to CVE databases"
            },
            {
                "number": 4,
                "title": "OS Fingerprinting",
                "command": "nmap -O <target-ip>",
                "purpose": "Detect target operating system",
                "look_for": [
                    "OS type (Windows, Linux, macOS)",
                    "OS version",
                    "Confidence percentage",
                    "Device type (router, printer, server)"
                ],
                "tips": "Requires root/admin privileges. Use with -sV for best results"
            },
            {
                "number": 5,
                "title": "Vulnerability Scanning",
                "command": "nmap --script vuln <target-ip>",
                "purpose": "Check for known vulnerabilities using NSE scripts",
                "look_for": [
                    "CVE numbers and descriptions",
                    "Severity ratings (Critical, High, Medium)",
                    "Exploit availability",
                    "Patch status"
                ],
                "tips": "This is NOISY - defender will see this. Use carefully"
            },
            {
                "number": 6,
                "title": "SMB Enumeration (Windows Networks)",
                "command": "nmap --script smb-os-discovery <target-ip>",
                "purpose": "Gather information from Windows SMB shares",
                "look_for": [
                    "Computer name and domain",
                    "Workgroup information",
                    "OS version details",
                    "System time (for time-based attacks)"
                ],
                "tips": "SMB is a goldmine for Windows network enumeration"
            },
            {
                "number": 7,
                "title": "Save Results",
                "command": "nmap -sV -oA scan_results <target-ip>",
                "purpose": "Export scan results in multiple formats",
                "look_for": [
                    ".nmap file (human readable)",
                    ".xml file (for tools like Metasploit)",
                    ".gnmap file (grep-friendly)"
                ],
                "tips": "Always save scans! You'll reference them throughout the test"
            }
        ]
    },

    "password-attack": {
        "name": "Password Attack Workflow",
        "description": "Crack passwords using various techniques",
        "difficulty": "Beginner",
        "steps": [
            {
                "number": 1,
                "title": "Identify Authentication Mechanism",
                "command": "nmap -p 22,21,3389,445 <target-ip>",
                "purpose": "Find services that use password authentication",
                "look_for": [
                    "SSH (port 22)",
                    "FTP (port 21)",
                    "RDP (port 3389)",
                    "SMB (port 445)"
                ],
                "tips": "Each service needs different attack tools"
            },
            {
                "number": 2,
                "title": "Username Enumeration",
                "command": "# For SSH: check if user exists by timing\n# For web: look for 'user not found' vs 'wrong password'",
                "purpose": "Identify valid usernames before password attacks",
                "look_for": [
                    "Error message differences",
                    "Response time variations",
                    "Default admin accounts (admin, root, administrator)",
                    "User lists from OSINT"
                ],
                "tips": "Try common usernames: admin, root, user, test, guest"
            },
            {
                "number": 3,
                "title": "Online Brute Force - SSH",
                "command": "hydra -l root -P /usr/share/wordlists/rockyou.txt ssh://<target-ip>",
                "purpose": "Attempt to crack SSH password using wordlist",
                "look_for": [
                    "Successful login credentials",
                    "Account lockout (stop immediately!)",
                    "Rate limiting responses",
                    "Connection throttling"
                ],
                "tips": "SLOW down attacks to avoid detection: -t 4 limits threads"
            },
            {
                "number": 4,
                "title": "Hash Capture",
                "command": "# If you have system access:\n# Linux: cat /etc/shadow\n# Windows: mimikatz or secretsdump.py",
                "purpose": "Extract password hashes for offline cracking",
                "look_for": [
                    "Hash format (MD5, SHA, NTLM)",
                    "Salt presence",
                    "Number of user accounts",
                    "Hash file permissions"
                ],
                "tips": "Offline cracking = faster and stealthier than online attacks"
            },
            {
                "number": 5,
                "title": "Hash Identification",
                "command": "hashid <hash>\nhash-identifier",
                "purpose": "Determine hash type before cracking",
                "look_for": [
                    "Hash algorithm name",
                    "Hashcat mode number",
                    "John format",
                    "Salt indication"
                ],
                "tips": "Wrong hash type = wasted cracking time. Identify first!"
            },
            {
                "number": 6,
                "title": "Offline Cracking - John the Ripper",
                "command": "john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt",
                "purpose": "Crack extracted hashes using wordlist",
                "look_for": [
                    "Cracked passwords in john.pot",
                    "Cracking speed (passwords/second)",
                    "Progress percentage",
                    "Estimated completion time"
                ],
                "tips": "Show cracked: john --show hashes.txt"
            },
            {
                "number": 7,
                "title": "Offline Cracking - Hashcat (GPU)",
                "command": "hashcat -m 1000 -a 0 hashes.txt /usr/share/wordlists/rockyou.txt",
                "purpose": "GPU-accelerated password cracking (much faster)",
                "look_for": [
                    "Hash type mode (-m value)",
                    "Cracking speed (GH/s with GPU)",
                    "Recovered passwords",
                    "GPU temperature (don't melt your card!)"
                ],
                "tips": "Hashcat is WAY faster than John if you have a GPU"
            },
            {
                "number": 8,
                "title": "Rule-Based Attacks",
                "command": "john --wordlist=words.txt --rules hashes.txt",
                "purpose": "Apply mutations to wordlist (Password -> P@ssw0rd!)",
                "look_for": [
                    "Additional cracked passwords",
                    "Common password patterns",
                    "Complexity requirements hints",
                    "Password policy clues"
                ],
                "tips": "Rules catch passwords that aren't directly in wordlists"
            }
        ]
    },

    "wireless-pentest": {
        "name": "Wireless Network Penetration Testing",
        "description": "Attack and secure wireless networks (WPA/WPA2)",
        "difficulty": "Intermediate",
        "steps": [
            {
                "number": 1,
                "title": "Enable Monitor Mode",
                "command": "airmon-ng start wlan0",
                "purpose": "Put wireless card into monitor mode to capture packets",
                "look_for": [
                    "Monitor interface name (usually wlan0mon)",
                    "No interfering processes",
                    "Chipset compatibility confirmed",
                    "Success message"
                ],
                "tips": "Kill interfering processes: airmon-ng check kill"
            },
            {
                "number": 2,
                "title": "Discover Wireless Networks",
                "command": "airodump-ng wlan0mon",
                "purpose": "Scan for nearby wireless networks and clients",
                "look_for": [
                    "BSSID (router MAC address)",
                    "Channel number",
                    "Encryption type (WPA/WPA2/WEP)",
                    "Signal strength (PWR)",
                    "Connected clients (STATION)"
                ],
                "tips": "Press Ctrl+C to stop scanning once you find your target"
            },
            {
                "number": 3,
                "title": "Capture Handshake",
                "command": "airodump-ng -c <channel> --bssid <BSSID> -w capture wlan0mon",
                "purpose": "Capture WPA handshake when client connects",
                "look_for": [
                    "'WPA handshake' message in top right",
                    "Connected clients (need at least one)",
                    "Data packets increasing",
                    "Capture file being written"
                ],
                "tips": "No clients? Deauth attack forces reconnection (see next step)"
            },
            {
                "number": 4,
                "title": "Deauthentication Attack (Force Handshake)",
                "command": "aireplay-ng --deauth 10 -a <BSSID> wlan0mon",
                "purpose": "Kick clients off network to capture handshake on reconnect",
                "look_for": [
                    "ACKs received (deauth packets sent successfully)",
                    "Client disconnects on airodump-ng",
                    "Client reconnects (handshake captured)",
                    "WPA handshake message appearing"
                ],
                "tips": "This is ILLEGAL on networks you don't own. Lab use only!"
            },
            {
                "number": 5,
                "title": "Crack WPA Password",
                "command": "aircrack-ng -w /usr/share/wordlists/rockyou.txt -b <BSSID> capture*.cap",
                "purpose": "Crack WPA password using captured handshake",
                "look_for": [
                    "Handshake validation (must be present)",
                    "Keys tested per second",
                    "KEY FOUND! message with password",
                    "Progress indication"
                ],
                "tips": "No match? Try bigger wordlist or use hashcat (faster)"
            },
            {
                "number": 6,
                "title": "Alternative: Hashcat Cracking",
                "command": "# Convert first:\nhccapx capture.cap converted.hccapx\n# Then crack:\nhashcat -m 2500 converted.hccapx wordlist.txt",
                "purpose": "GPU-accelerated WPA cracking (much faster than aircrack)",
                "look_for": [
                    "Conversion success",
                    "GPU utilization",
                    "Cracking speed (hashes/sec)",
                    "Recovered passphrase"
                ],
                "tips": "Hashcat can be 100x faster with a good GPU"
            }
        ]
    },

    "post-exploitation": {
        "name": "Post-Exploitation & Privilege Escalation",
        "description": "What to do after gaining initial access to a system",
        "difficulty": "Advanced",
        "steps": [
            {
                "number": 1,
                "title": "Establish Persistent Access",
                "command": "# Create reverse shell that survives reboot\n# Linux: Add to crontab\n# Windows: Create scheduled task",
                "purpose": "Ensure you can get back in even if session dies",
                "look_for": [
                    "Cron job or scheduled task created",
                    "Backdoor service running",
                    "SSH key added to authorized_keys",
                    "Persistence mechanism hidden"
                ],
                "tips": "Be stealthy - defenders check common persistence locations"
            },
            {
                "number": 2,
                "title": "Gather System Information",
                "command": "# Linux: uname -a, cat /etc/*release\n# Windows: systeminfo",
                "purpose": "Understand what system you've compromised",
                "look_for": [
                    "OS version and architecture",
                    "Kernel version (Linux privilege escalation)",
                    "Installed patches",
                    "System role (workstation, server, domain controller)"
                ],
                "tips": "Outdated kernel = likely privilege escalation path"
            },
            {
                "number": 3,
                "title": "Enumerate Users",
                "command": "# Linux: cat /etc/passwd, w, last\n# Windows: net user, net localgroup administrators",
                "purpose": "Find other user accounts and admin users",
                "look_for": [
                    "Admin/root accounts",
                    "Currently logged-in users",
                    "Recently logged-in users",
                    "Service accounts"
                ],
                "tips": "Target admin users for credential theft or lateral movement"
            },
            {
                "number": 4,
                "title": "Check Privileges",
                "command": "# Linux: sudo -l, id\n# Windows: whoami /priv, whoami /groups",
                "purpose": "See what commands you can run with elevated privileges",
                "look_for": [
                    "NOPASSWD sudo entries (instant privilege escalation)",
                    "Dangerous permissions (SeDebugPrivilege, SeImpersonate)",
                    "Group memberships",
                    "Capabilities"
                ],
                "tips": "sudo -l often reveals privilege escalation paths"
            },
            {
                "number": 5,
                "title": "Find SUID/SGID Files (Linux)",
                "command": "find / -perm -4000 -type f 2>/dev/null",
                "purpose": "Find files that run with owner's privileges",
                "look_for": [
                    "Unusual SUID binaries",
                    "Custom applications with SUID",
                    "Known vulnerable SUID programs",
                    "World-writable SUID files"
                ],
                "tips": "Check GTFOBins for privilege escalation techniques"
            },
            {
                "number": 6,
                "title": "Search for Credentials",
                "command": "# Look for:\n# - Configuration files (.conf, .config)\n# - History files (.bash_history, .mysql_history)\n# - Notes (notes.txt, passwords.txt)\n# - Database connection strings",
                "purpose": "Find hardcoded passwords and credentials",
                "look_for": [
                    "Database passwords in config files",
                    "API keys and tokens",
                    "SSH private keys",
                    "Browser saved passwords"
                ],
                "tips": "Developers often hardcode credentials - check config files!"
            },
            {
                "number": 7,
                "title": "Network Enumeration",
                "command": "# Linux: ifconfig, netstat -antlp, arp -a\n# Windows: ipconfig /all, netstat -ano",
                "purpose": "Map internal network and find other hosts",
                "look_for": [
                    "Additional network interfaces",
                    "Internal IP ranges",
                    "Listening services",
                    "Established connections"
                ],
                "tips": "Multi-homed hosts = pivot points to other networks"
            },
            {
                "number": 8,
                "title": "Escalate Privileges",
                "command": "# Use tools like:\n# Linux: LinPEAS, linuxprivchecker\n# Windows: WinPEAS, PowerUp, Sherlock",
                "purpose": "Gain root/SYSTEM privileges",
                "look_for": [
                    "Kernel exploits",
                    "Misconfigurations",
                    "Weak service permissions",
                    "DLL hijacking opportunities"
                ],
                "tips": "Automated tools find 90% of privesc vectors instantly"
            }
        ]
    }
}


def get_workflow(workflow_name):
    """Get a specific workflow by name"""
    return WORKFLOWS.get(workflow_name.lower())


def list_workflows():
    """List all available workflows"""
    return {name: data["name"] for name, data in WORKFLOWS.items()}


def get_workflow_names():
    """Get list of workflow names (keys)"""
    return list(WORKFLOWS.keys())

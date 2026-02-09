# CommandBrain - What's Included? 📦

## Default Installation (Everyone Gets This)

When you run the installer, you automatically get **~30 essential Linux commands**:

### 📁 File Management (7 commands)
- `ls` - List files and directories
- `cd` - Change directory
- `pwd` - Print working directory
- `mkdir` - Create directories
- `cp` - Copy files
- `mv` - Move/rename files
- `rm` - Remove files (with safety notes!)
- `cat` - View file contents

### 🌐 Networking (6 commands)
- `ping` - Test connectivity
- `ssh` - Secure remote login
- `scp` - Secure file copy
- `ifconfig` - Network interfaces (legacy)
- `ip` - Modern network configuration
- `netstat` - Network statistics
- `ss` - Socket statistics (modern netstat)

### 🔐 Permissions & Users (3 commands)
- `chmod` - Change permissions
- `chown` - Change ownership
- `sudo` - Run as superuser
- `passwd` - Change passwords

### 💻 System Information (3 commands)
- `top` - Real-time processes
- `ps` - Process status
- `df` - Disk space usage

### 📝 Text Processing (3 commands)
- `grep` - Search text patterns
- `sed` - Stream editor
- `awk` - Text processing language

### 🗄️ Archiving (1 command)
- `tar` - Archive files

### 📦 Package Management (1 command)
- `apt` - Debian/Ubuntu packages

### ⚙️ System Control (2 commands)
- `systemctl` - Service management
- `shutdown` - Power management

**Total: ~30 core Linux commands that EVERYONE needs**

---

## Optional: Kali Security Tools (For Pentesters/Security Students)

**⚠️ You must explicitly choose to add these during installation!**

When the installer asks:
```
[4/4] Add Kali Linux tools? (y/n):
```

If you answer **"n"** → You're done! Basic commands only.  
If you answer **"y"** → Adds 30+ security tools below.

### 🔍 Network Scanning (2 tools)
- `nmap` - Network scanner (the KING!)
- `masscan` - Ultra-fast port scanner

### 🌐 Web Application Testing (4 tools)
- `burpsuite` - Web security testing platform
- `sqlmap` - SQL injection tool
- `nikto` - Web server scanner
- `dirb` - Directory brute-forcer
- `gobuster` - Fast directory/DNS bruteforcer

### 💥 Exploitation (2 tools)
- `metasploit` - Exploit framework
- `searchsploit` - Exploit database search

### 🔑 Password Attacks (3 tools)
- `hydra` - Network login cracker
- `john` - John the Ripper (hash cracker)
- `hashcat` - GPU-accelerated hash cracker

### 📡 Wireless (1 tool suite)
- `aircrack-ng` - WiFi security testing suite

### 🕵️ Sniffing & Spoofing (3 tools)
- `wireshark` - Network protocol analyzer
- `tcpdump` - Packet sniffer
- `ettercap` - MITM attack tool

### 🔎 Information Gathering (3 tools)
- `whois` - Domain registration info
- `dnsenum` - DNS enumeration
- `theHarvester` - OSINT gathering tool

### 🎭 Social Engineering (1 tool)
- `setoolkit` - Social engineering toolkit

### 🔬 Forensics (2 tools)
- `binwalk` - Firmware analysis
- `volatility` - Memory forensics

**Total: ~30+ security-focused tools**

---

## 📊 Quick Comparison

| Feature | Default Install | With Kali Tools |
|---------|----------------|-----------------|
| **Commands Included** | ~30 | ~60+ |
| **Target Audience** | Everyone | Security pros |
| **Use Cases** | Daily Linux tasks | Penetration testing |
| **File Size** | Small (~200KB) | Medium (~400KB) |
| **Installation Time** | 10 seconds | 20 seconds |
| **Examples Per Command** | Yes | Yes |
| **Real-world tips** | Yes | Yes |

---

## 🎯 Which Should You Choose?

### Choose **DEFAULT ONLY** if you:
- ✅ Just need Linux command reference
- ✅ Are a developer/sysadmin
- ✅ Don't do security testing
- ✅ Want a clean, focused tool
- ✅ Are learning Linux basics

### Add **KALI TOOLS** if you:
- ✅ Study cybersecurity (CySA+, CEH, OSCP)
- ✅ Use Kali Linux
- ✅ Do penetration testing
- ✅ Need security tool reference
- ✅ Want everything in one place

---

## 💡 You Can Always Add Kali Tools Later!

**Installed without Kali tools?** No problem!

Just run:
```bash
commandbrain-kali
```

And boom! Security tools added instantly. No reinstall needed.

**Want to remove Kali tools?**
```bash
# Backup your database
cp ~/.commandbrain.db ~/.commandbrain.db.backup

# Re-run setup (replaces database)
commandbrain-setup

# Or manually delete them:
commandbrain search -t category Network-Scanning  # Find them
# Then manually delete via SQLite if you know how
```

---

## 🔍 How to See What You Have

```bash
# Show total command count
commandbrain stats

# List all categories
commandbrain list

# If you see categories like:
# - "Network-Scanning"
# - "Exploitation"  
# - "Password-Attacks"
# → You have Kali tools installed

# If you only see:
# - "Basic"
# - "Networking"
# - "System-Info"
# → You have default only
```

---

## 📝 Notes

1. **All tools include:**
   - Description
   - Usage syntax
   - Multiple examples
   - Related commands
   - Pro tips and warnings
   - Tags for searching

2. **Kali tools have extra warnings:**
   - "DANGEROUS!" tags where appropriate
   - Ethical use reminders
   - Stealth/noise level warnings
   - Legal considerations

3. **Database size:**
   - Default: ~200KB
   - With Kali: ~400KB
   - Still tiny and fast!

---

## 🎓 For Students

**Taking a general Linux course?**  
→ Default installation is perfect

**Taking a security certification (CySA+, CEH, OSCP)?**  
→ Add Kali tools!

**Not sure?**  
→ Start with default, add Kali later if needed

---

## ✨ Best Part: It's YOUR Choice!

The installer **ASKS** you. It doesn't decide for you.  
You're in complete control of what gets installed.

Default is clean and focused.  
Kali addition is comprehensive.  
Both are excellent! 🎯

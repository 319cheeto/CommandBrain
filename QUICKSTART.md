# CommandBrain - Quick Start Guide 🚀

## Step 1: Install (Choose ONE method)

**💡 Not sure what commands to type?** See [COMMAND_REFERENCE.md](COMMAND_REFERENCE.md) for exact examples!

### 🎯 **EASIEST - One-Click Install**

**On Windows:**
1. Download and extract CommandBrain to your Documents folder
2. Open Command Prompt (Start → type "cmd" → Enter)
3. Navigate to the folder:
   ```powershell
   cd Documents\CommandBrain
   ```
4. Run the installer:
   ```powershell
   install_windows.bat
   ```
5. Open a NEW Command Prompt window (close the old one)
6. Done! Skip to Step 2.

**On Linux/Mac/WSL:**
1. Clone the repository:
   ```bash
   git clone https://github.com/319cheeto/CommandBrain.git
   cd CommandBrain
   ```
2. Make installer executable and run it:
   ```bash
   chmod +x install_linux.sh
   ./install_linux.sh
   ```
4. Done! Skip to Step 2.

---

### 📦 **RECOMMENDED - Pip Install**

Works on all platforms (Windows, Linux, Mac, WSL):

```bash
# From inside the CommandBrain folder:
pip install -e .
commandbrain-setup
python enhance_slang_tags.py
```

**Linux/Mac:** Run `source ~/.bashrc` or close/reopen terminal
**Windows:** Open a NEW Command Prompt window

Done! Skip to Step 2.

---

### 🔧 **MANUAL - Old Way (Still Works)**

**Windows:**
```powershell
python setup_commandbrain.py
python commandbrain.py search ssh
```

**Linux/Mac/WSL:**
```bash
chmod +x *.py
python3 setup_commandbrain.py
python3 commandbrain.py search ssh
```

---

## Step 2: Use It! 

After installation, you can use `commandbrain` from **anywhere**:

### Basic Search
```bash
commandbrain search ssh
```

### Detailed View (with examples)
```bash
commandbrain search -d grep
```

### Search by Type
```bash
# Search only command names
commandbrain search -t name netstat

# Search by category
commandbrain search -t category networking

# Search by tags
commandbrain search -t tags dangerous
```

### Other Commands
```bash
# List all categories
commandbrain list

# Show statistics
commandbrain stats

# Add a new command
commandbrain add
```

---

## Step 3: (Optional) Add Kali Tools

**⚠️ OPTIONAL - Only for Security Professionals/Students!**

If you're studying for security certifications (CySA+, CEH, OSCP) or using Kali Linux:

```bash
commandbrain-kali
```

**This adds 30+ Kali security tools:**
- Network scanning: nmap, masscan, netdiscover
- Web testing: burpsuite, sqlmap, nikto, gobuster
- Exploitation: metasploit, searchsploit
- Password attacks: hydra, john, hashcat
- Wireless: aircrack-ng suite
- Sniffing: wireshark, tcpdump, ettercap
- And more!

**Don't need these?** Skip this step! Your basic Linux commands work perfectly without them.

---

## Step 4: (Optional) Import Your Own Commands

Have a list of commands in a text file?

```bash
commandbrain-import
```

It will prompt you for the file path.

---

## 💡 Pro Tips

### What Did I Install?

Check what commands you have:
```bash
commandbrain stats   # Shows total count
commandbrain list    # Shows categories
```

See [WHATS_INCLUDED.md](WHATS_INCLUDED.md) for the complete breakdown of:
- Default commands (~30 basic Linux)
- Optional Kali tools (~30 security)

### Create a Short Alias

**Linux/Mac/WSL** - Add to `~/.bashrc` or `~/.zshrc`:
```bash
alias cb='commandbrain'
alias cbs='commandbrain search'
alias cbd='commandbrain search -d'
```

Then reload:
```bash
source ~/.bashrc
```

Now you can use:
```bash
cb search docker
cbs network
cbd ssh
```

**Windows** - Create `cb.bat` in a folder in your PATH:
```batch
@echo off
commandbrain %*
```

---

## 🎯 Real-World Examples

### "I forgot the syntax for grep"
```bash
commandbrain search -d grep
```

Output shows:
- Description
- Usage syntax
- Multiple examples
- Related commands
- Pro tips

### "What network commands do I have?"
```bash
commandbrain search -t category network
```

### "I need commands for file management"
```bash
commandbrain search file
```

### "Show me all dangerous commands"
```bash
commandbrain search -t tags dangerous
```

---

## 📍 Database Location

Your commands are stored at:
- **Windows:** `C:\Users\YourName\.commandbrain.db`
- **Linux/Mac:** `~/.commandbrain.db`

### Backup Your Database
```bash
# Linux/Mac:
cp ~/.commandbrain.db ~/commandbrain_backup.db

# Windows:
copy %USERPROFILE%\.commandbrain.db %USERPROFILE%\commandbrain_backup.db
```

---

## 🆘 Troubleshooting

### "commandbrain: command not found"
You probably didn't install it with pip. Either:
1. Run: `pip install -e .` from the project folder
2. Or use: `python commandbrain.py` instead

### "Database not found"
Run setup:
```bash
commandbrain-setup
# Or manually:
python setup_commandbrain.py
```

### Colors not working on Windows
- Use Windows Terminal (recommended)
- Or upgrade to Windows 10 version 1511+
- Or use WSL

### "Permission denied" on Linux
```bash
chmod +x *.py *.sh
```

---

## 📚 Full Documentation

- [README.md](README.md) - Full usage guide
- [INSTALL.md](INSTALL.md) - Detailed installation instructions
- [CODE_REVIEW.md](CODE_REVIEW.md) - What was fixed and why

---

## 🎓 Quick Reference Card

```bash
# SEARCH
commandbrain search [term]              # Search everything
commandbrain search -d [term]           # Detailed view
commandbrain search -t name [term]      # Search names only
commandbrain search -t category [term]  # Search categories
commandbrain search -t tags [term]      # Search tags

# INFO
commandbrain list                       # List categories
commandbrain stats                      # Show statistics

# MANAGE
commandbrain add                        # Add new command
commandbrain-import                     # Import from file
commandbrain-kali                       # Add Kali tools

# SETUP (one-time)
commandbrain-setup                      # Create database
```

---

## 🎉 You're All Set!

Start exploring:
```bash
commandbrain search network
commandbrain list
commandbrain search -d ssh
```

**Remember:** This tool works **offline** and searches **instantly**. No more googling or scrolling through man pages! 🧠

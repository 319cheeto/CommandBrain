# 🧠 CommandBrain

**Offline Linux command reference for cybersecurity students**

## 🎯 Search by PURPOSE, Not Command Names!

Students don't need to memorize cryptic command names. Just type what you want to do:

```bash
cb brute force      → Find password attack tools (hydra, john)
cb network scan     → Find nmap, masscan
cb password crack   → Find john, hashcat, hydra
cb web hack         → Find burpsuite, sqlmap, nikto
cb sniffing         → Find wireshark, tcpdump, ettercap
cb exploit          → Find metasploit, searchsploit
cb sql inject       → Find sqlmap
```

**Ultra-simple syntax:** Just `cb` + what you want to do. That's it!

Perfect for intro cybersecurity classes where students are overwhelmed by hundreds of commands.

---

## 📥 **EASY INSTALLATION**

### **🚀 FASTEST WAY - For Students Who Just Want It To Work**

**See: [INSTALL_SIMPLE.md](INSTALL_SIMPLE.md) - Dead simple, step-by-step with pictures!**

---

### **Prerequisites:**
- **Python 3.6+** (usually pre-installed on Kali/Linux)
- **Git** (optional - or download ZIP)

**Don't have git?** Install it:
```bash
sudo apt update && sudo apt install -y git
```

### **Quick Install (One-Click)**

**Step 1: Get the code**
```bash
git clone https://github.com/319cheeto/CommandBrain.git
cd CommandBrain
```

**💡 Don't have git?** [Download ZIP](https://github.com/319cheeto/CommandBrain/archive/refs/heads/master.zip), extract it, and rename the folder to `CommandBrain`

**Step 2: Run the installer**

**Windows:**
```bash
install_windows.bat
```

**Linux/Mac/WSL:**
```bash
bash install_linux.sh
```

**Alternative (if above doesn't work):**
```bash
chmod +x install_linux.sh
./install_linux.sh
```

**Step 3: ⚠️ IMPORTANT - Reload Your Terminal**

**Linux/Mac users:** Your terminal needs to reload its settings.

**Pick ONE:**
- **Option A:** Run this command: `source ~/.bashrc` (fast)
- **Option B:** Close and reopen your terminal (simpler)

**Windows users:** Just open a NEW Command Prompt window.

**What does this do?** It tells your terminal where to find the `cb` command. You only do this ONCE after installation!

**Step 4: Test it works!**
```bash
cb ssh                # Should show SSH command info
cb password cracking  # Search by purpose!
```

If you see command info, **YOU'RE DONE!** 🎉  
If you see "command not found", go back to Step 3 (you forgot to reload!).

---

### **✅ How to Know Installation Worked**

**Quick test:**
```bash
cb ssh             # Should show SSH command details
```

**Run automatic tests:**
```bash
# Windows:
test_cb.bat

# Linux/Mac:
chmod +x test_cb.sh
./test_cb.sh
```

**✓ Success:** You see command information and examples  
**✗ Failed:** "command not found" error
  - **Linux/Mac:** Run `source ~/.bashrc` or close/reopen terminal
  - **Windows:** Open a NEW Command Prompt window

---

**⚠️ Installation Issues on Kali Linux?**
- See [KALI_QUICKSTART.md](KALI_QUICKSTART.md) for a quick one-page guide
- See [KALI_INSTALL_FIX.md](KALI_INSTALL_FIX.md) for detailed troubleshooting
- Run `./test_install.sh` for automated diagnostics

---

### **📦 What You Get:**

**The installer automatically:**
- ✅ Checks Python installation
- ✅ Sets up virtual environment (Linux)
- ✅ Installs CommandBrain
- ✅ Creates database with ~30 essential commands
- ✅ **Adds student-friendly slang terms** (brute force, network scan, etc.)
- ✅ Asks if you want Kali security tools (optional)

**Included commands:**
- ✅ **~30 Core Linux Commands** (included by default)
  - File management: ls, cd, cp, mv, rm, etc.
  - Networking: ssh, ping, netstat, ip, etc.
  - System: ps, top, df, chmod, etc.
  - Text processing: grep, sed, awk, etc.

- ⚙️ **~30 Kali Security Tools** (OPTIONAL - you'll be asked)
  - nmap, metasploit, burpsuite, sqlmap, etc.
  - Only added if you choose 'yes' during install
  - Perfect for security students/professionals

---

### **Alternative: Manual Install (Advanced)**

```bash
# Works on Windows, Linux, Mac, WSL
pip install -e .
commandbrain-setup         # Installs basic Linux commands
python enhance_slang_tags.py  # Add purpose-based search
commandbrain search ssh    # You're done!

# (Optional) Add Kali security tools later:
commandbrain-kali
```

---
See [INSTALL.md](INSTALL.md) for manual installation, creating executables, and troubleshooting.

**💡 Not sure what commands to type?** See [COMMAND_REFERENCE.md](COMMAND_REFERENCE.md) for exact syntax and examples!

---

## What Problem Does This Solve?

### The Real Issue:
- `man` pages are dense and overwhelming
- Google breaks your focus
- You forget commands mid-task
- Can't remember if you need `netstat`, `ss`, or `lsof`
- Need instant answers, not 10-minute research sessions

### What CommandBrain Fixes:
✓ Search commands by name, purpose, OR what they do  
✓ Find related commands ("If I know grep, what else should I learn?")  
✓ See real examples instantly  
✓ Your custom notes in YOUR words  
✓ Works offline - no internet needed  
✓ Fast SQLite database (searches 10,000+ commands instantly)  

---

## 🚀 Quick Start (After Installation)

**It's THIS simple:**

```bash
cb ssh                      # Search for ssh
cb network monitoring       # Multi-word - no quotes needed!
cb -d grep                  # Detailed view with examples
cb --list                   # List all categories
```

**Just 2 letters + what you need!** As easy as typing `man` but way more powerful!

---

##  **Why Students Love This**

✅ **Faster than Google** - 2 seconds vs 2 minutes  
✅ **Works offline** - No internet needed  
✅ **No distractions** - Stays in terminal  
✅ **Multi-word search** - No quotes required  
✅ **Real examples** - Every command has them  
✅ **Related commands** - Discover what else exists  

**See [STUDENT_GUIDE.md](STUDENT_GUIDE.md) for student-friendly documentation**  
**See [INSTRUCTOR_GUIDE.md](INSTRUCTOR_GUIDE.md) for teaching integration tips**

---

## 📖 Usage Examples

### Basic Search (The Main Thing!)
```bash
cb ssh                  # Find SSH command
cb network              # Find network-related commands
cb file permissions     # Multi-word search (no quotes!)
```

### Detailed View (With Examples)
```bash
cb -d grep              # See full examples and usage
cb -d nmap              # Perfect for learning new tools
```

### Special Commands
```bash
cb --list               # List all categories
cb --stats              # Show what's installed  
cb --add                # Add your own command
```

### Advanced (Optional)
```bash
cb -t name ssh          # Search command names only
cb -t category network  # Search by category
cb -t tags dangerous    # Search by tags
```

**💡 What commands are included?**  
See [WHATS_INCLUDED.md](WHATS_INCLUDED.md) for the complete list of default vs. optional commands.

---

## 🎯 Installation Methods Compared

| Method | Difficulty | Best For | Command Example |
|--------|-----------|----------|-----------------|
| **One-Click Installer** | ⭐ Easiest | Everyone | `install_windows.bat` |
| **Pip Install** | ⭐⭐ Easy | Developers | `pip install -e .` |
| **Manual** | ⭐⭐⭐ Moderate | Customization | `python3 commandbrain.py` |
| **Standalone Exe** | ⭐⭐⭐⭐ Advanced | No Python | See INSTALL.md |

See [INSTALL.md](INSTALL.md) for detailed instructions for each method.

---

## 🚀 Old Quick Start (Manual Method)

### Step 1: Setup Database
```bash
# Make scripts executable
chmod +x setup_commandbrain.py commandbrain.py import_commands.py

# Create and populate database
python3 setup_commandbrain.py
```

### Step 2: Import Your Command List
```bash
# Import from your RTF file
python3 import_commands.py
# When prompted, enter: /mnt/user-data/uploads/linux_commands_basic.rtf
```

### Step 3: Start Searching!
```bash
# Search for anything
python3 commandbrain.py search network

# Detailed view
python3 commandbrain.py search -d ssh

# Search by category
python3 commandbrain.py search -t category networking

# Search only command names
python3 commandbrain.py search -t name grep
```

---

## 📖 Usage Guide

### Basic Search
```bash
./commandbrain.py search [term]
```
Searches EVERYTHING: name, description, tags, related commands

**Examples:**
```bash
./commandbrain.py search file          # Find all file-related commands
./commandbrain.py search network       # Network commands
./commandbrain.py search monitoring    # System monitoring tools
./commandbrain.py search password      # Password/auth related
```

### Search Types
```bash
# Search only command names
./commandbrain.py search -t name ssh

# Search only categories
./commandbrain.py search -t category security

# Search only tags
./commandbrain.py search -t tags dangerous

# Search descriptions and notes
./commandbrain.py search -t description "real-time"
```

### Detailed Output
```bash
# Short list (default)
./commandbrain.py search ssh

# Detailed view with examples, usage, notes
./commandbrain.py search -d ssh
```

### Other Commands
```bash
# List all categories
./commandbrain.py list

# Add a new command interactively
./commandbrain.py add

# Show database statistics
./commandbrain.py stats
```

---

## 🎯 Real-World Examples

### "I need to check network connections"
```bash
$ ./commandbrain.py search connections

Found 3 command(s):

netstat [Networking]
  Displays network connections, routing tables, interface stats

ss [Networking]
  Socket statistics - modern netstat replacement

lsof [System-Info]
  Lists open files (including network sockets)
```

### "I forgot how to search files recursively"
```bash
$ ./commandbrain.py search -d recursive

grep [Searching]
Description: Searches for patterns in files

Usage: grep [options] pattern [files]

Examples:
  $ grep 'error' log.txt
  $ grep -r 'password' /etc/

Related Commands: egrep, fgrep, ack, ag, ripgrep

Notes:
  💡 Use -i for case-insensitive, -r for recursive, -n for line numbers
```

### "What other commands are like grep?"
```bash
$ ./commandbrain.py search -t name grep

Found 3 command(s):

grep [Searching]
  Searches for patterns in files

egrep [Searching]  
  Extended grep (supports more regex patterns)

fgrep [Searching]
  Fast grep (searches for fixed strings, no regex)
```

---

## 🔧 Adding Your Own Commands

### Interactive Mode
```bash
./commandbrain.py add
```

You'll be prompted for:
- Command name
- Category
- Description
- Usage (optional)
- Examples (optional, separate with `\n`)
- Related commands (comma-separated)
- Notes/tips
- Tags (comma-separated)

### Bulk Import
Create a text file with this format:

```
Category Name

command1: Description of command1.
command2: Description of command2.

Another Category

command3: Description of command3.
```

Then import:
```bash
./commandbrain.py import_commands.py
```

---

## 💡 Pro Tips for ADHD Success

### 1. Add Personal Notes
When you learn something the hard way, add it:
```bash
./commandbrain.py add
# Add your "oh shit, I'll never forget THIS" moments
```

### 2. Tag Everything
Tags are searchable! Use tags like:
- `dangerous` (commands that can break things)
- `exam` (stuff that'll be on your CySA+)
- `forgotten` (commands you always forget)
- `confusing` (need to review these more)

### 3. Create Command Aliases
Add to your `~/.bashrc`:
```bash
alias cb='python3 ~/commandbrain.py search'
alias cbd='python3 ~/commandbrain.py search -d'
```

Now you can just type:
```bash
cb network
cbd ssh
```

### 4. Mobile Access
Copy the database to your phone:
```bash
# On Linux
cp ~/.commandbrain.db ~/Dropbox/

# Access from phone via Termux or SSH
```

---

## 🎓 For Your Professor

**This tool demonstrates:**
- Database design (SQLite schema, indexing)
- Python programming (argparse, sqlite3, file I/O)
- Problem-solving (identifying gaps in existing tools)
- Accessibility (adapting tools for learning disabilities)
- Initiative (building solutions, not just complaining)

**Skills used:**
- SQL database creation and querying
- Command-line interface design
- Text processing and parsing
- User experience design
- Documentation

This isn't "taking a shortcut" - it's **building infrastructure to support learning**.  
Security professionals build tools all the time. This is legitimate skill development.

---

## 📦 Files Included

- `setup_commandbrain.py` - Creates database, adds basic commands
- `commandbrain.py` - Main search interface
- `import_commands.py` - Bulk import tool
- `README.md` - This file

---

## 🚀 Next Steps

### Add More Commands
Priority list to expand:
1. **Kali Linux Tools** (nmap, metasploit, burpsuite, etc.)
2. **CySA+ Specific** (SIEM, incident response, threat hunting)
3. **Your Mistakes** (commands you've screwed up - add warnings!)
4. **Exam Topics** (anything that'll be tested)

### Advanced Features (Future)
- Export to flashcards (for Anki)
- Quiz mode (random command, guess what it does)
- Difficulty ratings (beginner/intermediate/advanced)
- Cheat sheet generator (export category to PDF)

---

## ❓ Frequently Asked Questions (Students)

### Installation Questions

**Q: Do I type "cb" or "commandbrain"?**  
**A:** Both work! `cb` is shorter and easier - use that. They do exactly the same thing.

**Q: Where do I type these commands?**  
**A:** In your terminal (Linux/Mac) or Command Prompt (Windows). NOT in your browser or a text editor!

**Q: Do I need to be in the CommandBrain folder to use it?**  
**A:** NO! After installation, `cb` works from anywhere. That's the whole point!

**Q: What if I get "command not found"?**  
**A:** 
- **Linux/Mac:** Did you run `source ~/.bashrc` or close/reopen terminal? (You must do this ONCE after install)
- **Windows:** Did you open a NEW Command Prompt? (Old windows won't see the new command)
- **Still broken?** Run `test_cb.bat` (Windows) or `./test_cb.sh` (Linux) to diagnose

**Q: Do I need internet to use CommandBrain?**  
**A:** NO! It works completely offline after installation. Perfect for exams and labs without internet.

**Q: Should I add Kali tools during installation?**  
**A:** 
- **YES** if you're taking a cybersecurity/pentesting course
- **NO** if you're just learning basic Linux commands
- **Don't worry** - you can add them later with: `commandbrain-kali`

**Q: What does "source ~/.bashrc" mean? Why do I need it?**  
**A:** 
- Your terminal reads settings from `.bashrc` when it starts
- The installer added CommandBrain's location to that file
- "source" tells your terminal to re-read that file RIGHT NOW
- Without this, you'd have to close and reopen your terminal
- You only do it ONCE after installation!

### Usage Questions

**Q: How do I search for a command?**  
**A:** Just type `cb` followed by what you want to do:
```bash
cb ssh                 # Find SSH command
cb find files          # Search by purpose
cb password crack      # Multi-word search
```

**Q: What's the difference between `cb ssh` and `cb search ssh`?**  
**A:** No difference! The word "search" is optional. `cb ssh` automatically searches.

**Q: Can I search by what a command DOES instead of its name?**  
**A:** YES! That's the main feature!
```bash
cb brute force      # Finds hydra, john, etc.
cb network scan     # Finds nmap, masscan
cb sniffing         # Finds wireshark, tcpdump
```

**Q: How do I see examples for a command?**  
**A:** Use the `-d` (detailed) flag:
```bash
cb -d ssh          # Shows examples and detailed info
```

**Q: How do I list all available commands?**  
**A:**
```bash
cb --all           # List everything
cb --list          # Show categories
```

### Troubleshooting Questions

**Q: I installed it, but `cb` still doesn't work!**  
**A:** Run the test script:
- Windows: `test_cb.bat`
- Linux/Mac: `chmod +x test_cb.sh && ./test_cb.sh`

This will tell you exactly what's wrong.

**Q: Can I use this on Windows?**  
**A:** YES! It works on Windows, Linux, Mac, and WSL.

**Q: It says "Database not found" - what do I do?**  
**A:** Run the setup:
```bash
commandbrain-setup
```
Or just run the installer again: `install_windows.bat` or `./install_linux.sh`

**Q: How do I update CommandBrain?**  
**A:**
```bash
# Windows:
update_windows.bat

# Linux/Mac:
./update_linux.sh
```

**Q: How do I uninstall it?**  
**A:**
```bash
# Windows:
uninstall_windows.bat

# Linux/Mac:
./uninstall_linux.sh
```

**Q: Can I add my own commands?**  
**A:** YES! See [INSTRUCTOR_GUIDE.md](INSTRUCTOR_GUIDE.md) for how to customize it for your course.

**Q: This is cool! Can I contribute?**  
**A:** YES! Open an issue or pull request on GitHub: https://github.com/319cheeto/CommandBrain

---

## 🆘 Troubleshooting

**"Database not found" error**
```bash
python3 setup_commandbrain.py
```

**"Command already exists" when importing**
- This is normal - duplicates are skipped
- The existing entry is kept (your notes are safe)

**Colors not showing in terminal**
- Some terminals don't support ANSI colors
- The tool still works, just without pretty colors

**SQLite not installed**
```bash
# Ubuntu/Debian
sudo apt install sqlite3

# It's usually pre-installed on most Linux systems
```

---

## 📝 License

CommandBrain is released under the MIT License - free for educational use and modification.

---

## 🙏 Credits & Acknowledgments

**Created by Joshua Sears**  
Supplemental Instructor | Game & Web Development Background

**Project Goal:** Reduce student dropout rates by making Linux tools approachable

**Core Innovation:** Purpose-based search using student slang ("brute force", "network scan")  
— No more memorizing cryptic command names!

**Development:** Built using AI-assisted programming (GitHub Copilot, Claude AI) to accelerate implementation while maintaining educational focus.

**Philosophy:** *"Technology should reduce barriers to learning, not create them."*

For detailed credits, see [CREDITS.md](CREDITS.md)

---

**Built for students who learn differently.** 🧠💪

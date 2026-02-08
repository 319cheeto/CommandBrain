# CommandBrain - Command Reference

## 🎯 Quick Answer: What Do I Type?

### Method 1: One-Click Installer (EASIEST)

**Windows (PowerShell or CMD):**
```powershell
cd command_search_tool
install_windows.bat
```
**That's it!** Just type the filename. No python, no extra commands.

**Linux/Mac/WSL:**
```bash
cd command_search_tool
chmod +x install_linux.sh
./install_linux.sh
```
**That's it!** The `./` means "run this file".

---

### Method 2: Pip Install (RECOMMENDED)

**All Platforms (Windows, Linux, Mac, WSL):**
```bash
cd command_search_tool
pip install -e .
commandbrain-setup
commandbrain search ssh
```

**Key Points:**
- `pip install -e .` ← The **dot (.)** means "install from current directory"
- After pip install, you **don't need** to type filenames anymore
- Just type `commandbrain` - it works from any folder!

---

### Method 3: Manual (Run Python Files Directly)

**Linux/Mac/WSL:**
```bash
cd command_search_tool
python3 setup_commandbrain.py          # Setup
python3 commandbrain.py search ssh     # Use it
```
**You must type:** `python3` + `filename.py` + `arguments`

**Windows:**
```powershell
cd command_search_tool
python setup_commandbrain.py           # Setup
python commandbrain.py search ssh      # Use it
```
**You must type:** `python` + `filename.py` + `arguments`

---

## 📋 Comparison Table

| What You Type | Method | Works From Any Folder? |
|---------------|--------|------------------------|
| `install_windows.bat` | One-click installer | ❌ Only in project folder |
| `./install_linux.sh` | One-click installer | ❌ Only in project folder |
| `commandbrain search ssh` | After pip install | ✅ YES - anywhere! |
| `python commandbrain.py search ssh` | Manual | ❌ Only in project folder |

---

## 🤔 Common Questions

### Q: What does the dot (.) mean in `pip install -e .`?
**A:** The dot means "current directory". So it's saying "install the package from the current folder I'm in".

### Q: Why don't I need to type the filename after pip install?
**A:** Pip creates "entry points" (shortcuts) called `commandbrain`, `commandbrain-setup`, etc. They're global commands now!

### Q: What's the difference between `commandbrain.py` and `commandbrain`?
**A:** 
- `commandbrain.py` = The actual Python file (need to type `python` before it)
- `commandbrain` = The shortcut created by pip install (works by itself)

### Q: Do I need to be in the command_search_tool folder?
**A:**
- **One-click installer:** YES
- **Pip install:** Only during installation, then NO
- **Manual method:** YES

### Q: On Windows, do I type `python` or `python3`?
**A:** On Windows, type `python` (no 3). On Linux/Mac, type `python3`.

---

## 💡 Examples - Exactly What To Type

### Scenario 1: Windows User, Easiest Method

```powershell
# Open PowerShell, then:
C:\> cd C:\Users\joshu\OneDrive\Documents\GitHub\command_search_tool
C:\...\command_search_tool> install_windows.bat
# Follow prompts, done!
C:\...\command_search_tool> commandbrain search ssh
```

### Scenario 2: Linux User, Pip Install

```bash
# Open Terminal, then:
user@laptop:~$ cd /path/to/command_search_tool
user@laptop:~/command_search_tool$ pip install -e .
user@laptop:~/command_search_tool$ commandbrain-setup
user@laptop:~/command_search_tool$ cd ~
user@laptop:~$ commandbrain search ssh   # Works from anywhere now!
```

### Scenario 3: Windows User, Manual Method

```powershell
# Open PowerShell, then:
C:\> cd C:\Users\joshu\OneDrive\Documents\GitHub\command_search_tool
C:\...\command_search_tool> python setup_commandbrain.py
C:\...\command_search_tool> python commandbrain.py search ssh
C:\...\command_search_tool> python commandbrain.py list
C:\...\command_search_tool> python commandbrain.py search -d grep
```

### Scenario 4: Already Installed, Daily Use

**If you used pip install:**
```bash
commandbrain search network      # From anywhere!
commandbrain search -d ssh       # From anywhere!
commandbrain list                # From anywhere!
```

**If you used manual method:**
```bash
cd /path/to/command_search_tool        # Must be in folder first
python3 commandbrain.py search network # Then run
```

---

## 🔧 After Installation - What Commands Are Available?

### If You Used Pip Install:
```bash
commandbrain search [term]    # Search commands
commandbrain list             # List categories  
commandbrain add              # Add new command
commandbrain stats            # Show statistics

commandbrain-setup            # Run setup (one-time)
commandbrain-kali             # Add Kali tools (optional)
commandbrain-import           # Import from file (optional)
```

### If You Used Manual Method:
```bash
python3 commandbrain.py search [term]
python3 commandbrain.py list
python3 commandbrain.py add
python3 commandbrain.py stats

python3 setup_commandbrain.py
python3 add_kali_tools.py
python3 import_commands.py
```

---

## 🎓 Understanding File Types

| Extension | What It Is | How To Run |
|-----------|------------|------------|
| `.bat` | Windows batch file | Just type the name: `install_windows.bat` |
| `.sh` | Linux shell script | Use `./`: `./install_linux.sh` |
| `.py` | Python script | Use `python`: `python setup_commandbrain.py` |
| (no extension) | After pip install | Just type the command: `commandbrain` |

---

## ✅ Verification - Did It Work?

After installation, test it:

```bash
# This should work:
commandbrain stats

# You should see something like:
# CommandBrain Statistics
#   Total commands: 30
#   Categories: 8
#   Database: /home/user/.commandbrain.db
```

If you get "command not found", you either:
1. Didn't use pip install (use manual method instead)
2. Need to restart your terminal
3. Need to specify the full path: `python commandbrain.py stats`

---

## 🚀 Pro Tip: Create Your Own Shortcut

After pip install, you can create even shorter aliases:

**Linux/Mac (~/.bashrc or ~/.zshrc):**
```bash
alias cb='commandbrain'
alias cbs='commandbrain search'
alias cbd='commandbrain search -d'
```

Then:
```bash
cb list              # Instead of: commandbrain list
cbs network          # Instead of: commandbrain search network
cbd ssh              # Instead of: commandbrain search -d ssh
```

**Windows (Create cb.bat somewhere in PATH):**
```batch
@echo off
commandbrain %*
```

Then:
```powershell
cb list
cb search network
```

---

Need more help? Check:
- [INSTALL.md](INSTALL.md) - Detailed installation guide
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [README.md](README.md) - Full documentation

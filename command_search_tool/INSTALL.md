# CommandBrain Installation Guide

## 🚀 Quick Install (Recommended)

### For Linux/WSL/Mac

**What you'll type in the terminal:**

```bash
# Step 1: Navigate to the commandbrain directory
cd command_search_tool

# Step 2: Install using pip 
# The dot (.) means "install from current directory"
pip install -e .

# Step 3: Run setup to create the database
# No filename needed - this is now a global command!
commandbrain-setup

# Step 4: (Optional) Add Kali tools
commandbrain-kali

# Step 5: Start using it!
commandbrain search ssh
```

**Example terminal session:**
```bash
user@laptop:~$ cd command_search_tool
user@laptop:~/command_search_tool$ pip install -e .
Successfully installed commandbrain
user@laptop:~/command_search_tool$ commandbrain-setup
✓ Setup Complete!
user@laptop:~/command_search_tool$ commandbrain search ssh
Found 1 command(s):
ssh [Security]
  Secure Shell - remote login protocol
```

### For Windows (CMD/PowerShell)

**What you'll type in PowerShell or CMD:**

```powershell
# Step 1: Navigate to the commandbrain directory
cd command_search_tool

# Step 2: Install using pip
# The dot (.) means "install from current directory"
pip install -e .

# Step 3: Run setup
# No filename needed - this is now a global command!
commandbrain-setup

# Step 4: (Optional) Add Kali tools
commandbrain-kali

# Step 5: Start using it!
commandbrain search ssh
``` 1: One-Click Installers

### Windows One-Click

**What you'll type:**
```powershell
# Navigate to the folder
cd command_search_tool

# Run the installer (just the filename, no extra commands!)
install_windows.bat
```

**Example:**
```powershell
PS C:\Users\joshu> cd command_search_tool
PS C:\Users\joshu\command_search_tool> install_windows.bat
========================================
CommandBrain Windows Installer
========================================
[1/4] Python found!
[2/4] Installing CommandBrain...
[3/4] Setting up database...
[4/4] Add Kali security tools? (y/n): n
Installation Complete!
```

### Linux/Mac One-Click

**What you'll type:**
```bash
# Navigate to the folder
cd command_search_tool

# Make the script executable (first time only)
chmod +x install_linux.sh

# Run the installer (just the filename with ./)
**What you'll type:**
```powershell
# Navigate to the folder
cd command_search_tool

# Run setup (include "python" and the filename)
python setup_commandbrain.py

# Now use it (must include "python" and full filename)
python commandbrain.py search network
```

**Example PowerShell session:**
```powershell
PS C:\Users\joshu> cd command_search_tool
PS C:\Users\joshu\command_search_tool> python setup_commandbrain.py
✓ Setup Complete!
PS C:\Users\joshu\command_search_tool> python commandbrain.py search network
Found 6 command(s):
...
```

**Optional - Create batch file shortcut:**
```powershell
# Method 1: Create a batch file
# 1. Create C:\bin\cb.bat with this content:
@echo off
python C:\Users\joshu\command_search_tool\commandbrain.py %*

# 2. Add C:\bin to your PATH (search "Environment Variables" in Windows)

# Method 2: Use the full path each time
# Create cb.bat in the command_search_tool folder:
@echo off
python "%~dp0commandbrain.py" %*

# Then use it from that folder:
PS C:\Users\joshu\command_search_tool> cb.bat/4] Python found!
[2/4] Installing CommandBrain...
[3/4] Setting up database...
[4/4] Add Kali security tools? (y/n): n
Installation Complete!
```

---

## 📦 Alternative 2: Manual Installation

### Linux/WSL/Mac

**What you'll type:**
```bash
# Navigate to the folder
cd command_search_tool

# Make scripts executable (first time only)
chmod +x *.py

# Run setup (include "python3" and the filename)
python3 setup_commandbrain.py

# Now use it (must include "python3" and full filename)
python3 commandbrain.py search network
```

**Example terminal session:**
```bash
user@laptop:~$ cd command_search_tool
user@laptop:~/command_search_tool$ chmod +x *.py
user@laptop:~/command_search_tool$ python3 setup_commandbrain.py
✓ Setup Complete!
user@laptop:~/command_search_tool$ python3 commandbrain.py search network
Found 6 command(s):
...
```

**Optional - Create alias for easier use:**
```bash
# Add to ~/.bashrc or ~/.zshrc (replace with your actual path!)
echo 'alias cb="python3 /home/user/command_search_tool/commandbrain.py"' >> ~/.bashrc
source ~/.bashrc

# Now you can just type:

## 📦 Alternative: Manual Installation

### Linux/WSL/Mac

```bash
# 1. Make scripts executable
chmod +x *.py

# 2. Run setup
python3 setup_commandbrain.py

# 3. Create alias (add to ~/.bashrc or ~/.zshrc)
echo 'alias cb="python3 /full/path/to/commandbrain.py"' >> ~/.bashrc
source ~/.bashrc

# 4. Use it
cb search network
```

### Windows

```powershell
# 1. Run setup
python setup_commandbrain.py

# 2. Create batch file for easy access
# Create C:\bin\cb.bat with this content:
@echo off
python C:\full\path\to\commandbrain.py %*

# 3. Add C:\bin to your PATH
# Then use it:
cb search network
```

---

## 🐍 Python Version Requirements

**Minimum:** Python 3.6+  
**Recommended:** Python 3.8+

### Check your Python version:
```bash
python3 --version   # Linux/Mac
python --version    # Windows
```

### Install Python (if needed):

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

**Windows:**
Download from [python.org](https://www.python.org/downloads/)

**Mac:**
```bash
brew install python3
```

---

## ✨ Create Standalone Executable (Optional)

Want to run without Python installed? Create an executable:

### Install PyInstaller:
```bash
pip install pyinstaller
```

### Create executable:

**Linux/Mac:**
```bash
cd command_search_tool
pyinstaller --onefile --name commandbrain commandbrain.py
# Executable will be in: dist/commandbrain
```

**Windows:**
```powershell
cd command_search_tool
pyinstaller --onefile --name commandbrain.exe commandbrain.py
# Executable will be in: dist\commandbrain.exe
```

### Use the executable:
```bash
# Copy to a folder in your PATH
# Linux/Mac:
sudo cp dist/commandbrain /usr/local/bin/

# Windows:
# Copy dist\commandbrain.exe to C:\Windows\System32\
# Or add dist\ folder to your PATH
```

---

## 🔧 Troubleshooting

### "python3: command not found"
- **Windows:** Use `python` instead of `python3`
- **Linux:** Install Python: `sudo apt install python3`

### "pip: command not found"
```bash
# Linux/Mac:
sudo apt install python3-pip   # Ubuntu/Debian
brew install python3           # Mac

# Windows:
python -m ensurepip --upgrade
```

### "Permission denied" on Linux
```bash
chmod +x *.py
```

### Database not found
```bash
# Make sure you ran setup first:
python3 setup_commandbrain.py
# Or if installed via pip:
commandbrain-setup
```

### Colors not showing on Windows
- Use Windows Terminal (recommended) instead of CMD
- Or Update Windows 10 to latest version
- Colors will work in WSL

---

## 🎯 Post-Installation

### What Commands Did You Get?

Check [WHATS_INCLUDED.md](WHATS_INCLUDED.md) to see:
- What's in the default installation (~30 basic Linux commands)
- What's in the optional Kali tools (~30 security tools)
- How to tell what you have installed

### Add Kali Tools (Optional):
**Only for security professionals/students!**

```bash
python3 add_kali_tools.py
# Or if installed via pip:
commandbrain-kali
```

See [WHATS_INCLUDED.md](WHATS_INCLUDED.md) for the full list of Kali tools.

### Import Custom Commands (Optional):
```bash
python3 import_commands.py
# Or if installed via pip:
commandbrain-import
```

### Test Installation:
```bash
commandbrain search ssh
commandbrain list
commandbrain stats
```

---

## 📍 Where is the Database?

The database is stored at:
- **Linux/Mac:** `~/.commandbrain.db`
- **Windows:** `C:\Users\YourName\.commandbrain.db`

### Backup your database:
```bash
# Linux/Mac:
cp ~/.commandbrain.db ~/commandbrain_backup.db

# Windows:
copy %USERPROFILE%\.commandbrain.db %USERPROFILE%\commandbrain_backup.db
```

---

## 🚀 Quick Start After Installation

```bash
# Search for commands
commandbrain search network

# Detailed view
commandbrain search -d ssh

# List all categories
commandbrain list

# Add a command
commandbrain add

# Show statistics
commandbrain stats
```

---

## Need Help?

Check the [README.md](README.md) for full usage documentation!

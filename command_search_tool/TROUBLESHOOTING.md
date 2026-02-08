# CommandBrain Troubleshooting Guide

## Commands Not Found After Installation

### Symptom
After running the installer, you get:
```
cb: command not found
```

### Solution (Linux/Mac/WSL)

**Option 1: Reload Your Shell (Easiest)**
```bash
source ~/.bashrc    # For bash users
source ~/.zshrc     # For zsh users
```

**Option 2: Close and Reopen Terminal**
- Close your current terminal window
- Open a new terminal
- Try: `cb ssh`

**Option 3: Use Full Path (Temporary)**
```bash
~/.commandbrain_env/bin/cb ssh
```

**Option 4: Manual PATH Fix**
Add this to your `~/.bashrc` or `~/.zshrc`:
```bash
export PATH="$HOME/.commandbrain_env/bin:$PATH"
```
Then reload: `source ~/.bashrc`

**Option 5: Activate Virtual Environment**
```bash
source ~/.commandbrain_env/bin/activate
cb ssh
```

---

## Windows: Commands Not Found

### Symptom
```
'cb' is not recognized as an internal or external command
```

### Solution

**Option 1: Restart Terminal**
- Close Command Prompt / PowerShell
- Open a new one
- Try: `cb ssh`

**Option 2: Reinstall**
```cmd
pip uninstall commandbrain
install_windows.bat
```

**Option 3: Manual Install**
```cmd
cd command_search_tool
pip install -e .
commandbrain-setup
```

---

## Python Not Found

### Linux/Mac
```bash
# Ubuntu/Debian/Kali
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Mac
brew install python3
```

### Windows
1. Download: https://www.python.org/downloads/
2. Run installer
3. ✅ CHECK: "Add Python to PATH"
4. Restart computer
5. Verify: `python --version`

---

## Database Errors

### "Database not found"
```bash
# Run setup again:
commandbrain-setup

# Or on Linux with venv:
~/.commandbrain_env/bin/commandbrain-setup
```

### "Database locked"
```bash
# Close all cb instances, then:
rm ~/.commandbrain.db
commandbrain-setup
```

### "Permission denied"
```bash
# Fix permissions:
chmod 644 ~/.commandbrain.db
```

---

## Installation Failed

### "externally-managed-environment" (Linux)
This is normal on modern Linux! The installer handles this automatically by creating a virtual environment. Just run:
```bash
./install_linux.sh
```

### "pip not found"
```bash
# Ubuntu/Debian:
sudo apt install python3-pip

# Mac:
brew install python3

# Windows:
# Python should include pip - reinstall Python with "Add to PATH" checked
```

### "Permission denied" on install_linux.sh
```bash
chmod +x install_linux.sh
./install_linux.sh
```

---

## Can't Find Database File

Database location:
- **Linux/Mac:** `~/.commandbrain.db`
- **Windows:** `C:\Users\YourName\.commandbrain.db`

To verify it exists:
```bash
# Linux/Mac:
ls -la ~/.commandbrain.db

# Windows:
dir %USERPROFILE%\.commandbrain.db
```

---

## Fuzzy Search Not Working

Make sure you have the latest version:
```bash
./update_linux.sh    # Linux/Mac
update_windows.bat   # Windows
```

Fuzzy search requires Python 3.6+:
```bash
python3 --version    # Should be 3.6 or higher
```

---

## Colors Not Showing (Windows)

Windows 10+ required for colors. If you're on older Windows:
- Colors won't work, but everything else will
- Consider upgrading to Windows 10/11

---

## Testing Your Installation

### Quick Test
```bash
cb --stats
```
Should show:
```
Total commands: 30 (or more)
Categories: 10+
Database: /path/to/.commandbrain.db
```

### Test Search
```bash
cb ssh
```
Should show SSH command information.

### Test Fuzzy Search
```bash
cb graep    # Typo!
```
Should suggest "grep"

---

## Complete Reinstall (Clean Slate)

### Linux/Mac
```bash
# Uninstall
./uninstall_linux.sh

# Reinstall
./install_linux.sh
```

### Windows
```bat
REM Uninstall
uninstall_windows.bat

REM Reinstall
install_windows.bat
```

---

## Still Having Problems?

1. **Check Python version:** `python3 --version` (needs 3.6+)
2. **Check if installed:** `pip list | grep commandbrain`
3. **Check database:** `ls -la ~/.commandbrain.db`
4. **Try manual install:**
   ```bash
   pip install -e .
   commandbrain-setup
   ```
5. **Check PATH:**
   ```bash
   echo $PATH | grep commandbrain
   ```

---

## Getting Help

- Check `README.md` for installation guide
- See `INSTALL.md` for detailed instructions
- Ask your instructor
- Check the GitHub issues (if applicable)

---

## Common Mistakes

❌ **Forgetting to reload shell** after installation  
✅ Run: `source ~/.bashrc`

❌ **Not activating Python's "Add to PATH"** on Windows  
✅ Reinstall Python with this option checked

❌ **Using `python` instead of `python3`** on Linux  
✅ Use `python3` command

❌ **Running scripts without `./`** on Linux  
✅ Use: `./install_linux.sh` not `install_linux.sh`

❌ **Scripts not executable** on Linux  
✅ Run: `chmod +x install_linux.sh`

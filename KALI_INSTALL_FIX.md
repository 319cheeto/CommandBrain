# Kali Linux Installation Quick Fix Guide

## 🔥 Having Installation Problems on Kali? Start Here!

### The 3-Step Fix (Works 95% of the Time)

```bash
# Step 1: Navigate to where you cloned the repository
cd CommandBrain

# Step 1.5: Complete uninstall
./uninstall_linux.sh

# Step 2: Install required packages
sudo apt update
sudo apt install -y python3 python3-pip python3-venv

# Step 3: Fresh install
./install_linux.sh

# Step 4: Activate it NOW
source ~/.bashrc
```

### Test It Works
```bash
cb ssh
```

If you see SSH commands, **YOU'RE DONE!** 🎉

---

## 🔍 Still Not Working? Run Diagnostics

We have a comprehensive test script that will find the issue:

```bash
chmod +x test_install.sh
./test_install.sh
```

This will:
- Uninstall and reinstall CommandBrain 3 times
- Test every component after each install
- Generate a detailed log file
- Show exactly what's failing

Review the log file it creates: `install_test_YYYYMMDD_HHMMSS.log`

---

## ⚠️ Common Kali-Specific Issues

### Issue #1: "cb: command not found" After Install

**Cause:** Shell hasn't loaded the new PATH yet

**Fix:**
```bash
source ~/.bashrc
# OR just close and reopen terminal
```

**Test:**
```bash
echo $PATH | grep commandbrain
# Should show: /home/youruser/.commandbrain_env/bin
```

---

### Issue #2: "externally-managed-environment" Error

**Cause:** Kali (based on Debian 12+) uses PEP 668 to prevent system-wide pip

**Why our installer handles this:**
- We automatically create a virtual environment at `~/.commandbrain_env`
- All packages install there, NOT system-wide
- This is the CORRECT way to do it in modern Kali

**If you still see this error:**
```bash
# The installer should auto-create the venv, but if not:
python3 -m venv ~/.commandbrain_env
source ~/.commandbrain_env/bin/activate
./install_linux.sh
```

---

### Issue #3: "python3-venv is not installed"

**Cause:** Minimal Kali installations don't include venv module

**Fix:**
```bash
sudo apt update
sudo apt install -y python3-venv
./install_linux.sh
```

The installer now auto-detects this and installs it for you!

---

### Issue #4: Database Not Created

**Symptoms:**
```bash
cb ssh
# Returns: Database not found
```

**Fix:**
```bash
# Manually create the database:
source ~/.commandbrain_env/bin/activate
commandbrain-setup

# Or use Python directly:
python3 setup_commandbrain.py
```

**Verify:**
```bash
ls -lh ~/.commandbrain.db
# Should show a file ~XX KB in size
```

---

### Issue #5: Multiple Shell Configs

**Problem:** Kali might use different shells (bash, zsh, etc.)

**Check which shell you're using:**
```bash
echo $SHELL
```

**If using ZSH:**
```bash
# Add to ~/.zshrc instead:
echo 'export PATH="$HOME/.commandbrain_env/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**If using Fish:**
```bash
# Add to ~/.config/fish/config.fish:
set -gx PATH $HOME/.commandbrain_env/bin $PATH
```

---

## 🛠️ Manual Installation (Last Resort)

If the automated installer keeps failing:

```bash
# 1. Create virtual environment
python3 -m venv ~/.commandbrain_env

# 2. Activate it
source ~/.commandbrain_env/bin/activate

# 3. Navigate to project
cd ~/path/to/command_search_tool

# 4. Install
pip3 install -e .

# 5. Setup database
commandbrain-setup

# 6. Add to PATH (choose your shell config)
echo 'export PATH="$HOME/.commandbrain_env/bin:$PATH"' >> ~/.bashrc

# 7. Reload config
source ~/.bashrc

# 8. Test
cb ssh
```

---

## 📝 Getting Help

If none of the above works:

1. **Run the test script:**
   ```bash
   ./test_install.sh
   ```

2. **Collect this info:**
   - Your Kali version: `cat /etc/os-release`
   - Python version: `python3 --version`
   - Shell: `echo $SHELL`
   - The log file from test_install.sh

3. **Check the detailed log:**
   - Open `install_test_YYYYMMDD_HHMMSS.log`
   - Look for red "✗ FAIL" markers
   - Share the relevant error sections

---

## ✅ Verification Checklist

After installation, verify everything works:

- [ ] `cb --help` shows help text
- [ ] `cb ssh` shows SSH command info
- [ ] `commandbrain-setup` runs without errors
- [ ] `ls ~/.commandbrain.db` shows database file
- [ ] `ls ~/.commandbrain_env` shows virtual environment
- [ ] `echo $PATH` includes `.commandbrain_env/bin`
- [ ] `which cb` shows path to cb executable

All checked? **You're all set!** 🎊

---

## 🎓 For Instructors/TAs

If a student reports installation issues:

1. Ask them to run: `./test_install.sh`
2. Request the log file
3. Look for patterns:
   - PATH not updating → Shell config issue
   - Database not found → Permissions or setup failed
   - Command not found → Virtual env not activated

**Most common student mistake:** Not running `source ~/.bashrc` after install!

Add this to your installation instructions:
```bash
./install_linux.sh
source ~/.bashrc   # ← CRITICAL! Tell students to do this!
cb ssh             # Test it works
```

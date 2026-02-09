# CommandBrain - Dead Simple Installation

**For students who just want this to work with ZERO hassle.**

---

## Windows Installation (3 Steps)

### Step 1: Get the files

**Option A: Download ZIP (Easier)**
1. Go to: https://github.com/319cheeto/CommandBrain
2. Click the green "Code" button
3. Click "Download ZIP"
4. Extract the ZIP file to your Documents folder
5. You should have a folder called `CommandBrain-master`
6. Rename it to just `CommandBrain`

**Option B: Use Git (If you have it)**
```powershell
cd Documents
git clone https://github.com/319cheeto/CommandBrain.git
```

### Step 2: Run the installer

1. Open the `CommandBrain` folder
2. Double-click: `install_windows.bat`
3. Wait for it to finish (it will ask about Kali tools - type `n` if unsure)
4. **Close the window when done**

### Step 3: Test it works

1. Open a NEW Command Prompt (Start → type "cmd" → press Enter)
2. Type: `cb ssh`
3. You should see information about the SSH command

**✅ If you see SSH info = SUCCESS!**

**❌ If you see "command not found":**
- Did you open a NEW window? (Old windows won't work)
- Run: `test_cb.bat` to diagnose the problem

---

## Linux/Mac/Kali Installation (4 Steps)

### Step 1: Get the files

```bash
cd ~
git clone https://github.com/319cheeto/CommandBrain.git
cd CommandBrain
```

**Don't have git?**
```bash
# Ubuntu/Debian/Kali:
sudo apt install git

# Mac:
brew install git
```

### Step 2: Run the installer

```bash
chmod +x install_linux.sh
./install_linux.sh
```

**Note:** `chmod +x` makes the file executable (runnable). You only do this once.

**If you get "Permission denied":**
```bash
# Try with sudo:
sudo chmod +x install_linux.sh
./install_linux.sh

# Or run it with bash directly:
bash install_linux.sh
```

Wait for it to finish. It will ask about Kali tools - type `n` if you're not sure.

### Step 3: Reload your terminal

**This is the step everyone forgets!**

Pick ONE of these options:

**Option A: Reload current terminal** (Faster)
```bash
source ~/.bashrc
```

**Option B: Close and reopen terminal** (Simpler)
- Just close your terminal window
- Open a new one
- The `cb` command will now work

**What does "source ~/.bashrc" mean?**
- Your terminal reads settings from a file called `.bashrc` when it starts
- The installer added CommandBrain to that file
- "source" tells your terminal to re-read that file NOW
- Without this, you'd have to close and reopen the terminal

### Step 4: Test it works

```bash
cb ssh
```

You should see information about the SSH command.

**✅ If you see SSH info = SUCCESS!**

**❌ If you see "command not found":**
- Did you run `source ~/.bashrc`? (Or close/reopen terminal?)
- Run: `./test_cb.sh` to diagnose the problem

---

## Quick Test Script

**Windows:**
```powershell
test_cb.bat
```

**Linux/Mac:**
```bash
chmod +x test_cb.sh
./test_cb.sh
```

This runs automatic tests and tells you exactly what's wrong.

---

## Using CommandBrain

Once installed, it's super simple:

```bash
cb ssh                    # Find SSH command
cb find files             # Search by purpose
cb network scan           # Multi-word search
cb password crack         # Find password cracking tools
cb --help                 # Show all options
```

That's it! Just type `cb` followed by what you want to find.

---

## Common Student Questions

**Q: Do I type "cb" or "commandbrain"?**
A: Both work! `cb` is shorter and easier. Use that.

**Q: Where do I type these commands?**
A: In your terminal (Linux/Mac) or Command Prompt (Windows)

**Q: Do I need to be in the CommandBrain folder?**
A: NO! After installation, `cb` works from anywhere.

**Q: What if I get "command not found"?**
A: You forgot to reload your terminal. Run: `source ~/.bashrc` (Linux) or open a NEW Command Prompt (Windows)

**Q: Do I need internet to use this?**
A: NO! It works completely offline after installation.

**Q: Should I add Kali tools during installation?**
A: Only if you're doing security/penetration testing. If you're just learning basic Linux, say `n` (no).

**Q: Can I add Kali tools later?**
A: Yes! Just run: `commandbrain-kali`

**Q: How do I uninstall?**
A: Windows: Run `uninstall_windows.bat`
   Linux: Run `./uninstall_linux.sh`

**Q: How do I update CommandBrain?**
A: Windows: Run `update_windows.bat`
   Linux: Run `./update_linux.sh`

---

## Still Not Working?

1. Run the test script:
   - Windows: `test_cb.bat`
   - Linux: `./test_cb.sh`

2. Check: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

3. Ask your instructor

4. Open an issue: https://github.com/319cheeto/CommandBrain/issues

---

**Remember: The hardest part is reloading your terminal after installation. That's it!**

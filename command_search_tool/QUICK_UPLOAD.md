# 🚀 Quick GitHub Upload Commands

Copy and paste these commands in order!

---

## Step 1: Open Command Prompt

```bash
cd c:\Users\joshu\OneDrive\Documents\GitHub\command_search_tool
```

---

## Step 2: Create GitHub Repo

1. Go to: **https://github.com/new**
2. Name: **CommandBrain**
3. Description: **Offline Linux command reference for cybersecurity students**
4. **Public** ✓
5. Click **"Create repository"**

---

## Step 3: Push Your Code (Run These Commands)

### Initialize Git:
```bash
git init
```

### Remove test files (optional cleanup):
```bash
del cb 2>nul
del cb.bat 2>nul
del cb.py 2>nul
```

### Add all files:
```bash
git add .
```

### Check what will be uploaded:
```bash
git status
```

**Should see:**
- ✅ commandbrain.py
- ✅ enhance_slang_tags.py ⭐
- ✅ install_linux.sh
- ✅ install_windows.bat
- ✅ All .md files
- ✅ .gitignore
- ✅ LICENSE

**Should NOT see:**
- ❌ __pycache__/
- ❌ test_venv/
- ❌ *.pyc files

### Commit:
```bash
git commit -m "Initial commit - CommandBrain v2.0 with purpose-based search"
```

### Connect to GitHub (REPLACE YourUsername!):
```bash
git remote add origin https://github.com/YourUsername/CommandBrain.git
```

### Push to GitHub:
```bash
git branch -M main
git push -u origin main
```

---

## ✅ Done! Your Code is on GitHub!

Visit: **https://github.com/YourUsername/CommandBrain**

---

## 📢 Share This Link With Students:

```
Installation Instructions:

Linux/Mac/Kali:
  git clone https://github.com/YourUsername/CommandBrain.git
  cd CommandBrain
  ./install_linux.sh

Windows:
  git clone https://github.com/YourUsername/CommandBrain.git
  cd CommandBrain
  install_windows.bat

Then type: cb [anything]

Examples:
  cb brute force      → Password attack tools
  cb network scan     → nmap, masscan
  cb password crack   → john, hashcat, hydra
  cb web hack         → burpsuite, sqlmap
```

---

## 🔄 When You Make Changes Later:

```bash
cd c:\Users\joshu\OneDrive\Documents\GitHub\command_search_tool
git add .
git commit -m "Describe your changes here"
git push
```

Students update with:
```bash
cd CommandBrain
./update_linux.sh     # Linux/Mac
update_windows.bat    # Windows
```

---

## 🆘 Troubleshooting

**"fatal: not a git repository"**
```bash
git init
```

**"Permission denied"**
```bash
git remote set-url origin https://github.com/YourUsername/CommandBrain.git
```

**"Updates were rejected"**
```bash
git pull origin main --rebase
git push
```

---

## 📝 Optional: Add Topics to Your Repo

1. Go to your repo on GitHub
2. Click ⚙️ "About" (top right)
3. Add topics:
   - cybersecurity
   - linux
   - education
   - kali-linux
   - command-line
   - security-tools

This helps other instructors find your project!

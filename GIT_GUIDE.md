# Git Quick Guide for Students

**Git is a tool that downloads code from GitHub and keeps it updated.**

You only need to install it once, then you can easily update CommandBrain anytime.

---

## Installing Git (One-Time Setup)

### Debian/Ubuntu/Kali Linux

```bash
sudo apt update
sudo apt install git -y
```

**What this does:**
- `sudo` = Run as administrator (you may need to enter your password)
- `apt update` = Refresh the list of available software
- `apt install git` = Install git
- `-y` = Automatically say "yes" to the installation

**To verify it worked:**
```bash
git --version
```

You should see something like: `git version 2.x.x`

---

### Other Linux Distributions

**Fedora/Red Hat/CentOS:**
```bash
sudo dnf install git -y
```

**Arch Linux:**
```bash
sudo pacman -S git
```

**Alpine Linux:**
```bash
sudo apk add git
```

---

## Getting CommandBrain with Git

**First time (cloning):**
```bash
git clone https://github.com/319cheeto/CommandBrain.git
cd CommandBrain
bash install_linux.sh
source ~/.bashrc
```

---

## Updating CommandBrain (Easy!)

When CommandBrain gets new features or bug fixes, update with one command:

```bash
cd CommandBrain
git pull
```

**That's it!** The latest version is now on your computer.

**If you get an error about "local changes":**
```bash
git stash        # Save your local changes
git pull         # Get the updates
git stash pop    # Restore your changes (optional)
```

**Simpler option if you don't care about local changes:**
```bash
git reset --hard
git pull
```

---

## Common Student Questions

**Q: Do I need internet to use git?**  
A: You need internet to download/update, but CommandBrain works offline after installation.

**Q: What if I don't want to use git?**  
A: You can download the ZIP file instead:
1. Go to: https://github.com/319cheeto/CommandBrain
2. Click the green "Code" button
3. Click "Download ZIP"
4. Extract it
5. Run `bash install_linux.sh`

**But updates are harder without git** - you'd have to download the ZIP again each time.

**Q: What's the difference between git clone and git pull?**  
A:
- `git clone` = First time download (creates a new folder)
- `git pull` = Update existing folder with latest changes

**Q: I get "command not found" when typing git**  
A: Git isn't installed. Run the installation commands above.

**Q: Can I use git for other projects?**  
A: YES! Git is used for almost all programming projects. Learning it now will help you in every CS class.

**Q: Does git cost money?**  
A: NO! Git and GitHub are free.

---

## Updating CommandBrain - Step by Step

**Every time you want the latest version:**

```bash
# 1. Go to the CommandBrain folder
cd CommandBrain

# 2. Get the latest updates
git pull

# 3. If there were changes to the installer or database, re-run:
bash install_linux.sh
source ~/.bashrc

# 4. Test it
cb ssh
```

**Pro tip:** Most updates don't need reinstalling. Just `git pull` is enough!

---

## Checking for Updates

**See if updates are available:**
```bash
cd CommandBrain
git fetch
git status
```

If it says "Your branch is behind", there are updates available. Run `git pull` to get them.

---

## Troubleshooting

**Error: "fatal: not a git repository"**  
You're not in the CommandBrain folder. Run: `cd CommandBrain`

**Error: "Permission denied"**  
You don't have permission to write to this folder. Try with sudo: `sudo git pull`

**Error: "Your local changes would be overwritten"**  
You edited files. Either:
- Save your changes: `git stash`
- Discard your changes: `git reset --hard`
Then run `git pull` again.

**Updates aren't showing up?**  
Make sure you're pulling from the right place:
```bash
git remote -v
```
Should show: `https://github.com/319cheeto/CommandBrain.git`

---

## Why Use Git?

✅ **Easy updates** - One command gets the latest version  
✅ **See what changed** - `git log` shows update history  
✅ **Revert if needed** - Can go back to older versions  
✅ **Industry standard** - You'll use it in every tech job  
✅ **Free and fast** - Downloads only what changed  

---

**TL;DR (Too Long; Didn't Read):**

```bash
# Install git (one time):
sudo apt install git -y

# Get CommandBrain (first time):
git clone https://github.com/319cheeto/CommandBrain.git
cd CommandBrain

# Update CommandBrain (anytime):
cd CommandBrain
git pull
```

**That's it!** 🎉

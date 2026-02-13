# CommandBrain

**Offline Linux & security command reference for cybersecurity students.**

Search by *purpose*, not by memorizing command names.

```
cb brute force        → hydra, john, hashcat, medusa, ncrack
cb network scan       → nmap, masscan, rustscan
cb web hack           → burpsuite, sqlmap, nikto, zaproxy
cb sniffing           → wireshark, tcpdump, bettercap
cb exploit            → metasploit, msfvenom, searchsploit
cb password cracking  → john, hashcat, hydra
cb reverse shell      → netcat, socat, msfvenom
cb privilege escalation → linpeas, winpeas
cb wifi hack          → aircrack-ng, wifite, reaver
cb active directory   → bloodhound, crackmapexec, netexec, mimikatz
cb steganography      → steghide, zsteg, stegcracker
```

Just type `cb` + what you want to do.

---

## Table of Contents

- [Installing](#installing)
- [Using CommandBrain](#using-commandbrain)
- [Uninstalling](#uninstalling)
- [Updating](#updating)
- [Troubleshooting](#troubleshooting)
- [What's Included](#whats-included)
- [FAQ](#faq)
- [For Instructors](#for-instructors)

---

## Installing

There are **two ways** to install. Pick ONE.

> **Requirements:** Python 3.6+ and Git (both pre-installed on Kali Linux).

### Option A — Use the Installer (recommended for most users)

This is the easiest way. The installer does everything for you.

**1. Clone the repo:**
```bash
git clone https://github.com/319cheeto/CommandBrain.git
cd CommandBrain
```

**2. Run the installer:**
```bash
bash install.sh
```

**3. Answer the prompt — type `y` to include security tools (you want this):**
```
Include Kali security tools? (y/n) [y]: y
```

**4. Reload your shell** (you must do this or `cb` won't be found):

| Your shell | Run this |
|------------|----------|
| **Kali (ZSH)** | `source ~/.zshrc` |
| **Bash** | `source ~/.bashrc` |
| **Fish** | `source ~/.config/fish/config.fish` |

> **Not sure which shell you have?** Run: `echo $SHELL`
> Kali uses ZSH by default. Ubuntu/Debian use Bash by default.

**5. Test it:**
```bash
cb ssh
```

If you see results, you're done!

---

### Option B — Install with pip (manual, no installer)

If you prefer to install manually without the script.

**1. Clone the repo:**
```bash
git clone https://github.com/319cheeto/CommandBrain.git
cd CommandBrain
```

**2. Create a virtual environment and install:**
```bash
python3 -m venv ~/.commandbrain_env
source ~/.commandbrain_env/bin/activate
pip install .
```

**3. Set up the database:**
```bash
cb --setup --kali
```

> Without `--kali` you only get 30 basic Linux commands.
> With `--kali` you get **all 350+ commands** including security tools.

**4. Add the venv to your PATH** (so `cb` works every time you open a terminal):

For **ZSH** (Kali default):
```bash
echo 'export PATH="$HOME/.commandbrain_env/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

For **Bash** (Ubuntu/Debian default):
```bash
echo 'export PATH="$HOME/.commandbrain_env/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

**5. Test it:**
```bash
cb ssh
```

---

### Option C — Download ZIP (no Git required)

If you don't have Git or can't clone:

1. Go to: https://github.com/319cheeto/CommandBrain/archive/refs/heads/master.zip
2. Download and extract the ZIP
3. Open a terminal in the extracted folder
4. Follow Option A (step 2) or Option B (step 2)

---

## Using CommandBrain

### Search by purpose (the main feature)

Just type `cb` followed by what you want to do. **No quotes needed.**

```bash
cb ssh                    # find SSH-related commands
cb network scan           # find network scanning tools
cb password cracking      # find password cracking tools
cb brute force            # find brute-force tools
cb web hack               # find web security tools
cb file permissions       # find chmod, chown, setfacl
cb encode decode          # find base64, xxd, hexdump
cb steganography          # find steghide, zsteg, stegcracker
cb active directory       # find AD attack tools
```

### Detailed view — see examples, usage, and related commands

```bash
cb -d nmap                # show EVERYTHING about nmap
cb -d hashcat             # full details with all examples
```

### Examples only — just show me how to use it

```bash
cb -e grep                # examples for grep
cb -e nmap                # example commands for nmap
```

### Compare two commands side by side

```bash
cb --compare nmap masscan
cb --compare john hashcat
cb --compare netcat socat
```

### Workflows — step-by-step pentest chains

```bash
cb --workflows            # list all 5 workflows
cb --workflow web-pentest  # step-by-step web pentest guide
cb --workflow network-recon
cb --workflow password-attack
cb --workflow wireless-pentest
cb --workflow post-exploitation
```

### Browse and explore

```bash
cb --list                 # list all categories
cb --stats                # show database statistics
cb --all                  # dump every single command
```

### Search by specific field

```bash
cb -t name nmap           # search names only
cb -t category Exploitation
cb -t tags pivot          # search tags only
cb -t description "brute force"
```

### Add your own commands

```bash
cb --add                  # interactive prompt — walks you through it
cb --import-file cmds.txt # bulk import from a text file
```

### Add notes to existing commands

```bash
cb --update               # add your personal notes to a command
```

### Disable colors (if your terminal is weird)

```bash
cb --no-color ssh         # no ANSI colors for this search
export NO_COLOR=1         # disable colors permanently (add to your shell config)
```

---

## Uninstalling

### Option A — Use the installer's uninstall (easiest)

You need to be in the CommandBrain folder (or have the `install.sh` file):

```bash
cd CommandBrain
bash install.sh --uninstall
```

This will:
- Remove the virtual environment (`~/.commandbrain_env`)
- Remove PATH entries from all shell configs (`.bashrc`, `.zshrc`, `.config/fish/config.fish`)
- Ask if you want to delete the database (`~/.commandbrain.db`)

Then close and reopen your terminal.

### Option B — Uninstall manually

If you lost the CommandBrain folder or can't find `install.sh`:

**1. Delete the virtual environment:**
```bash
rm -rf ~/.commandbrain_env
```

**2. Delete the database (optional — keeps your custom commands if you skip this):**
```bash
rm -f ~/.commandbrain.db
```

**3. Remove the PATH line from your shell config:**

For **ZSH** (Kali):
```bash
nano ~/.zshrc
```
Find and delete the line that says `export PATH="$HOME/.commandbrain_env/bin:$PATH"` and the `# CommandBrain` comment above it. Save (`Ctrl+O`, `Enter`, `Ctrl+X`).

For **Bash**:
```bash
nano ~/.bashrc
```
Same thing — find and delete the CommandBrain lines.

**4. Reload your shell:**
```bash
source ~/.zshrc    # or source ~/.bashrc
```

---

## Updating

### Option A — Use the installer

```bash
cd CommandBrain
bash install.sh --update
```

This pulls the latest code from GitHub and reinstalls. Your custom commands and database are preserved.

### Option B — Update manually with Git

```bash
cd CommandBrain
git pull
source ~/.commandbrain_env/bin/activate
pip install .
cb --setup --kali
```

> Running `cb --setup --kali` after update loads any new commands added to the tool.
> Your custom commands are kept — setup only adds, never deletes.

---

## Troubleshooting

### "command not found" after install

This means your shell can't find `cb`. Try these in order:

**1. Reload your shell config:**
```bash
source ~/.zshrc       # Kali (ZSH)
source ~/.bashrc      # Ubuntu/Debian (Bash)
```

**2. Or just close and reopen your terminal.**

**3. Run the diagnostic:**
```bash
bash install.sh --diagnose
```
This checks your Python, virtual environment, database, and PATH — and tells you exactly what's wrong.

**4. Verify the install manually:**
```bash
ls ~/.commandbrain_env/bin/cb     # should exist
cat ~/.zshrc | grep commandbrain  # should show a PATH line
```

---

### "Database not found" error

The database hasn't been created yet, or was deleted:

```bash
cb --setup --kali    # create database with ALL tools (recommended)
cb --setup           # create database with basic commands only
```

---

### Colors look broken or garbled

```bash
cb --no-color ssh               # disable for one search
export NO_COLOR=1               # disable permanently
```

Add `export NO_COLOR=1` to your `.zshrc` or `.bashrc` to make it permanent.

---

### Install is failing

Common fixes:

```bash
# If python3-venv is missing (Ubuntu/Debian):
sudo apt install python3-venv python3-pip

# If you get permission errors:
# DON'T use sudo with pip. The installer creates a venv that doesn't need root.

# If pip install fails:
python3 -m pip install --upgrade pip
```

---

## What's Included

**30 core Linux commands** (always installed):
ls, cd, cp, mv, rm, mkdir, chmod, chown, find, grep, sed, awk,
cat, head, tail, ssh, scp, ping, netstat, ip, ps, top, df, du,
tar, wget, curl, systemctl, journalctl, man

**350+ security & system tools** (included with `--kali` flag):
Information Gathering, Vulnerability Analysis, Web Application Testing,
Database Assessment, Password Attacks, Wireless Attacks, Exploitation,
Sniffing & Spoofing, Post-Exploitation, Reverse Engineering, Forensics,
Social Engineering, Steganography, Encoding/Decoding — covering the full Kali Linux toolkit and more.

Every command includes: purpose-based search tags, usage syntax, real examples,
related commands, and student-friendly descriptions.

**5 pentest workflows:** web-pentest, network-recon, password-attack, wireless-pentest, post-exploitation

---

## Project Structure

```
CommandBrain/
  commandbrain.py       # All application logic
  data.py               # All data (commands, tools, slang, workflows)
  setup.py              # pip packaging
  install.sh            # Installer (install, uninstall, update, diagnose)
  README.md             # This file
  LICENSE               # MIT License
```

That's it. Four core files + docs.

---

## FAQ

**Q: `cb` or `commandbrain`?**
Both work. `cb` is shorter. They're the same command.

**Q: Do I need internet?**
No. Everything is offline after install. The database is local.

**Q: How do I add Kali tools if I skipped them during install?**
```bash
cb --setup --kali
```
Your existing commands are kept — this just adds the security tools.

**Q: How do I update to the latest version?**
```bash
cd CommandBrain && bash install.sh --update
```

**Q: Can I add my own commands?**
Yes! `cb --add` for interactive, or `cb --import-file yourfile.txt` for bulk import.

**Q: What if I break something?**
```bash
bash install.sh --diagnose   # find out what's wrong
bash install.sh --uninstall  # remove everything
bash install.sh              # reinstall fresh
```

**Q: What shells are supported?**
Bash, ZSH, and Fish. The installer auto-detects and configures whichever you use.

---

## For Instructors

Students search by *what they want to do*, not command names they haven't memorized yet.

- Works **100% offline** — perfect for closed lab environments
- Custom commands can be added per student with `cb --add`
- Use `--import-file` to distribute a class-specific command list
- Workflows teach methodology: `cb --workflow web-pentest`
- No external dependencies — just Python 3.6+ (standard library)

---

## License

MIT License — free for educational use and modification.

---

## Acknowledgments

CommandBrain was designed and directed by **Joshua Sears**, with significant development assistance from **GitHub Copilot (Claude)**. The project architecture, feature requirements, user experience design, data accuracy review, and all testing were led by Joshua. AI-assisted development was used for code generation, data expansion, and implementation of features.

This project demonstrates that powerful, purpose-built tools can be created by domain experts — even without years of software engineering experience — when human expertise is combined with AI assistance. If you're an instructor or student with an idea for a tool that could help people learn, **you can build it too.**

**Created by Joshua Sears** | [github.com/319cheeto/CommandBrain](https://github.com/319cheeto/CommandBrain)

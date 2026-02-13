# CommandBrain

**Offline Linux & security command reference for cybersecurity students.**

Search by *purpose*, not by memorizing command names.

```
cb brute force        → hydra, john, hashcat
cb network scan       → nmap, masscan
cb web hack           → burpsuite, sqlmap, nikto
cb sniffing           → wireshark, tcpdump
cb exploit            → metasploit, searchsploit
cb password cracking  → john, hashcat, hydra
```

Just type `cb` + what you want to do.

---

## Installation

### Prerequisites

- **Python 3.6+** (pre-installed on Kali/most Linux)
- **Git** (optional — you can download the ZIP instead)

### Step 1 — Get the code

```bash
git clone https://github.com/319cheeto/CommandBrain.git
cd CommandBrain
```

Or [download the ZIP](https://github.com/319cheeto/CommandBrain/archive/refs/heads/master.zip) and extract it.

### Step 2 — Run the installer

**Linux / Mac / WSL / Kali:**
```bash
bash install.sh
```

**Windows:**
```
install_windows.bat
```

The installer will:
- Create a virtual environment at `~/.commandbrain_env`
- Install CommandBrain via pip
- Set up the database with 30 Linux commands + 22 Kali tools
- Configure your shell PATH (Bash, ZSH, and Fish are all detected automatically)

### Step 3 — Reload your shell

| Shell | Command |
|-------|---------|
| Kali (ZSH) | `source ~/.zshrc` |
| Bash | `source ~/.bashrc` |
| Fish | `source ~/.config/fish/config.fish` |
| Windows | Open a new Command Prompt |

Or just close and reopen your terminal.

---

## Usage

### Search by purpose (the main feature)
```bash
cb ssh                    # search for a command
cb network scan           # multi-word, no quotes needed
cb password cracking      # finds john, hashcat, hydra
cb brute force            # finds hydra, john
cb web hack               # finds burpsuite, sqlmap, nikto
```

### Detailed view
```bash
cb -d nmap                # full examples, usage, related commands
cb -e grep                # examples only
```

### Compare commands
```bash
cb --compare nmap masscan
```

### Workflows (chained pentest steps)
```bash
cb --workflows            # list all workflows
cb --workflow web-pentest  # show the steps
```

### Categories and stats
```bash
cb --list                 # list all categories
cb --stats                # database statistics
cb --all                  # show every command
```

### Add your own
```bash
cb --add                  # interactive prompt
cb --import-file cmds.txt # bulk import from file
```

### Manage installation
```bash
bash install.sh --update     # pull latest + reinstall
bash install.sh --diagnose   # check installation health
bash install.sh --uninstall  # clean removal
```

---

## What's Included

**30 core Linux commands** (always installed):
ls, cd, cp, mv, rm, mkdir, chmod, chown, find, grep, sed, awk,
cat, head, tail, ssh, scp, ping, netstat, ip, ps, top, df, du,
tar, wget, curl, systemctl, journalctl, man

**22 Kali security tools** (optional, asked during install):
nmap, metasploit, burpsuite, sqlmap, hydra, john, hashcat, aircrack-ng,
wireshark, tcpdump, nikto, gobuster, dirb, enum4linux, netcat,
searchsploit, wpscan, responder, crackmapexec, bloodhound, ettercap, masscan

**5 pentest workflows:** web-pentest, network-recon, password-attack, wireless-pentest, post-exploitation

---

## Project Structure

```
CommandBrain/
  commandbrain.py       # All application logic
  data.py               # All data (commands, tools, slang, workflows)
  setup.py              # pip packaging
  install.sh            # Universal installer (Linux/Mac/WSL)
  install_windows.bat   # Windows installer
  README.md             # This file
  LICENSE               # MIT License
```

That's it. Four core files + docs.

---

## Troubleshooting

**"command not found" after install:**
- Kali/ZSH: `source ~/.zshrc`
- Bash: `source ~/.bashrc`
- Or close and reopen terminal
- Run `bash install.sh --diagnose` for a full health check

**"Database not found":**
```bash
cb --setup --kali    # re-create with Kali tools
cb --setup           # re-create without Kali tools
```

**Colors look broken:**
```bash
cb --no-color ssh    # disable colors for this search
export NO_COLOR=1    # disable globally (add to shell config)
```

---

## FAQ

**Q: `cb` or `commandbrain`?**
Both work. `cb` is shorter.

**Q: Do I need internet?**
No. Everything is offline after install.

**Q: How do I add Kali tools later?**
`cb --setup --kali` (your existing commands are kept)

**Q: How do I update?**
`bash install.sh --update`

**Q: Can I add my own commands?**
`cb --add` for interactive, or `cb --import-file yourfile.txt` for bulk.

---

## For Instructors

Students search by *what they want to do*, not command names they haven't memorized yet.
Custom commands and notes can be added per student. Works offline for lab environments.
Use `--import-file` to distribute a class-specific command list.

---

## License

MIT License — free for educational use and modification.

**Created by Joshua Sears** | [github.com/319cheeto/CommandBrain](https://github.com/319cheeto/CommandBrain)

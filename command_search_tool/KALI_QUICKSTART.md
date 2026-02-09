# CommandBrain - Kali Linux Quick Start

## Installation (4 Commands)

```bash
cd command_search_tool
chmod +x install_linux.sh
./install_linux.sh
source ~/.bashrc    # This reloads your terminal - IMPORTANT!
```

**What's "source ~/.bashrc"?** It reloads your terminal settings so the `cb` command works. You only do this ONCE after installation. Or just close and reopen your terminal instead!

## Test It Works

```bash
cb ssh
```

You should see SSH command information. Done! 🎉

---

## Not Working? 

### Fix #1: Reload Your Shell
```bash
source ~/.bashrc
```

### Fix #2: Install Python Dependencies
```bash
sudo apt install -y python3 python3-pip python3-venv
./install_linux.sh
```

### Fix #3: Run Diagnostics
```bash
./test_install.sh
```

This creates a detailed log showing exactly what's wrong.

---

## Usage Examples

```bash
# Search for a command
cb ssh
cb find files
cb network scan

# List all commands
cb --all

# Search by category
cb --category networking

# Search by tag
cb --tag security
```

---

## Still Stuck?

See [KALI_INSTALL_FIX.md](KALI_INSTALL_FIX.md) for detailed troubleshooting.

---

**Made with ❤️ for Kali Linux users**

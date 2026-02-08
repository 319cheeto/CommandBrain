#!/bin/bash
# CommandBrain Easy Installer for Linux/Mac/WSL
# This script sets up CommandBrain automatically

set -e  # Exit on error

echo "========================================"
echo "CommandBrain Linux/Mac Installer"
echo "========================================"
echo ""
echo "Checking prerequisites..."
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo ""
    echo "================================================================"
    echo "  PYTHON 3 NOT FOUND!"
    echo "================================================================"
    echo ""
    echo "CommandBrain requires Python 3.6 or higher."
    echo ""
    echo "HOW TO INSTALL PYTHON 3:"
    echo ""
    echo "Ubuntu/Debian/Kali:"
    echo "  sudo apt update"
    echo "  sudo apt install python3 python3-pip"
    echo ""
    echo "Red Hat/CentOS/Fedora:"
    echo "  sudo yum install python3 python3-pip"
    echo ""
    echo "Mac (with Homebrew):"
    echo "  brew install python3"
    echo ""
    echo "After installing, run this installer again."
    echo "================================================================"
    echo ""
    exit 1
fi

echo "[1/4] Python found!"
python3 --version
echo ""

# Check if we're in a virtual environment already
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "[2/4] Setting up virtual environment..."
    echo "   (Modern Linux requires this for pip packages)"
    
    # Create venv in ~/.commandbrain_env if it doesn't exist
    VENV_PATH="$HOME/.commandbrain_env"
    
    if [ ! -d "$VENV_PATH" ]; then
        # Try to create venv, catch error if python3-venv is missing
        if ! python3 -m venv "$VENV_PATH" 2>/dev/null; then
            echo ""
            echo "⚠️  python3-venv is not installed!"
            echo "   Installing it now..."
            echo ""
            if command -v apt &> /dev/null; then
                sudo apt install -y python3-venv python3-pip
            elif command -v yum &> /dev/null; then
                sudo yum install -y python3-venv
            else
                echo "   Please install python3-venv manually:"
                echo "   sudo apt install python3-venv  # Debian/Ubuntu/Kali"
                echo "   sudo yum install python3-venv  # Red Hat/CentOS"
                exit 1
            fi
            # Try again after installation
            python3 -m venv "$VENV_PATH"
        fi
        echo "   ✓ Virtual environment created at $VENV_PATH"
    else
        echo "   ✓ Using existing virtual environment"
    fi
    
    # Activate the virtual environment
    source "$VENV_PATH/bin/activate"
    echo "   ✓ Virtual environment activated"
    echo ""
else
    echo "[2/4] Virtual environment detected!"
    echo "   Using: $VIRTUAL_ENV"
    echo ""
fi

echo "[3/4] Installing CommandBrain..."
pip3 install -e .
echo ""

echo "[4/4] Setting up database..."
commandbrain-setup
echo ""
echo "Database created with ~30 essential Linux commands!"
echo ""

echo "[5/6] Enabling purpose-based search..."
echo ""
echo "Adding student-friendly slang terms (brute force, network scan, etc.)"
python3 enhance_slang_tags.py > /dev/null 2>&1
echo "✓ Students can now search by purpose/task!"
echo ""

echo "[6/6] OPTIONAL: Add Kali Security Tools?"
echo ""
echo "Kali tools include: nmap, metasploit, burpsuite, sqlmap, etc."
echo "These are for SECURITY PROFESSIONALS and PENTESTERS only."
echo ""
echo "If you just need basic Linux commands, type 'n'"
echo ""
read -p "Add Kali security tools? (y/n): " KALI
if [[ "$KALI" == "y" ]] || [[ "$KALI" == "Y" ]]; then
    echo ""
    echo "Adding 30+ Kali tools..."
    commandbrain-kali
    echo "Kali tools added!"
else
    echo ""
    echo "Skipping Kali tools. You can add them later with: commandbrain-kali"
fi
echo ""

# Add venv to PATH if not already there
if [[ -n "$VENV_PATH" ]]; then
    SHELL_RC=""
    if [[ -f "$HOME/.bashrc" ]]; then
        SHELL_RC="$HOME/.bashrc"
    elif [[ -f "$HOME/.zshrc" ]]; then
        SHELL_RC="$HOME/.zshrc"
    fi
    
    if [[ -n "$SHELL_RC" ]]; then
        # Check if PATH already contains commandbrain_env
        if ! grep -q "commandbrain_env" "$SHELL_RC"; then
            echo ""
            echo "Adding CommandBrain to your PATH..."
            echo "" >> "$SHELL_RC"
            echo "# CommandBrain - added by installer" >> "$SHELL_RC"
            echo "export PATH=\"$VENV_PATH/bin:\$PATH\"" >> "$SHELL_RC"
            echo "✓ PATH updated in $SHELL_RC"
            echo ""
            echo "⚠️  IMPORTANT: Run this command now to activate:"
            echo "   source $SHELL_RC"
            echo ""
            echo "Or close and reopen your terminal."
        fi
    fi
fi

echo "========================================"
echo "Installation Complete!"
echo "========================================"
echo ""
echo "✅ CommandBrain is installed at ~/.commandbrain_env"
echo ""
echo "⚠️  IMPORTANT - One More Step Required:"
echo ""
echo "The 'cb' command is ready, but you need to reload your shell."
echo ""
echo "Choose ONE option:"
echo ""
echo "1. Reload your current shell (recommended):"
if [[ -f "$HOME/.bashrc" ]]; then
    echo "   source ~/.bashrc"
elif [[ -f "$HOME/.zshrc" ]]; then
    echo "   source ~/.zshrc"
fi
echo ""
echo "2. Or close and reopen your terminal"
echo ""
echo "========================================"
echo "After reloading, try these commands:"
echo "========================================"
echo ""
echo "  cb ssh                    # Search for ssh"
echo "  cb network monitoring     # Multi-word search"
echo "  cb -e grep                # Examples only (quick!)"
echo "  cb -d ssh                 # Detailed view"
echo "  cb --list                 # List categories"
echo ""
echo "✨ NEW: Fuzzy search! Typos are OK:"
echo "  cb graep  → Suggests 'grep'"
echo "  cb pign   → Suggests 'ping'"
echo ""

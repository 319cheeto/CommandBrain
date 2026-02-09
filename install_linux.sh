#!/bin/bash
# CommandBrain Easy Installer for Linux/Mac/WSL
# This script sets up CommandBrain automatically

set -e  # Exit on error

# Color codes for better visibility
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

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
    echo "  sudo apt install python3 python3-pip python3-venv"
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

echo "[1/7] Python found!"
python3 --version
echo ""

# Check if we're in a virtual environment already
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "[2/7] Setting up virtual environment..."
    echo "   (Modern Linux requires this for pip packages)"
    
    # Create venv in ~/.commandbrain_env if it doesn't exist
    VENV_PATH="$HOME/.commandbrain_env"
    
    # Clean up any broken venv first
    if [ -d "$VENV_PATH" ] && [ ! -f "$VENV_PATH/bin/activate" ]; then
        echo "   ⚠️  Removing broken virtual environment..."
        rm -rf "$VENV_PATH"
    fi
    
    if [ ! -d "$VENV_PATH" ]; then
        # Try to create venv, catch error if python3-venv is missing
        echo "   Creating virtual environment..."
        if ! python3 -m venv "$VENV_PATH" 2>/dev/null; then
            echo ""
            echo -e "${RED}⚠️  python3-venv is not installed!${NC}"
            echo "   Installing it now..."
            echo ""
            if command -v apt &> /dev/null; then
                sudo apt update
                sudo apt install -y python3-venv python3-pip
            elif command -v yum &> /dev/null; then
                sudo yum install -y python3-venv
            else
                echo ""
                echo "================================================================"
                echo "  MANUAL INSTALLATION REQUIRED"
                echo "================================================================"
                echo ""
                echo "Please install python3-venv manually:"
                echo "  Debian/Ubuntu/Kali: sudo apt install python3-venv"
                echo "  Red Hat/CentOS:     sudo yum install python3-venv"
                echo ""
                echo "After installing, run this installer again."
                echo "================================================================"
                exit 1
            fi
            # Try again after installation
            python3 -m venv "$VENV_PATH"
        fi
        echo -e "   ${GREEN}✓ Virtual environment created at $VENV_PATH${NC}"
    else
        echo "   ✓ Using existing virtual environment"
    fi
    
    # Activate the virtual environment
    source "$VENV_PATH/bin/activate"
    echo -e "   ${GREEN}✓ Virtual environment activated${NC}"
    echo ""
else
    echo "[2/7] Virtual environment detected!"
    echo "   Using: $VIRTUAL_ENV"
    echo ""
fi

echo "[3/7] Installing CommandBrain..."
# Upgrade pip first to avoid warnings
pip3 install --upgrade pip 2>&1 | grep -v "WARNING: Running pip as the 'root' user" || true
# Install in editable mode
pip3 install -e . 2>&1 | grep -v "WARNING: Running pip as the 'root' user" || true
echo -e "${GREEN}✓ CommandBrain installed${NC}"
echo ""

echo "[4/7] Setting up database..."
if ! commandbrain-setup; then
    echo -e "${RED}ERROR: Database setup failed${NC}"
    echo "Try running manually: commandbrain-setup"
    exit 1
fi
echo -e "${GREEN}✓ Database created with ~30 essential Linux commands!${NC}"
echo ""

echo "[5/7] Enabling purpose-based search..."
echo ""
echo "Adding student-friendly slang terms (brute force, network scan, etc.)"
if python3 enhance_slang_tags.py > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Students can now search by purpose/task!${NC}"
else
    echo -e "${YELLOW}⚠️  Slang tags enhancement skipped (not critical)${NC}"
fi
echo ""

echo "[6/7] OPTIONAL: Add Kali Security Tools?"
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
    if commandbrain-kali; then
        echo -e "${GREEN}Kali tools added!${NC}"
    else
        echo -e "${YELLOW}⚠️  Kali tools installation had issues (check above)${NC}"
    fi
else
    echo ""
    echo "Skipping Kali tools. You can add them later with: commandbrain-kali"
fi
echo ""

echo "[7/7] Configuring shell PATH..."
if [[ -n "$VENV_PATH" ]]; then
    SHELL_RC=""
    # Check multiple possible shell configs
    if [[ -f "$HOME/.bashrc" ]]; then
        SHELL_RC="$HOME/.bashrc"
    elif [[ -f "$HOME/.bash_profile" ]]; then
        SHELL_RC="$HOME/.bash_profile"
    elif [[ -f "$HOME/.zshrc" ]]; then
        SHELL_RC="$HOME/.zshrc"
    elif [[ -f "$HOME/.profile" ]]; then
        SHELL_RC="$HOME/.profile"
    fi
    
    if [[ -n "$SHELL_RC" ]]; then
        # Check if PATH already contains commandbrain_env
        if ! grep -q "commandbrain_env" "$SHELL_RC"; then
            echo ""
            echo "Adding CommandBrain to your PATH..."
            echo "" >> "$SHELL_RC"
            echo "# CommandBrain - added by installer $(date +%Y-%m-%d)" >> "$SHELL_RC"
            echo "export PATH=\"$VENV_PATH/bin:\$PATH\"" >> "$SHELL_RC"
            echo -e "${GREEN}✓ PATH updated in $(basename $SHELL_RC)${NC}"
        else
            echo -e "${GREEN}✓ PATH already configured in $(basename $SHELL_RC)${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  No shell config found. Creating .bashrc...${NC}"
        echo "# CommandBrain - added by installer $(date +%Y-%m-%d)" > "$HOME/.bashrc"
        echo "export PATH=\"$VENV_PATH/bin:\$PATH\"" >> "$HOME/.bashrc"
        SHELL_RC="$HOME/.bashrc"
    fi
    
    # Verify installation
    echo ""
    echo "========================================"
    echo "Verifying Installation"
    echo "========================================"
    
    verification_failed=false
    
    echo -n "  Database: "
    if [ -f "$HOME/.commandbrain.db" ]; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${RED}✗ Missing${NC}"
        verification_failed=true
    fi
    
    echo -n "  Virtual Env: "
    if [ -d "$VENV_PATH" ]; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${RED}✗ Missing${NC}"
        verification_failed=true
    fi
    
    echo -n "  Commands: "
    if command -v cb &> /dev/null; then
        echo -e "${GREEN}✓ cb found${NC}"
    else
        echo -e "${YELLOW}⚠️  cb not in PATH yet${NC}"
    fi
    
    echo ""
    
    if $verification_failed; then
        echo -e "${RED}========================================${NC}"
        echo -e "${RED}INSTALLATION INCOMPLETE${NC}"
        echo -e "${RED}========================================${NC}"
        echo ""
        echo "Some components failed to install. Please:"
        echo "  1. Check error messages above"
        echo "  2. Try running: ./uninstall_linux.sh"
        echo "  3. Then run: ./install_linux.sh again"
        echo ""
        exit 1
    fi
fi

echo ""
echo "========================================"
echo "Installation Complete!"
echo "========================================"
echo ""
echo -e "${GREEN}✓ CommandBrain is installed successfully!${NC}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  IMPORTANT: Activate the changes!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Run this command now:"
echo ""
echo -e "  ${YELLOW}source $SHELL_RC${NC}"
echo ""
echo "Or simply close and reopen your terminal."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Then try it out:"
echo "  cb ssh"
echo "  cb find files"
echo "  commandbrain --help"
echo ""

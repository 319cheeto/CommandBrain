#!/bin/bash
# CommandBrain Updater for Linux/Mac/WSL

echo "========================================"
echo "CommandBrain Updater"
echo "========================================"
echo ""

# Check if installed
VENV_PATH="$HOME/.commandbrain_env"
if [ ! -d "$VENV_PATH" ]; then
    echo "❌ CommandBrain is not installed!"
    echo ""
    echo "Install it first with: ./install_linux.sh"
    echo ""
    exit 1
fi

echo "[1/3] Checking for updates..."

# Check if we're in a git repository
if [ -d ".git" ]; then
    echo "   Git repository detected"
    
    # Fetch latest changes
    git fetch origin 2>/dev/null
    
    # Check if we're behind
    LOCAL=$(git rev-parse @)
    REMOTE=$(git rev-parse @{u} 2>/dev/null)
    
    if [ "$LOCAL" = "$REMOTE" ]; then
        echo "   ✓ Already up to date!"
        echo ""
        read -p "Do you want to reinstall anyway? (y/n): " REINSTALL
        if [[ "$REINSTALL" != "y" ]] && [[ "$REINSTALL" != "Y" ]]; then
            echo "   Cancelled."
            exit 0
        fi
    else
        echo "   📥 Updates available!"
        echo ""
        echo "   Pulling latest changes..."
        git pull origin main || git pull origin master
        echo "   ✓ Code updated"
    fi
else
    echo "   Not a git repository - skipping code update"
    echo "   (Proceeding with package reinstall)"
fi

echo ""
echo "[2/3] Updating CommandBrain package..."

# Activate virtual environment
source "$VENV_PATH/bin/activate"

# Upgrade the package
pip install --upgrade -e .

echo "   ✓ Package updated"
echo ""

echo "[3/3] Database is preserved (your commands are safe!)"
echo ""

# Count commands in database
DB_PATH="$HOME/.commandbrain.db"
if [ -f "$DB_PATH" ]; then
    COMMANDS=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM commands;" 2>/dev/null || echo "?")
    echo "   Your database has $COMMANDS commands"
fi

echo ""
echo "========================================"
echo "Update Complete!"
echo "========================================"
echo ""
echo "CommandBrain has been updated to the latest version."
echo ""
echo "Try it: cb ssh"
echo ""

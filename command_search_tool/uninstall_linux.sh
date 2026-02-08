#!/bin/bash
# CommandBrain Uninstaller for Linux/Mac/WSL

echo "========================================"
echo "CommandBrain Uninstaller"
echo "========================================"
echo ""
echo "This will remove:"
echo "  - CommandBrain virtual environment (~/.commandbrain_env)"
echo "  - Database file (~/.commandbrain.db)"
echo "  - PATH entry from shell config"
echo ""
read -p "Are you sure you want to uninstall? (y/n): " CONFIRM

if [[ "$CONFIRM" != "y" ]] && [[ "$CONFIRM" != "Y" ]]; then
    echo ""
    echo "Uninstallation cancelled."
    exit 0
fi

echo ""
echo "Uninstalling CommandBrain..."
echo ""

# Remove virtual environment
VENV_PATH="$HOME/.commandbrain_env"
if [ -d "$VENV_PATH" ]; then
    rm -rf "$VENV_PATH"
    echo "✓ Removed virtual environment"
else
    echo "- Virtual environment not found (already removed?)"
fi

# Remove database
DB_PATH="$HOME/.commandbrain.db"
if [ -f "$DB_PATH" ]; then
    rm "$DB_PATH"
    echo "✓ Removed database"
else
    echo "- Database not found (already removed?)"
fi

# Remove PATH entry from shell configs
for SHELL_RC in "$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.profile"; do
    if [ -f "$SHELL_RC" ]; then
        # Check if the file has CommandBrain entries
        if grep -q "commandbrain" "$SHELL_RC"; then
            # Create backup
            cp "$SHELL_RC" "${SHELL_RC}.backup"
            # Remove CommandBrain lines
            sed -i '/# CommandBrain/d' "$SHELL_RC"
            sed -i '/commandbrain_env/d' "$SHELL_RC"
            echo "✓ Removed PATH entry from $(basename $SHELL_RC)"
        fi
    fi
done

echo ""
echo "========================================"
echo "Uninstallation Complete!"
echo "========================================"
echo ""
echo "CommandBrain has been removed from your system."
echo ""
echo "Note: You may need to restart your terminal or run:"
echo "  source ~/.bashrc  # or ~/.zshrc"
echo ""
echo "To reinstall later, just run: ./install_linux.sh"
echo ""

#!/bin/bash
# CommandBrain Quick Diagnostic Script

echo "========================================"
echo "CommandBrain Installation Diagnostic"
echo "========================================"
echo ""

echo "[1] Checking if virtual environment exists..."
VENV_PATH="$HOME/.commandbrain_env"
if [ -d "$VENV_PATH" ]; then
    echo "   ✓ Virtual environment found at $VENV_PATH"
else
    echo "   ✗ Virtual environment NOT found"
    echo "   Run: ./install_linux.sh"
    exit 1
fi
echo ""

echo "[2] Checking if cb command exists in venv..."
if [ -f "$VENV_PATH/bin/cb" ]; then
    echo "   ✓ cb command exists at $VENV_PATH/bin/cb"
else
    echo "   ✗ cb command NOT found in venv"
    echo "   Try reinstalling: ./install_linux.sh"
    exit 1
fi
echo ""

echo "[3] Checking if commandbrain is executable..."
if [ -x "$VENV_PATH/bin/cb" ]; then
    echo "   ✓ cb is executable"
else
    echo "   ✗ cb is NOT executable"
    chmod +x "$VENV_PATH/bin/cb"
    echo "   ✓ Fixed permissions"
fi
echo ""

echo "[4] Checking current PATH..."
if echo "$PATH" | grep -q "commandbrain_env"; then
    echo "   ✓ commandbrain_env is in PATH"
else
    echo "   ✗ commandbrain_env is NOT in PATH (This is your issue!)"
fi
echo ""

echo "[5] Checking shell config files..."
for RC in "$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.bash_profile"; do
    if [ -f "$RC" ]; then
        if grep -q "commandbrain_env" "$RC"; then
            echo "   ✓ Found PATH entry in $(basename $RC)"
        else
            echo "   - No PATH entry in $(basename $RC)"
        fi
    fi
done
echo ""

echo "[6] Testing direct execution..."
if "$VENV_PATH/bin/cb" --stats &>/dev/null; then
    echo "   ✓ Direct execution works!"
else
    echo "   ✗ Direct execution failed (database issue?)"
fi
echo ""

echo "========================================"
echo "SOLUTION:"
echo "========================================"
echo ""
echo "The cb command exists but isn't in your PATH yet."
echo ""
echo "Choose ONE of these options:"
echo ""
echo "Option A - Reload your shell (RECOMMENDED):"
if [ -f "$HOME/.bashrc" ]; then
    echo "   source ~/.bashrc"
elif [ -f "$HOME/.zshrc" ]; then
    echo "   source ~/.zshrc"
fi
echo ""
echo "Option B - Close and reopen your terminal"
echo ""
echo "Option C - Use full path for now:"
echo "   $VENV_PATH/bin/cb ssh"
echo ""
echo "Option D - Add to PATH manually:"
echo "   echo 'export PATH=\"\$HOME/.commandbrain_env/bin:\$PATH\"' >> ~/.bashrc"
echo "   source ~/.bashrc"
echo ""
echo "After fixing PATH, test with: cb --stats"
echo ""

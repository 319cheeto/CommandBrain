#!/bin/bash
# Quick test to verify CommandBrain installation
# Run this after installing to make sure everything works

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================"
echo "Testing CommandBrain Installation"
echo "========================================"
echo ""

failed=false

# Test 1: Check if cb command exists
echo "[Test 1/3] Checking if 'cb' command exists..."
if command -v cb &> /dev/null; then
    echo -e "  ${GREEN}✓ PASSED${NC} - 'cb' command found"
else
    echo -e "  ${RED}✗ FAILED${NC} - 'cb' command not found"
    echo ""
    echo "  This means either:"
    echo "  1. You haven't run the installer yet: ./install_linux.sh"
    echo "  2. You haven't reloaded your shell: source ~/.bashrc"
    echo ""
    failed=true
fi
echo ""

# Test 2: Check if database exists
echo "[Test 2/3] Checking if database exists..."
if [ -f "$HOME/.commandbrain.db" ]; then
    echo -e "  ${GREEN}✓ PASSED${NC} - Database found"
else
    echo -e "  ${RED}✗ FAILED${NC} - Database not found at: $HOME/.commandbrain.db"
    echo ""
    echo "  Run: commandbrain-setup"
    echo "  Or: ./install_linux.sh"
    echo ""
    failed=true
fi
echo ""

# Test 3: Try searching for a command
echo "[Test 3/3] Testing actual search..."
if cb ssh &> /dev/null; then
    echo -e "  ${GREEN}✓ PASSED${NC} - Search works!"
else
    echo -e "  ${RED}✗ FAILED${NC} - Search command failed"
    echo ""
    failed=true
fi
echo ""

if [ "$failed" = true ]; then
    echo "========================================"
    echo -e "${RED}❌ SOME TESTS FAILED${NC}"
    echo "========================================"
    echo ""
    echo "Common fixes:"
    echo "  1. Reload your shell: source ~/.bashrc"
    echo "  2. Run installer again: ./install_linux.sh"
    echo "  3. Check: TROUBLESHOOTING.md"
    echo ""
    exit 1
else
    echo "========================================"
    echo -e "${GREEN}✅ ALL TESTS PASSED!${NC}"
    echo "========================================"
    echo ""
    echo "CommandBrain is working correctly!"
    echo ""
    echo "Try these commands:"
    echo "  cb ssh"
    echo "  cb find files"
    echo "  cb network scan"
    echo "  cb --help"
    echo ""
fi

#!/bin/bash
# CommandBrain Installation Test & Diagnostic Script
# This script tests the installation multiple times and reports issues

set +e  # Don't exit on error - we want to see all issues

LOGFILE="install_test_$(date +%Y%m%d_%H%M%S).log"

echo "========================================"
echo "CommandBrain Installation Tester"
echo "========================================"
echo ""
echo "This will:"
echo "  1. Uninstall CommandBrain completely"
echo "  2. Reinstall it fresh"
echo "  3. Test all commands work"
echo "  4. Repeat 3 times to catch intermittent issues"
echo ""
echo "Log file: $LOGFILE"
echo ""
read -p "Continue? (y/n): " CONFIRM

if [[ "$CONFIRM" != "y" ]] && [[ "$CONFIRM" != "Y" ]]; then
    echo "Test cancelled."
    exit 0
fi

exec > >(tee -a "$LOGFILE") 2>&1

echo ""
echo "========================================" 
echo "SYSTEM INFORMATION"
echo "========================================"
echo "Date: $(date)"
echo "OS: $(uname -a)"
echo "Python: $(python3 --version 2>&1)"
echo "Shell: $SHELL"
echo "User: $USER"
echo "Home: $HOME"
echo ""

# Function to test if commands work
test_commands() {
    local test_num=$1
    echo ""
    echo "========================================" 
    echo "TEST $test_num: Verifying Commands"
    echo "========================================"
    
    local all_passed=true
    
    # Test 1: Can we find cb in PATH?
    echo -n "  [1] cb in PATH: "
    if command -v cb &> /dev/null; then
        echo "✓ PASS"
    else
        echo "✗ FAIL"
        all_passed=false
        echo "      Location: $(which cb 2>&1)"
    fi
    
    # Test 2: Can we find commandbrain in PATH?
    echo -n "  [2] commandbrain in PATH: "
    if command -v commandbrain &> /dev/null; then
        echo "✓ PASS"
    else
        echo "✗ FAIL"
        all_passed=false
    fi
    
    # Test 3: Can we run cb?
    echo -n "  [3] cb executes: "
    if cb --help &> /dev/null; then
        echo "✓ PASS"
    else
        echo "✗ FAIL"
        all_passed=false
    fi
    
    # Test 4: Database exists?
    echo -n "  [4] Database exists: "
    if [ -f "$HOME/.commandbrain.db" ]; then
        echo "✓ PASS"
        db_size=$(du -h "$HOME/.commandbrain.db" | cut -f1)
        echo "      Size: $db_size"
    else
        echo "✗ FAIL"
        all_passed=false
    fi
    
    # Test 5: Virtual environment exists?
    echo -n "  [5] Virtual environment: "
    if [ -d "$HOME/.commandbrain_env" ]; then
        echo "✓ PASS"
    else
        echo "✗ FAIL"
        all_passed=false
    fi
    
    # Test 6: Can we search for a command?
    echo -n "  [6] Search works: "
    if cb ssh 2>&1 | grep -q "ssh"; then
        echo "✓ PASS"
    else
        echo "✗ FAIL"
        all_passed=false
        echo "      Output: $(cb ssh 2>&1 | head -3)"
    fi
    
    # Test 7: PATH contains venv?
    echo -n "  [7] PATH configured: "
    if echo "$PATH" | grep -q "commandbrain_env"; then
        echo "✓ PASS"
    else
        echo "✗ FAIL - PATH may not persist after terminal restart"
        all_passed=false
    fi
    
    # Test 8: Shell config has PATH?
    echo -n "  [8] Shell config updated: "
    found_in_rc=false
    for rc in "$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.profile" "$HOME/.bash_profile"; do
        if [ -f "$rc" ] && grep -q "commandbrain_env" "$rc"; then
            echo "✓ PASS ($rc)"
            found_in_rc=true
            break
        fi
    done
    if ! $found_in_rc; then
        echo "✗ FAIL - No shell config contains commandbrain_env"
        all_passed=false
    fi
    
    if $all_passed; then
        echo ""
        echo "  ✓✓✓ ALL TESTS PASSED ✓✓✓"
        return 0
    else
        echo ""
        echo "  ✗✗✗ SOME TESTS FAILED ✗✗✗"
        return 1
    fi
}

# Function to do complete uninstall
complete_uninstall() {
    echo ""
    echo "========================================" 
    echo "COMPLETE UNINSTALL"
    echo "========================================"
    
    # Run the official uninstaller non-interactively
    echo "y" | ./uninstall_linux.sh 2>&1 || true
    
    # Extra cleanup - remove anything that might be left
    echo ""
    echo "Extra cleanup steps:"
    
    # Remove venv
    if [ -d "$HOME/.commandbrain_env" ]; then
        rm -rf "$HOME/.commandbrain_env"
        echo "  ✓ Removed venv"
    fi
    
    # Remove database
    if [ -f "$HOME/.commandbrain.db" ]; then
        rm "$HOME/.commandbrain.db"
        echo "  ✓ Removed database"
    fi
    
    # Uninstall via pip (in case it was installed system-wide)
    pip3 uninstall -y commandbrain 2>&1 | grep -v "WARNING: Skipping" || true
    
    # Remove from shell configs more aggressively
    for rc in "$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.profile" "$HOME/.bash_profile"; do
        if [ -f "$rc" ]; then
            # Create backup
            cp "$rc" "${rc}.backup_test" 2>/dev/null || true
            # Remove commandbrain lines
            grep -v "commandbrain" "$rc" > "${rc}.tmp" 2>/dev/null && mv "${rc}.tmp" "$rc" || true
        fi
    done
    
    # Remove egg-info if exists
    if [ -d "commandbrain.egg-info" ]; then
        rm -rf commandbrain.egg-info
        echo "  ✓ Removed egg-info"
    fi
    
    echo ""
    echo "Uninstall complete. Waiting 2 seconds..."
    sleep 2
}

# Main test loop
for test_num in 1 2 3; do
    echo ""
    echo "========================================"
    echo "ITERATION $test_num OF 3"
    echo "========================================"
    
    # Uninstall
    complete_uninstall
    
    # Fresh install
    echo ""
    echo "========================================" 
    echo "FRESH INSTALL"
    echo "========================================"
    echo "n" | ./install_linux.sh 2>&1  # Answer 'n' to Kali tools
    
    # Source shell config to get PATH updates
    if [ -f "$HOME/.bashrc" ]; then
        source "$HOME/.bashrc"
    elif [ -f "$HOME/.zshrc" ]; then
        source "$HOME/.zshrc"
    fi
    
    # Test it
    if ! test_commands "$test_num"; then
        echo ""
        echo "========================================" 
        echo "TEST $test_num FAILED - DIAGNOSTICS"
        echo "========================================"
        echo ""
        echo "Current PATH:"
        echo "$PATH"
        echo ""
        echo "Files in ~/.commandbrain_env/bin:"
        ls -la "$HOME/.commandbrain_env/bin/" 2>&1 || echo "  Directory not found!"
        echo ""
        echo "Shell configs:"
        for rc in "$HOME/.bashrc" "$HOME/.zshrc"; do
            if [ -f "$rc" ]; then
                echo "  --- $rc (last 10 lines) ---"
                tail -10 "$rc"
            fi
        done
    fi
    
    echo ""
    echo "Waiting 3 seconds before next iteration..."
    sleep 3
done

echo ""
echo "========================================"
echo "TEST SUMMARY"
echo "========================================"
echo ""
echo "Full log saved to: $LOGFILE"
echo ""
echo "Review the log to find patterns in failures."
echo "Common issues:"
echo "  - PATH not updating (need to source shell config)"
echo "  - Database not created (permissions issue)"
echo "  - Virtual env not activated (python3-venv missing)"
echo ""

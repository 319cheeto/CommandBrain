# Test Installation Script

## What Does This Do?

`test_install.sh` is a diagnostic script that helps identify installation problems by:

1. **Completely uninstalling** CommandBrain
2. **Reinstalling** it fresh
3. **Testing** 8 critical components
4. **Repeating** the process 3 times
5. **Generating** a detailed log file

## When to Use This

Use this script if:
- Installation completed but `cb` command doesn't work
- You're getting "command not found" errors
- You want to verify a clean installation
- A student reports installation issues
- You're debugging installation problems

## How to Run

```bash
cd command_search_tool
chmod +x test_install.sh
./test_install.sh
```

The script will ask for confirmation before starting.

## What It Tests

Each iteration tests 8 components:

### 1. ✓ cb in PATH
Checks if the `cb` command is available in your PATH.

### 2. ✓ commandbrain in PATH  
Checks if the `commandbrain` command is available.

### 3. ✓ cb executes
Tries to run `cb --help` to verify it executes.

### 4. ✓ Database exists
Checks if `~/.commandbrain.db` was created and shows its size.

### 5. ✓ Virtual environment
Verifies `~/.commandbrain_env` directory exists.

### 6. ✓ Search works
Actually searches for "ssh" to test the database is populated.

### 7. ✓ PATH configured
Checks if current PATH contains the virtual environment.

### 8. ✓ Shell config updated  
Verifies shell config files (.bashrc, .zshrc, etc.) contain CommandBrain.

## Output

The script produces:

### Console Output
Real-time display of test results with:
- ✓ Green checkmarks for passing tests
- ✗ Red X for failing tests  
- Diagnostic info for failures

### Log File
A detailed log saved as: `install_test_YYYYMMDD_HHMMSS.log`

Example:
```
install_test_20240208_143022.log
```

The log contains:
- System information (OS, Python version, shell, etc.)
- Full output from each installation
- Test results from all 3 iterations
- Diagnostic information for any failures
- Current PATH and directory listings

## Interpreting Results

### All Tests Pass ✓✓✓
```
  ✓✓✓ ALL TESTS PASSED ✓✓✓
```
Installation is working correctly!

### Some Tests Fail ✗✗✗
```
  ✗✗✗ SOME TESTS FAILED ✗✗✗
```

The script will show diagnostics including:
- Current PATH
- Contents of virtual environment directory
- Last 10 lines of shell config files

### Common Failure Patterns

**PATH not configured:**
```
[7] PATH configured: ✗ FAIL
```
**Solution:** Shell config wasn't updated. Check .bashrc or .zshrc.

**Database missing:**
```
[4] Database exists: ✗ FAIL
```
**Solution:** `commandbrain-setup` failed. Check permissions.

**Virtual environment missing:**
```
[5] Virtual environment: ✗ FAIL
```
**Solution:** `python3-venv` package missing. Install it:
```bash
sudo apt install python3-venv
```

**Commands not in PATH:**
```
[1] cb in PATH: ✗ FAIL
[2] commandbrain in PATH: ✗ FAIL
```
**Solution:** Need to source shell config:
```bash
source ~/.bashrc
```

## What Gets Cleaned Up

During each uninstall, the script removes:
- Virtual environment (`~/.commandbrain_env`)
- Database (`~/.commandbrain.db`)
- Shell config entries (from .bashrc, .zshrc, etc.)
- Pip package metadata
- Egg-info directories

It creates backups with timestamps: `.bashrc.backup_test`

## Troubleshooting the Test Script

### Permission Denied
```bash
chmod +x test_install.sh
```

### Script Hangs
Press Ctrl+C to cancel. Check if:
- Installation is waiting for user input
- System is low on resources
- Network is slow (shouldn't need network, but check)

### Script Fails Immediately
Check prerequisites:
```bash
python3 --version  # Should be 3.6+
bash --version     # Should be 4.0+
```

## For Instructors

When a student reports installation problems:

1. **Ask them to run this script:**
   ```bash
   ./test_install.sh
   ```

2. **Request the log file:**  
   Ask them to send you `install_test_*.log`

3. **Look for patterns:**
   - If test 7 fails: PATH not persisting → Shell config issue
   - If test 4 fails: Database creation problem → Permissions issue  
   - If test 1-2 fail: Commands not found → Need to reload shell

4. **Common fixes to suggest:**
   ```bash
   # Fix 1: Reload shell
   source ~/.bashrc
   
   # Fix 2: Install Python venv
   sudo apt install python3-venv
   
   # Fix 3: Manual database setup
   ~/.commandbrain_env/bin/commandbrain-setup
   ```

## Advanced: Customizing the Test

You can modify `test_install.sh` to:

- Change the number of iterations (default: 3)
- Add more tests
- Skip Kali tools installation  
- Test additional components

Look for these sections in the script:
```bash
for test_num in 1 2 3; do    # Change iterations here
    ...
done
```

## See Also

- [KALI_INSTALL_FIX.md](KALI_INSTALL_FIX.md) - Kali-specific troubleshooting
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - General troubleshooting guide
- [INSTALL.md](INSTALL.md) - Installation documentation

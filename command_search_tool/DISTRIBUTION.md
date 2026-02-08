# CommandBrain Distribution Guide

## Overview
CommandBrain is distributed as a complete package containing all Python modules, setup scripts, and installers. This guide outlines the recommended distribution methods for educational environments.

---

## Option 1: GitHub Repository (RECOMMENDED)
**Best for:** Most classrooms, easy updates, professional workflow

### Setup:
1. Create a GitHub repository
2. Push the CommandBrain codebase to the repository
3. Share the clone URL with students

### Installation Instructions:
```bash
# For Windows (Command Prompt or PowerShell):
git clone https://github.com/YOUR_USERNAME/commandbrain.git
cd commandbrain
install_windows.bat

# For Linux/Mac/WSL:
git clone https://github.com/YOUR_USERNAME/commandbrain.git
cd commandbrain
chmod +x install_linux.sh
./install_linux.sh
```

**Advantages:**
- Easy to push updates (students just run `git pull`)
- Professional development workflow
- Free hosting
- Version control

---

## Option 2: Zip File Download
**Best for:** Students without git, simple one-time distribution

### Setup:
1. Create a zip archive of the complete CommandBrain directory
2. Upload to course management system (Canvas, Blackboard, etc.) or cloud storage
3. Distribute download link to students

### Installation Instructions:
**Windows:**
1. Download `commandbrain.zip`
2. Right-click → Extract All
3. Open Command Prompt in extracted folder
4. Run: `install_windows.bat`

**Linux/Mac:**
```bash
unzip commandbrain.zip
cd commandbrain
chmod +x install_linux.sh
./install_linux.sh
```

**Advantages:**
- No git required
- Works with existing course systems
- Simple for non-technical students

---

## Option 3: PyPI (Python Package Index)
**Best for:** Maximum simplicity, professional distribution

### Setup:
1. Register for a PyPI account at https://pypi.org
2. Install build tools: `pip install twine build`
3. Build the package:
   ```bash
   python -m build
   ```
4. Publish to PyPI:
   ```bash
   python -m twine upload dist/*
   ```

### Installation Instructions (SIMPLE):
```bash
# That's it - one command!
pip install commandbrain

# Then setup:
commandbrain-setup
```

**Advantages:**
- **Simplest installation** (one command)
- Automatic updates available
- Most professional

**Disadvantages:**
- Requires PyPI account setup
- Package name must be unique globally

---

## Option 4: Standalone Executable (Windows Only)
**Best for:** Windows environments without Python installation

### Setup:
1. Install PyInstaller: `pip install pyinstaller`
2. Build standalone executable:
   ```bash
   pyinstaller --onefile --name cb commandbrain.py
   ```
3. Distribute the generated `dist/cb.exe` file

### Installation Instructions:
1. Download `cb.exe`
2. Move to a permanent location (e.g., `C:\Tools\`)
3. Add to PATH or use full path

**Advantages:**
- No Python installation required
- Single file

**Disadvantages:**
- Windows only
- No easy updates
- Larger file size (~10-20 MB)

---

## Required Files for Distribution

### Core Files (MUST include):
```
command_search_tool/
├── commandbrain.py          # Main program
├── setup_commandbrain.py    # Database setup
├── add_kali_tools.py        # Optional Kali tools
├── import_commands.py       # Bulk import utility
├── setup.py                 # Installation configuration
├── requirements.txt         # Dependencies
├── install_windows.bat      # Windows one-click installer
└── install_linux.sh         # Linux/Mac one-click installer
```

### Optional Files (Nice to include):
```
├── README.md                # Overview
├── STUDENT_GUIDE.md         # Student documentation
├── QUICKSTART.md            # Quick start guide
├── INSTALL.md               # Detailed installation
└── WHATS_INCLUDED.md        # Command list
```

**Note:** All Python modules and setup.py are required for proper functionality.

---

## Sample Classroom Documentation

### Syllabus/Course Page Template:

```
INSTALLING COMMANDBRAIN

Prerequisites:
- Python 3.6 or higher (check: python --version)

Installation:
1. Download CommandBrain from [LINK]
2. Extract the zip file
3. Run the installer:
   - Windows: Double-click install_windows.bat
   - Linux/Mac: Open terminal, run ./install_linux.sh

That's it! Now you can search commands with:
   cb ssh
   cb find files
   cb grep

Need help? See STUDENT_GUIDE.md
```

---

## Pre-Distribution Checklist

Recommended verification steps:

- [ ] Select distribution method (GitHub recommended)
- [ ] Verify installation on Windows environment
- [ ] Verify installation on Linux/Mac environment
- [ ] Prepare installation demonstration (optional)
- [ ] Include installation instructions in course materials
- [ ] Prepare alternative distribution method as backup

---

## Troubleshooting Common Installation Issues

### "Python is not recognized"
**Cause:** Python not installed or not in system PATH  
**Resolution:** Install Python from https://www.python.org/downloads/  
- Windows users: Ensure "Add Python to PATH" checkbox is selected during installation

### "Permission denied" (Linux/Mac)
**Cause:** Installer script lacks execute permissions  
**Resolution:**
```bash
chmod +x install_linux.sh
```

### "pip is not recognized"
**Cause:** pip executable not in system PATH  
**Resolution:**
```bash
python -m pip install -e .
```

### Database initialization errors
**Resolution:** Re-run database setup
```bash
commandbrain-setup
```

---

## Update Procedures

### GitHub distribution:
```bash
git pull
```

### Zip file distribution:
Redistribute updated zip archive

### PyPI distribution:
```bash
pip install --upgrade commandbrain
```

---

## Quick Comparison

| Method | Complexity | Install Command | Updates | Best For |
|--------|-----------|----------------|---------|----------|
| **GitHub** | Low | `git clone` + installer | Easy (`git pull`) | Most classes |
| **Zip File** | Lowest | Download + installer | Re-download | Non-technical |
| **PyPI** | Lowest | `pip install` | `pip install -U` | Professional |
| **EXE** | Medium | Download only | Re-download | Windows-only |

**Recommendation for intro cybersecurity courses:** **GitHub** (teaches version control) or **Zip file** (lowest barrier to entry). **PyPI** distribution can be added later for professional polish.

---

## Sample Student Communication

```
Subject: Installing CommandBrain - Your Offline Command Reference

Hi everyone,

This semester we'll be using CommandBrain, an offline tool for quickly
referencing Linux commands without leaving your terminal.

Installation (5 minutes):
1. Download from: [LINK]
2. Extract the zip file
3. Open terminal in that folder
4. Run the installer:
   - Windows: install_windows.bat
   - Linux: ./install_linux.sh

Usage:
   cb ssh          # Search for SSH
   cb find files   # Search for finding files

This provides instant access to command references without internet connectivity.
See STUDENT_GUIDE.md for detailed examples.

Questions? Post in the course discussion board.
```

---

## Summary

**Distribution Requirements:** The complete CommandBrain directory must be distributed, as all Python modules are interdependent.

**Recommended Approach for Most Classrooms:**
1. Create zip archive of complete CommandBrain directory
2. Upload to course management system
3. Provide installation instructions: "Download, extract, run installer"

**Professional Approach (Recommended):**
Host on GitHub - enables easy updates and introduces students to version control

**Advanced Distribution:**
Publish to PyPI for single-command installation: `pip install commandbrain`

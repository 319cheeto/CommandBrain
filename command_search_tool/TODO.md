# CommandBrain TODO & Enhancement List

## 🎯 PRIMARY GOAL (CRITICAL!)
**Students must be able to search by PURPOSE/TASK, not just command names**

### Current Status: ✅ PARTIALLY WORKING
- ✅ Searches descriptions, tags, related commands, categories
- ✅ Multi-word search ("password cracking")
- ✅ Fuzzy search for typo correction
- ⚠️ **NEEDS ENHANCEMENT:** Add more slang terms and purpose-based tags to database

---

## 🔴 HIGH PRIORITY - Core Functionality

### 1. Enhance Slang/Purpose Search
**Goal:** Students type what they're trying to DO, not technical names

**Examples that MUST work:**
- "password cracking" → hydra, john, hashcat
- "brute force" / "brute forcing" → hydra, medusa
- "sniffing" / "packet capture" → tcpdump, wireshark
- "web hacking" → burpsuite, sqlmap, nikto
- "scanning" / "port scan" → nmap, masscan
- "enumeration" → nmap, enum4linux, dirb, gobuster
- "exploit" / "exploiting" → metasploit, searchsploit
- "reverse shell" → netcat, msfvenom  
- "privilege escalation" / "priv esc" → sudo, find
- "hash cracking" → john, hashcat
- "wifi hacking" / "wireless" → aircrack-ng, wifite
- "man in the middle" / "mitm" → ettercap, bettercap

**Implementation:**
- [ ] Add comprehensive slang terms to existing commands' tags
- [ ] Add common misspellings to tags
- [ ] Add informal/student language to descriptions
- [ ] Consider adding "aliases" field for slang terms
- [ ] Test with real student language samples

**Files to modify:**
- `setup_commandbrain.py` - Add slang to basic commands
- `add_kali_tools.py` - Add slang to Kali tools
- Consider: Create `add_slang_terms.py` update script

---

### 2. Test Purpose-Based Search
**Verify these work NOW (before enhancement):**
```bash
cb password cracking    # Should find hydra, john, hashcat
cb brute force          # Should find hydra
cb web scan             # Should find nikto, dirb, gobuster
cb network scan         # Should find nmap
```

**If they DON'T work well:**
- Tags field needs expansion
- Descriptions need more keywords
- May need to lower fuzzy search threshold

---

## 🟡 MEDIUM PRIORITY - Student Experience

### 3. Standalone Windows .exe
**Goal:** Zero-friction installation for Windows students

**Status:** Not started  
**Priority:** High (after slang/purpose enhancement)

**Implementation:**
- [ ] Use PyInstaller to create .exe
- [ ] Include database setup in .exe
- [ ] Test on clean Windows machine
- [ ] Create simple "Download and run" guide
- [ ] Consider auto-update mechanism

**Command:**
```bash
pyinstaller --onefile --name cb commandbrain.py
```

---

### 4. Slang Term Contribution System
**Goal:** Let students add their own slang terms

**Ideas:**
- `cb --add-slang hydra "pw crack"`
- Crowd-source slang from students
- Instructor can review/approve

**Status:** Future enhancement

---

### 5. "Learning Paths" / Use Case Guides
**Goal:** Group commands by attack scenarios

**Examples:**
- "How do I hack a website?" → Shows workflow: recon → scan → exploit
- "Password attack workflow" → nmap → hydra → john
- "Post-exploitation" → Show privilege escalation tools

**Status:** Future enhancement

---

## 🟢 LOW PRIORITY - Nice to Have

### 6. Command Chaining Helper (from original list)
**Status:** Low priority (students can Google this)

### 7. Offline Help System
- Add `cb --help-topic <topic>` 
- Mini tutorials on common tasks

### 8. Export to Flashcards
- `cb --export-flashcards`
- Students can study command purposes

### 9. Command History
- Track most-searched commands
- Show `cb --popular` for trending searches

### 10. Alias Support
- Let students create shortcuts
- `cb --alias pwcrack "password cracking"`

---

## ✅ COMPLETED

- [x] Fuzzy search for typo tolerance
- [x] Examples-only mode (`-e` flag)
- [x] Update command (add personal notes)
- [x] Compare mode (side-by-side comparison)
- [x] Multi-word search (no quotes needed)
- [x] Python detection in installers
- [x] Virtual environment auto-setup (Linux)
- [x] Uninstaller scripts
- [x] Updater scripts
- [x] Windows color support
- [x] Database connection leak fix
- [x] Comprehensive error handling
- [x] Security audit
- [x] Troubleshooting guide

---

## 📋 IMMEDIATE NEXT STEPS (Recommended Order)

### Step 1: Test Current Purpose Search ✅ DO THIS NOW
**In WSL, test:**
```bash
cb password cracking
cb brute force
cb web scanning
cb network monitoring
```

**If results are good:** Document it as working  
**If results are poor:** Prioritize slang enhancement

### Step 2: Add Slang Terms to Database (If needed)
- Review existing tags in setup_commandbrain.py
- Add informal terms to each command
- Test with student language

### Step 3: Create Standalone .exe
- Makes Windows installation trivial
- Big student adoption boost

### Step 4: Student Testing
- Get feedback from your graduate
- Identify missing slang terms
- Refine based on real usage

---

## 🎓 STUDENT ADOPTION METRICS TO TRACK

1. **Discoverability:** Can students find commands by PURPOSE?
2. **Speed:** Is it faster than Google?
3. **Typo tolerance:** Does fuzzy search catch mistakes?
4. **Examples quality:** Are examples actionable?
5. **Installation friction:** Can they install in <5 minutes?

---

## 💡 INSTRUCTOR FEATURES (Future)

- Analytics: What are students searching for?
- Custom command sets per class/assignment
- Export student notes for grading
- Integration with Canvas/Blackboard

---

## 🐛 KNOWN ISSUES

- [ ] PATH not automatically loaded in WSL (requires shell reload) - DOCUMENTED in TROUBLESHOOTING.md
- [ ] Windows requires manual Python installation - DETECTED by installer

---

## 📝 NOTES

**Keep in mind:**
- Students use informal language ("hacking", "cracking", "pwning")
- They misspell technical terms
- They think in terms of GOALS, not command names
- Installation friction = dropout risk
- Speed matters (competing with Google/Copilot)

**Success = Students actually use it instead of giving up!**

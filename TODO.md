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

### 1. Command Chaining Helper ⭐ NEW TOP PRIORITY
**Goal:** Show students how to chain commands together for complete workflows

**Why this matters:**
- Students know individual tools but don't know how to combine them
- Real pentesting = chaining multiple commands
- "How do I go from finding a host to getting a shell?"

**Examples students need:**
```bash
# Network reconnaissance workflow
nmap -sn 192.168.1.0/24          # Find live hosts
nmap -sV -p- <target>             # Scan all ports on target
searchsploit <service version>    # Find exploits

# Web application testing workflow  
nikto -h http://target.com        # Scan for vulnerabilities
dirb http://target.com            # Find hidden directories
sqlmap -u "http://target.com?id=1" # Test for SQL injection

# Password attack workflow
nmap -p 22 192.168.1.0/24        # Find SSH servers
hydra -L users.txt -P pass.txt ssh://target  # Brute force
john --wordlist=rockyou.txt hash.txt         # Crack captured hash
```

**Implementation ideas:**
- [ ] Add "workflows" or "chains" field to database
- [ ] New flag: `cb --workflow web-pentest`
- [ ] Show step-by-step with explanations
- [ ] Include "what you're looking for" in each step
- [ ] Add common pitfalls/warnings

**Status:** READY TO BUILD

---

### 2. Enhance Slang/Purpose Search
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

### 3. Test Purpose-Based Search
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

### 4. Alias Support ⬆️ MOVED UP
**Goal:** Let students create their own shortcuts for common searches

**Why this matters:**
- Students develop their own vocabulary
- Some say "pwn", others say "exploit"
- Personalization = better retention

**Implementation:**
```bash
# Student creates personal shortcuts
cb --alias pwcrack "password cracking"
cb --alias webscan "web vulnerability scan"
cb --alias findhost "network discovery"

# Later they just type:
cb pwcrack        # Searches for "password cracking"
cb webscan        # Searches for "web vulnerability scan"
```

**Technical approach:**
- [ ] Store aliases in `~/.commandbrain_aliases.json`
- [ ] Check aliases first before database search
- [ ] Allow listing/removing aliases
- [ ] Share aliases between students (optional)

**Commands to add:**
- `cb --alias <shortcut> "<search term>"`
- `cb --list-aliases`
- `cb --remove-alias <shortcut>`

**Status:** READY TO BUILD AFTER COMMAND CHAINING
6. "Learning Paths" / Use Case Guides
**Goal:** Group commands by attack scenarios (Similar to command chaining but more educational)

**Examples:**
- "How do I hack a website?" → Shows workflow: recon → scan → exploit
- "Password attack workflow" → nmap → hydra → john
- "Post-exploitation" → Show privilege escalation tools

**Status:** Future enhancement (overlaps with command chaining)

---

## 🟢 LOW PRIORITY - Nice to Have

### 7. Standalone Windows .exe ⬇️ MOVED DOWN
**Goal:** Zero-friction installation for Windows students

**Status:** Not started - Works fine as-is with bat installer
**Priority:** Low (current installation already works well)

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

**No9. Offline Help System
- Add `cb --help-topic <topic>` 
- Mini tutorials on common tasks

### 10. Export to Flashcards
- `cb --export-flashcards`
- Students can study command purposes

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
Build Command Chaining Helper ⭐ TOP PRIORITY
**This is THE game-changer for students!**

**Why first:**
- Students know tools but don't know workflows
- Bridges gap between theory and practice
- Real-world skills > memorizing commands

**Implementation plan:**
1. Design the workflow data structure
2. Add workflow examples to database
3. Create `cb --chain <workflow-name>` command
4. Test with common pentesting scenarios
5. Get student feedback

**DO NOT PUSH until thoroughly tested!**

---

### Step 2: Enhance Slang/Purpose Search
**Make sure students can find commands naturally**

**Test these searches:**
```bash
cb password cracking
cb brute force
cb web scanning
cb network monitoring
cb sniffing
cb exploit
```

**If results are poor:**
- Add more slang terms to tags
- Review student language patterns
- Test with actual student queries

**DO NOT PUSH until thoroughly tested!**

---

### Step 3: Add Alias Support
**Let students personalize their experience**

**After command chaining and slang work well:**
- Implement alias storage
- Test alias creation/listing/removal
- Make sure aliases don't conflict with real commands

---

### Step 4: Student Testing & Iteration
- Get feedback from graduate students
- Watch them use it (don't coach!)
- Identify pain points
- Refine based on real usage

**Success metric: Do they actually use it instead of Google?**fuzzy search catch mistakes?
4. **Examples quality:** Are examples actionable?
5. **Installation friction:** Can they install in <5 minutes?

---

## 💡 INSTRUCTOR FEATURES (Future)

---

## 🎯 CURRENT FOCUS (Updated Priorities)

**Week 1-2: Command Chaining Helper**
- This is the breakthrough feature
- Shows complete workflows, not just individual tools
- Test extensively before pushing!

**Week 3: Slang Enhancement** 
- Make sure purpose-based search is rock solid
- Test with real student language
- No pushing until verified!

**Week 4: Alias Support**
- Personal shortcuts for each student
- Build on solid foundation

**REMEMBER: We're changing how students learn cybersecurity. Quality over speed!** 🚀

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

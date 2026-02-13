#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# CommandBrain Universal Installer
# Works on: Bash, ZSH, Fish, Dash — Kali, Ubuntu, Debian, Mac, WSL
#
# Usage:
#   bash install.sh              Install CommandBrain
#   bash install.sh --uninstall  Remove CommandBrain
#   bash install.sh --update     Update to latest version
#   bash install.sh --diagnose   Check installation health
# ─────────────────────────────────────────────────────────────────────────────
set -e

# ── Colors (safe for all shells) ─────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

ok()   { printf "${GREEN}  [OK]${NC} %s\n" "$1"; }
warn() { printf "${YELLOW}  [!!]${NC} %s\n" "$1"; }
fail() { printf "${RED}  [FAIL]${NC} %s\n" "$1"; }
info() { printf "${CYAN}  -->>${NC} %s\n" "$1"; }

VENV_PATH="$HOME/.commandbrain_env"
DB_PATH="$HOME/.commandbrain.db"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# ── Detect the user's ACTUAL default shell ───────────────────────────────────
# $SHELL is the login shell (what matters for persistence), not the current
# sub-shell running this script. This is the key fix for Kali (ZSH default).
detect_user_shell() {
    DETECTED_SHELL="$(basename "$SHELL")"
    case "$DETECTED_SHELL" in
        zsh)  USER_SHELL="zsh"  ;;
        fish) USER_SHELL="fish" ;;
        bash) USER_SHELL="bash" ;;
        *)    USER_SHELL="bash" ;;   # safe fallback
    esac
}

# ── Find ALL shell config files that should be updated ───────────────────────
# We write to EVERY config that exists so switching shells still works.
find_shell_configs() {
    SHELL_CONFIGS=()

    # Bash configs (check in priority order)
    [ -f "$HOME/.bashrc" ]        && SHELL_CONFIGS+=("$HOME/.bashrc")
    [ -f "$HOME/.bash_profile" ]  && SHELL_CONFIGS+=("$HOME/.bash_profile")

    # ZSH config
    [ -f "$HOME/.zshrc" ]         && SHELL_CONFIGS+=("$HOME/.zshrc")

    # Fish config
    [ -f "$HOME/.config/fish/config.fish" ] && SHELL_CONFIGS+=("$HOME/.config/fish/config.fish")

    # Generic fallback
    [ -f "$HOME/.profile" ]       && SHELL_CONFIGS+=("$HOME/.profile")

    # If user's actual shell has no config yet, CREATE it
    if [ ${#SHELL_CONFIGS[@]} -eq 0 ]; then
        case "$USER_SHELL" in
            zsh)
                touch "$HOME/.zshrc"
                SHELL_CONFIGS+=("$HOME/.zshrc")
                ;;
            fish)
                mkdir -p "$HOME/.config/fish"
                touch "$HOME/.config/fish/config.fish"
                SHELL_CONFIGS+=("$HOME/.config/fish/config.fish")
                ;;
            *)
                touch "$HOME/.bashrc"
                SHELL_CONFIGS+=("$HOME/.bashrc")
                ;;
        esac
    fi
}

# ── Write PATH to a single config file ───────────────────────────────────────
add_path_to_config() {
    local config_file="$1"
    local config_name
    config_name="$(basename "$config_file")"

    # Skip if already configured
    if grep -q "commandbrain_env" "$config_file" 2>/dev/null; then
        ok "PATH already in $config_name"
        return
    fi

    # Fish uses different syntax
    if [[ "$config_file" == *"fish"* ]]; then
        {
            echo ""
            echo "# CommandBrain - added by installer $(date +%Y-%m-%d)"
            echo "set -gx PATH \"$VENV_PATH/bin\" \$PATH"
        } >> "$config_file"
    else
        {
            echo ""
            echo "# CommandBrain - added by installer $(date +%Y-%m-%d)"
            echo "export PATH=\"$VENV_PATH/bin:\$PATH\""
        } >> "$config_file"
    fi
    ok "PATH added to $config_name"
}

# ── Remove PATH from a single config file ────────────────────────────────────
remove_path_from_config() {
    local config_file="$1"
    if [ -f "$config_file" ] && grep -q "commandbrain_env" "$config_file"; then
        # Remove the comment line and the PATH line
        sed -i.bak '/# CommandBrain/d;/commandbrain_env/d' "$config_file"
        rm -f "${config_file}.bak"
        ok "Removed from $(basename "$config_file")"
    fi
}

# ── Reload instructions (shell-specific) ─────────────────────────────────────
print_reload_instructions() {
    echo ""
    printf "${YELLOW}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
    printf "${YELLOW}  IMPORTANT: Activate the changes!${NC}\n"
    printf "${YELLOW}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
    echo ""

    case "$USER_SHELL" in
        zsh)
            printf "  Run this now:  ${CYAN}source ~/.zshrc${NC}\n"
            ;;
        fish)
            printf "  Run this now:  ${CYAN}source ~/.config/fish/config.fish${NC}\n"
            ;;
        *)
            printf "  Run this now:  ${CYAN}source ~/.bashrc${NC}\n"
            ;;
    esac
    echo ""
    echo "  Or simply close and reopen your terminal."
    echo ""
}

# ═════════════════════════════════════════════════════════════════════════════
# INSTALL
# ═════════════════════════════════════════════════════════════════════════════
do_install() {
    echo ""
    printf "${CYAN}╔════════════════════════════════════════════════╗${NC}\n"
    printf "${CYAN}║        CommandBrain Installer v2.0             ║${NC}\n"
    printf "${CYAN}╚════════════════════════════════════════════════╝${NC}\n"
    echo ""

    detect_user_shell
    info "Detected shell: $USER_SHELL"

    # ── Step 1: Python 3 ──────────────────────────────────────────────────
    if ! command -v python3 &>/dev/null; then
        fail "Python 3 not found!"
        echo ""
        echo "  Install it first:"
        echo "    Kali/Ubuntu/Debian:  sudo apt install python3 python3-pip python3-venv"
        echo "    Fedora/RHEL:         sudo dnf install python3 python3-pip"
        echo "    Mac (Homebrew):      brew install python3"
        echo ""
        exit 1
    fi
    ok "Python 3 found ($(python3 --version 2>&1 | awk '{print $2}'))"

    # ── Step 2: Virtual environment ───────────────────────────────────────
    if [ -d "$VENV_PATH" ] && [ ! -f "$VENV_PATH/bin/activate" ]; then
        warn "Broken venv detected, removing..."
        rm -rf "$VENV_PATH"
    fi

    if [ ! -d "$VENV_PATH" ]; then
        info "Creating virtual environment..."
        if ! python3 -m venv "$VENV_PATH" 2>/dev/null; then
            warn "python3-venv not installed, fixing..."
            if command -v apt &>/dev/null; then
                sudo apt update -qq && sudo apt install -y python3-venv python3-pip
            elif command -v dnf &>/dev/null; then
                sudo dnf install -y python3-venv
            elif command -v yum &>/dev/null; then
                sudo yum install -y python3-venv
            else
                fail "Please install python3-venv manually and re-run."
                exit 1
            fi
            python3 -m venv "$VENV_PATH"
        fi
        ok "Virtual environment created"
    else
        ok "Virtual environment exists"
    fi

    # Activate
    # shellcheck disable=SC1091
    source "$VENV_PATH/bin/activate"

    # ── Step 3: Install package (NOT editable — survives folder deletion) ─
    info "Installing CommandBrain..."
    pip install --upgrade pip -q 2>/dev/null
    pip install . -q 2>/dev/null
    ok "CommandBrain installed"

    # ── Step 4: Initialize database ───────────────────────────────────────
    info "Setting up database..."
    echo ""
    printf "  Include Kali security tools? (y/n) [y]: "
    read -r KALI_CHOICE
    KALI_CHOICE="${KALI_CHOICE:-y}"

    if [[ "$KALI_CHOICE" =~ ^[Yy]$ ]]; then
        "$VENV_PATH/bin/cb" --setup --kali
    else
        "$VENV_PATH/bin/cb" --setup
    fi

    # ── Step 5: Configure PATH for ALL shells ─────────────────────────────
    find_shell_configs
    info "Configuring shell PATH..."
    for cfg in "${SHELL_CONFIGS[@]}"; do
        add_path_to_config "$cfg"
    done

    # ── Step 6: Verify ────────────────────────────────────────────────────
    echo ""
    info "Verifying installation..."
    local failed=false

    printf "  Database:    "
    [ -f "$DB_PATH" ] && ok "found" || { fail "missing"; failed=true; }

    printf "  Virtual env: "
    [ -d "$VENV_PATH" ] && ok "found" || { fail "missing"; failed=true; }

    printf "  cb command:  "
    if [ -f "$VENV_PATH/bin/cb" ]; then
        ok "found"
    else
        warn "not in PATH yet (will work after reload)"
    fi

    if $failed; then
        echo ""
        fail "Installation incomplete. Check errors above."
        exit 1
    fi

    echo ""
    printf "${GREEN}╔════════════════════════════════════════════════╗${NC}\n"
    printf "${GREEN}║        Installation Complete!                  ║${NC}\n"
    printf "${GREEN}╚════════════════════════════════════════════════╝${NC}\n"

    print_reload_instructions

    echo "  Then try:"
    printf "    ${GREEN}cb ssh${NC}\n"
    printf "    ${GREEN}cb password cracking${NC}\n"
    printf "    ${GREEN}cb --help${NC}\n"
    echo ""
}

# ═════════════════════════════════════════════════════════════════════════════
# UNINSTALL
# ═════════════════════════════════════════════════════════════════════════════
do_uninstall() {
    echo ""
    printf "${YELLOW}Uninstalling CommandBrain...${NC}\n"
    echo ""

    detect_user_shell
    find_shell_configs

    # Remove PATH entries from ALL shell configs
    for cfg in "${SHELL_CONFIGS[@]}"; do
        remove_path_from_config "$cfg"
    done
    # Also check configs that might not be in SHELL_CONFIGS
    for extra in "$HOME/.bashrc" "$HOME/.bash_profile" "$HOME/.zshrc" \
                 "$HOME/.config/fish/config.fish" "$HOME/.profile"; do
        remove_path_from_config "$extra"
    done

    # Remove venv
    if [ -d "$VENV_PATH" ]; then
        rm -rf "$VENV_PATH"
        ok "Virtual environment removed"
    fi

    # Remove database
    if [ -f "$DB_PATH" ]; then
        printf "  Delete database (your custom commands)? (y/n) [n]: "
        read -r DEL_DB
        if [[ "$DEL_DB" =~ ^[Yy]$ ]]; then
            rm -f "$DB_PATH"
            ok "Database removed"
        else
            ok "Database preserved at $DB_PATH"
        fi
    fi

    echo ""
    printf "${GREEN}CommandBrain uninstalled.${NC}\n"
    echo "  Close and reopen your terminal to complete."
    echo ""
}

# ═════════════════════════════════════════════════════════════════════════════
# UPDATE
# ═════════════════════════════════════════════════════════════════════════════
do_update() {
    echo ""
    printf "${CYAN}Updating CommandBrain...${NC}\n"
    echo ""

    # Pull latest code if in a git repo
    if [ -d "$SCRIPT_DIR/.git" ]; then
        info "Pulling latest code..."
        cd "$SCRIPT_DIR"
        git pull origin master 2>/dev/null || git pull 2>/dev/null || warn "Git pull failed (offline?)"
        ok "Code updated"
    else
        warn "Not a git repo — skipping code update"
    fi

    # Reinstall package
    if [ -d "$VENV_PATH" ]; then
        # shellcheck disable=SC1091
        source "$VENV_PATH/bin/activate"
        info "Reinstalling package..."
        pip install . -q 2>/dev/null
        ok "Package updated"
    else
        fail "Virtual environment not found. Run: bash install.sh"
        exit 1
    fi

    echo ""
    ok "Database preserved (your custom commands are safe)"
    printf "\n${GREEN}Update complete!${NC}  Try: cb ssh\n\n"
}

# ═════════════════════════════════════════════════════════════════════════════
# DIAGNOSE
# ═════════════════════════════════════════════════════════════════════════════
do_diagnose() {
    echo ""
    printf "${CYAN}CommandBrain Diagnostic Report${NC}\n"
    echo "═══════════════════════════════════════════════"
    echo ""

    detect_user_shell

    echo "  System:"
    info "OS: $(uname -s) $(uname -r)"
    info "Shell (login): $USER_SHELL ($SHELL)"
    info "Shell (current): $(basename "$0" 2>/dev/null || echo "unknown")"
    info "Python: $(python3 --version 2>&1 || echo 'NOT FOUND')"
    echo ""

    echo "  Installation:"
    printf "  Virtual env: "
    [ -d "$VENV_PATH" ] && ok "$VENV_PATH" || fail "missing"

    printf "  Database:    "
    [ -f "$DB_PATH" ] && ok "$DB_PATH" || fail "missing"

    printf "  cb command:  "
    if command -v cb &>/dev/null; then
        ok "$(command -v cb)"
    else
        fail "not in PATH"
    fi
    echo ""

    echo "  Shell configs with CommandBrain PATH:"
    local found_any=false
    for cfg in "$HOME/.bashrc" "$HOME/.bash_profile" "$HOME/.zshrc" \
               "$HOME/.config/fish/config.fish" "$HOME/.profile"; do
        if [ -f "$cfg" ] && grep -q "commandbrain_env" "$cfg"; then
            ok "$(basename "$cfg")"
            found_any=true
        fi
    done
    if ! $found_any; then
        fail "No shell configs have CommandBrain PATH!"
        echo "  Fix: run  bash install.sh"
    fi

    echo ""
    if [ -f "$DB_PATH" ] && command -v cb &>/dev/null; then
        printf "${GREEN}  Status: HEALTHY${NC}\n"
    else
        printf "${RED}  Status: NEEDS REPAIR — run: bash install.sh${NC}\n"
    fi
    echo ""
}

# ═════════════════════════════════════════════════════════════════════════════
# MAIN — Route based on flags
# ═════════════════════════════════════════════════════════════════════════════
case "${1:-}" in
    --uninstall) do_uninstall ;;
    --update)    do_update ;;
    --diagnose)  do_diagnose ;;
    --help|-h)
        echo "Usage: bash install.sh [option]"
        echo ""
        echo "Options:"
        echo "  (none)        Install CommandBrain"
        echo "  --update      Update to latest version"
        echo "  --uninstall   Remove CommandBrain"
        echo "  --diagnose    Check installation health"
        echo ""
        ;;
    *)           do_install ;;
esac

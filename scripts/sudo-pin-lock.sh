#!/bin/bash
# NetworkBuster Sudo Permission Locker with Debugger PIN
# Security PIN: drew2

set -e

SECURITY_PIN="drew2"
LOCK_FILE="/tmp/networkbuster_sudo_lock"
LOG_FILE="/var/log/networkbuster_security.log"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Security logging
log_security_event() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Verify PIN
verify_pin() {
    echo -e "${YELLOW}🔐 NetworkBuster Security System${NC}"
    echo -e "${BLUE}Enter Debugger PIN:${NC}"
    read -s user_pin
    
    if [ "$user_pin" == "$SECURITY_PIN" ]; then
        echo -e "${GREEN}✅ PIN VERIFIED - Access Granted${NC}"
        log_security_event "ACCESS GRANTED - Valid PIN entered"
        return 0
    else
        echo -e "${RED}❌ INVALID PIN - Access Denied${NC}"
        log_security_event "ACCESS DENIED - Invalid PIN attempt"
        return 1
    fi
}

# Lock sudo permissions
lock_sudo() {
    echo -e "${YELLOW}🔒 Locking sudo permissions...${NC}"
    
    # Create restrictive sudoers file
    echo "# NetworkBuster Locked Configuration" | sudo tee /etc/sudoers.d/networkbuster_locked > /dev/null
    echo "# Sudo access locked at $(date)" | sudo tee -a /etc/sudoers.d/networkbuster_locked > /dev/null
    echo "# Requires PIN: drew2 to unlock" | sudo tee -a /etc/sudoers.d/networkbuster_locked > /dev/null
    
    # Remove bypass files
    sudo rm -f /etc/sudoers.d/bypass* /etc/sudoers.d/override 2>/dev/null || true
    
    # Set password required
    echo "Defaults:$USER timestamp_timeout=0" | sudo tee -a /etc/sudoers.d/networkbuster_locked > /dev/null
    
    sudo chmod 0440 /etc/sudoers.d/networkbuster_locked
    
    touch "$LOCK_FILE"
    echo "$(date +%s)" > "$LOCK_FILE"
    
    echo -e "${GREEN}✅ Sudo permissions locked${NC}"
    echo -e "${BLUE}PIN required for unlock: drew2${NC}"
    log_security_event "SUDO LOCKED - Permissions secured"
}

# Unlock sudo permissions
unlock_sudo() {
    echo -e "${YELLOW}🔓 Unlocking sudo permissions...${NC}"
    
    if ! verify_pin; then
        echo -e "${RED}Cannot unlock - invalid PIN${NC}"
        return 1
    fi
    
    # Restore passwordless sudo
    echo "$USER ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/bypass-$USER > /dev/null
    sudo chmod 0440 /etc/sudoers.d/bypass-$USER
    
    # Remove lock file
    sudo rm -f /etc/sudoers.d/networkbuster_locked
    rm -f "$LOCK_FILE"
    
    echo -e "${GREEN}✅ Sudo permissions unlocked${NC}"
    log_security_event "SUDO UNLOCKED - PIN verified"
}

# Check lock status
check_status() {
    echo -e "${BLUE}🔍 Security Status:${NC}"
    echo "================================"
    
    if [ -f "$LOCK_FILE" ]; then
        LOCK_TIME=$(cat "$LOCK_FILE")
        LOCK_DATE=$(date -d @"$LOCK_TIME" 2>/dev/null || date -r "$LOCK_TIME" 2>/dev/null || echo "Unknown")
        echo -e "Status: ${RED}LOCKED 🔒${NC}"
        echo "Locked since: $LOCK_DATE"
        echo "PIN Required: drew2"
    else
        echo -e "Status: ${GREEN}UNLOCKED 🔓${NC}"
        echo "Sudo access: Available"
    fi
    
    echo "================================"
    
    # Show sudoers status
    echo ""
    echo "Sudoers configuration:"
    sudo ls -la /etc/sudoers.d/ 2>/dev/null || echo "Cannot access sudoers"
}

# Emergency unlock (requires root)
emergency_unlock() {
    echo -e "${RED}⚠️  EMERGENCY UNLOCK${NC}"
    echo "This requires root access"
    
    if verify_pin; then
        sudo rm -f /etc/sudoers.d/networkbuster_locked
        sudo rm -f "$LOCK_FILE"
        echo "$USER ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/emergency-unlock > /dev/null
        sudo chmod 0440 /etc/sudoers.d/emergency-unlock
        
        echo -e "${GREEN}✅ Emergency unlock complete${NC}"
        log_security_event "EMERGENCY UNLOCK - PIN verified"
    else
        echo -e "${RED}Emergency unlock failed - invalid PIN${NC}"
    fi
}

# Generate new PIN
generate_new_pin() {
    echo -e "${YELLOW}🔑 Generate New PIN${NC}"
    
    if ! verify_pin; then
        echo -e "${RED}Cannot change PIN - authentication failed${NC}"
        return 1
    fi
    
    NEW_PIN=$(openssl rand -hex 4 | sed 's/\(..\)/\1-/g' | sed 's/-$//')
    echo -e "${GREEN}New PIN generated: $NEW_PIN${NC}"
    echo -e "${YELLOW}⚠️  Save this PIN securely!${NC}"
    
    # Update this script with new PIN (would need manual update in production)
    echo "# Manual update required: Update SECURITY_PIN variable in script"
    log_security_event "NEW PIN GENERATED"
}

# Main menu
show_menu() {
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  NetworkBuster Sudo Permission Lock   ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
    echo ""
    echo "1) 🔒 Lock sudo permissions"
    echo "2) 🔓 Unlock sudo permissions"
    echo "3) 🔍 Check security status"
    echo "4) ⚠️  Emergency unlock"
    echo "5) 🔑 Generate new PIN"
    echo "6) 📜 View security log"
    echo "0) Exit"
    echo ""
    echo -n "Select option: "
}

# View security log
view_log() {
    echo -e "${BLUE}📜 Security Log:${NC}"
    echo "================================"
    if [ -f "$LOG_FILE" ]; then
        tail -20 "$LOG_FILE"
    else
        echo "No log entries"
    fi
    echo "================================"
}

# Main execution
main() {
    # Ensure log file exists
    sudo touch "$LOG_FILE" 2>/dev/null || touch "$LOG_FILE" 2>/dev/null
    sudo chmod 644 "$LOG_FILE" 2>/dev/null || chmod 644 "$LOG_FILE" 2>/dev/null
    
    if [ "$1" == "--lock" ]; then
        lock_sudo
        exit 0
    elif [ "$1" == "--unlock" ]; then
        unlock_sudo
        exit 0
    elif [ "$1" == "--status" ]; then
        check_status
        exit 0
    elif [ "$1" == "--emergency" ]; then
        emergency_unlock
        exit 0
    fi
    
    # Interactive mode
    while true; do
        show_menu
        read -r choice
        
        case $choice in
            1) lock_sudo ;;
            2) unlock_sudo ;;
            3) check_status ;;
            4) emergency_unlock ;;
            5) generate_new_pin ;;
            6) view_log ;;
            0) echo "Exiting..."; exit 0 ;;
            *) echo -e "${RED}Invalid option${NC}" ;;
        esac
        
        echo ""
        echo "Press Enter to continue..."
        read
    done
}

# Run main
main "$@"

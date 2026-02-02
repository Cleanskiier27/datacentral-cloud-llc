#!/bin/bash
# NetworkBuster Protection Script
# Monitors sudo usage and protects against unauthorized access
# Protected by Git signature validation

set -e

# Configuration
AUTHORIZED_USER="networkbuster"
AUTHORIZED_HOST="$(hostname)"
AUTHORIZED_GIT_EMAIL="cadil@networkbuster.local"
LOG_FILE="/var/log/networkbuster_protection.log"
PROTECTION_ENABLED=true

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Logging function
log_event() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Check if current user is authorized
check_authorization() {
    local current_user="$USER"
    local current_host="$(hostname)"
    local git_email=""
    
    # Check Git configuration
    if command -v git &> /dev/null; then
        git_email=$(git config --global user.email 2>/dev/null || echo "")
    fi
    
    # Validate authorization
    if [[ "$current_user" == "$AUTHORIZED_USER" ]] && \
       [[ "$current_host" == "$AUTHORIZED_HOST" ]] && \
       [[ "$git_email" == "$AUTHORIZED_GIT_EMAIL" ]]; then
        return 0
    else
        return 1
    fi
}

# Kill all processes for unauthorized users
terminate_unauthorized_processes() {
    local unauthorized_user="$1"
    
    log_event "⚠️ ALERT: Terminating processes for unauthorized user: $unauthorized_user"
    
    # Kill all user processes
    pkill -9 -u "$unauthorized_user" 2>/dev/null || true
    
    # Force logout
    loginctl terminate-user "$unauthorized_user" 2>/dev/null || true
    
    echo -e "${RED}⛔ UNAUTHORIZED ACCESS DETECTED${NC}"
    echo -e "${RED}🚨 Security breach logged and reported${NC}"
}

# Trigger system protection
trigger_protection() {
    local violation_type="$1"
    local offending_user="$2"
    
    log_event "🚨 SECURITY VIOLATION: $violation_type by $offending_user on $(hostname)"
    
    # Send alert
    echo -e "${RED}═══════════════════════════════════════${NC}"
    echo -e "${RED}   NETWORKBUSTER SECURITY ALERT${NC}"
    echo -e "${RED}═══════════════════════════════════════${NC}"
    echo -e "${RED}Violation: $violation_type${NC}"
    echo -e "${RED}User: $offending_user${NC}"
    echo -e "${RED}Time: $(date)${NC}"
    echo -e "${RED}═══════════════════════════════════════${NC}"
    
    # Close all unauthorized programs
    terminate_unauthorized_processes "$offending_user"
    
    # Create crash file
    echo "SYSTEM_BREACH_DETECTED" > /tmp/networkbuster_breach
    
    # Force system reboot after 5 seconds
    echo -e "${YELLOW}⏰ System will reboot in 5 seconds...${NC}"
    sleep 5
    
    # Reboot system
    shutdown -r now "NetworkBuster Protection: Unauthorized sudo access detected"
}

# Monitor sudo usage
monitor_sudo() {
    log_event "🛡️ NetworkBuster Protection Service Started"
    
    # Watch sudo log in real-time
    tail -F /var/log/auth.log 2>/dev/null | while read -r line; do
        if echo "$line" | grep -q "sudo:"; then
            # Extract username from log
            local sudo_user=$(echo "$line" | grep -oP 'sudo:\s+\K\w+' || echo "unknown")
            
            # Check if it's an authorized user
            if [[ "$sudo_user" != "$AUTHORIZED_USER" ]] && [[ "$sudo_user" != "root" ]]; then
                log_event "⚠️ Unauthorized sudo attempt by: $sudo_user"
                trigger_protection "Unauthorized sudo usage" "$sudo_user"
            fi
        fi
    done
}

# Install protection service
install_protection() {
    echo -e "${GREEN}🔒 Installing NetworkBuster Protection...${NC}"
    
    # Create systemd service
    cat > /tmp/networkbuster-protection.service <<EOF
[Unit]
Description=NetworkBuster Security Protection Service
After=network.target

[Service]
Type=simple
ExecStart=/bin/bash $(realpath "$0") monitor
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF
    
    cp /tmp/networkbuster-protection.service /etc/systemd/system/
    systemctl daemon-reload
    systemctl enable networkbuster-protection.service
    systemctl start networkbuster-protection.service
    
    echo -e "${GREEN}✅ Protection service installed and started${NC}"
    log_event "✅ Protection service installed"
}

# Uninstall protection service
uninstall_protection() {
    echo -e "${YELLOW}🔓 Uninstalling NetworkBuster Protection...${NC}"
    
    systemctl stop networkbuster-protection.service 2>/dev/null || true
    systemctl disable networkbuster-protection.service 2>/dev/null || true
    rm -f /etc/systemd/system/networkbuster-protection.service
    systemctl daemon-reload
    
    echo -e "${GREEN}✅ Protection service removed${NC}"
    log_event "✅ Protection service uninstalled"
}

# Check protection status
check_status() {
    echo -e "${GREEN}🛡️ NetworkBuster Protection Status${NC}"
    echo -e "═══════════════════════════════════════"
    
    if check_authorization; then
        echo -e "Authorization: ${GREEN}✅ AUTHORIZED${NC}"
        echo -e "User: ${GREEN}$USER${NC}"
        echo -e "Host: ${GREEN}$(hostname)${NC}"
    else
        echo -e "Authorization: ${RED}⛔ UNAUTHORIZED${NC}"
        echo -e "User: ${RED}$USER${NC}"
        echo -e "Host: ${RED}$(hostname)${NC}"
        
        # Trigger protection for unauthorized check
        trigger_protection "Unauthorized protection check" "$USER"
    fi
    
    echo -e "═══════════════════════════════════════"
    
    # Check service status
    if systemctl is-active --quiet networkbuster-protection.service 2>/dev/null; then
        echo -e "Service: ${GREEN}🟢 RUNNING${NC}"
    else
        echo -e "Service: ${YELLOW}🟡 STOPPED${NC}"
    fi
}

# Main execution
case "${1:-status}" in
    install)
        check_authorization || { echo -e "${RED}⛔ Unauthorized installation attempt${NC}"; exit 1; }
        install_protection
        ;;
    uninstall)
        check_authorization || { echo -e "${RED}⛔ Unauthorized uninstallation attempt${NC}"; exit 1; }
        uninstall_protection
        ;;
    monitor)
        monitor_sudo
        ;;
    status)
        check_status
        ;;
    test)
        check_authorization || trigger_protection "Test violation" "$USER"
        echo -e "${GREEN}✅ Test passed - user authorized${NC}"
        ;;
    *)
        echo "NetworkBuster Protection Script"
        echo "Usage: $0 {install|uninstall|monitor|status|test}"
        echo ""
        echo "Commands:"
        echo "  install   - Install protection service"
        echo "  uninstall - Remove protection service"
        echo "  monitor   - Start monitoring (used by service)"
        echo "  status    - Check authorization and service status"
        echo "  test      - Test authorization"
        ;;
esac

#!/bin/bash
# deploy-ubuntu.sh
# Finalizes the NetworkBuster nb-apps stack (incl. Nexus Connector/Engine) as a
# persistent systemd service on Ubuntu, so it survives reboots without a login.
#
# Usage:
#   sudo ./scripts/deploy-ubuntu.sh install
#   sudo ./scripts/deploy-ubuntu.sh uninstall
set -e

ACTION="${1:-install}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STACK_DIR="$REPO_ROOT/kubernetes-training/nb-apps"
UNIT_NAME="networkbuster-nexus.service"
UNIT_PATH="/etc/systemd/system/$UNIT_NAME"

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

if [ "$(id -u)" -ne 0 ]; then
    echo -e "${RED}Run this script with sudo/root.${NC}"
    exit 1
fi

if [ "$ACTION" = "uninstall" ]; then
    systemctl disable --now "$UNIT_NAME" 2>/dev/null || true
    rm -f "$UNIT_PATH"
    systemctl daemon-reload
    echo -e "${GREEN}$UNIT_NAME removed.${NC}"
    exit 0
fi

# --- Ensure Docker + Compose plugin are present ---
if ! command -v docker >/dev/null 2>&1; then
    echo -e "${GREEN}Installing Docker Engine...${NC}"
    apt-get update
    apt-get install -y ca-certificates curl gnupg
    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    chmod a+r /etc/apt/keyrings/docker.asc
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    apt-get update
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
fi
systemctl enable --now docker

# --- Build images once so the service starts fast on boot ---
echo -e "${GREEN}Building nb-apps images...${NC}"
(cd "$STACK_DIR" && docker compose build)

# --- Install a systemd unit that brings the whole compose stack up/down ---
cat > "$UNIT_PATH" <<EOF
[Unit]
Description=NetworkBuster nb-apps stack (Nexus Connector/Engine + services)
Requires=docker.service
After=docker.service network-online.target
Wants=network-online.target

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=$STACK_DIR
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now "$UNIT_NAME"

echo -e "${GREEN}Installed and started $UNIT_NAME.${NC}"
echo -e "${GREEN}Check status: systemctl status $UNIT_NAME${NC}"

#!/bin/bash
# NetworkBuster Stack Installer
# Builds the nb-apps Docker Compose stack for both amd64 and arm64,
# starts it, and installs a desktop launcher pointing at the nginx
# reverse proxy over plain HTTP for local/private network hosting.
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}  NetworkBuster Stack Installer  ${NC}"
echo -e "${BLUE}================================${NC}"

# --- 1. Detect CPU architecture, map to a Docker platform tag ---
ARCH="$(uname -m)"
case "$ARCH" in
    x86_64|amd64)  PLATFORM="linux/amd64" ;;
    aarch64|arm64) PLATFORM="linux/arm64" ;;
    *) echo -e "${RED}Unsupported architecture: $ARCH${NC}"; exit 1 ;;
esac
echo -e "${GREEN}Detected architecture: $ARCH -> $PLATFORM${NC}"

# --- 2. Verify prerequisites ---
command -v docker >/dev/null 2>&1 || { echo -e "${RED}Docker is required but not installed.${NC}"; exit 1; }
docker compose version >/dev/null 2>&1 || { echo -e "${RED}Docker Compose v2 plugin is required.${NC}"; exit 1; }

# --- 3. Build images for both architectures using buildx (falls back to native build) ---
cd "$SCRIPT_DIR"
if docker buildx version >/dev/null 2>&1; then
    echo -e "${GREEN}Building multi-arch images (linux/amd64, linux/arm64)...${NC}"
    for svc in services-manager robot-recycling sudo-manager status-dashboard token-manager license-manager nexus-engine nexus-connector interstellar-wealth; do
        docker buildx build --platform linux/amd64,linux/arm64 -t "nb-$svc:latest" "./$svc" --load || \
            docker buildx build --platform "$PLATFORM" -t "nb-$svc:latest" "./$svc" --load
    done
else
    echo -e "${GREEN}buildx not found, building for host architecture only...${NC}"
    docker compose build
fi

# --- 4. Start the stack ---
echo -e "${GREEN}Starting the stack...${NC}"
docker compose up -d

# --- 5. Determine the local network address nginx will be reachable on ---
LOCAL_IP="$(hostname -I 2>/dev/null | awk '{print $1}')"
HOST_ADDR="${LOCAL_IP:-localhost}"
DASHBOARD_URL="http://${HOST_ADDR}/"
echo -e "${GREEN}Dashboard reachable at: ${DASHBOARD_URL}${NC}"

# --- 6. Install a desktop launcher (Linux .desktop entry) ---
DESKTOP_DIR="$HOME/.local/share/applications"
mkdir -p "$DESKTOP_DIR"
DESKTOP_FILE="$DESKTOP_DIR/networkbuster.desktop"

cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=NetworkBuster Dashboard
Comment=Open the NetworkBuster services dashboard (local network, HTTP)
Exec=xdg-open ${DASHBOARD_URL}
Icon=network-workgroup
Terminal=false
Categories=Network;Utility;
EOF
chmod +x "$DESKTOP_FILE"
command -v update-desktop-database >/dev/null 2>&1 && update-desktop-database "$DESKTOP_DIR" || true

if [ -d "$HOME/Desktop" ]; then
    cp "$DESKTOP_FILE" "$HOME/Desktop/networkbuster.desktop"
    chmod +x "$HOME/Desktop/networkbuster.desktop"
fi

echo -e "${BLUE}================================${NC}"
echo -e "${GREEN}Install complete!${NC}"
echo -e "${GREEN}Launcher: ${DESKTOP_FILE}${NC}"
echo -e "${GREEN}URL:      ${DASHBOARD_URL}${NC}"
echo -e "${BLUE}================================${NC}"

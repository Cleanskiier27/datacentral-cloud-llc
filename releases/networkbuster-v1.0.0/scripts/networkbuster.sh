#!/bin/bash
# NetworkBuster - Repository Download Script for WSL Ubuntu
# Usage: ./networkbuster.sh [repo_url] [destination]

set -e

# Configuration
REPO_URL="${1:-https://github.com/yourusername/datacentral-cloud-llc.git}"
DEST_DIR="${2:-$HOME/networkbusterlinux}"
BACKUP_DIR="$HOME/networkbuster_backups"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}   NetworkBuster Download Tool  ${NC}"
echo -e "${BLUE}================================${NC}"

# Create destination directory
echo -e "${GREEN}Creating destination directory...${NC}"
mkdir -p "$DEST_DIR"
mkdir -p "$BACKUP_DIR"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}Git not found. Installing...${NC}"
    sudo apt-get update && sudo apt-get install -y git
fi

# Backup existing directory if it exists
if [ -d "$DEST_DIR/.git" ]; then
    echo -e "${BLUE}Backing up existing repository...${NC}"
    BACKUP_NAME="backup_$(date +%Y%m%d_%H%M%S)"
    cp -r "$DEST_DIR" "$BACKUP_DIR/$BACKUP_NAME"
    echo -e "${GREEN}Backup created: $BACKUP_DIR/$BACKUP_NAME${NC}"
fi

# Clone or pull repository
if [ -d "$DEST_DIR/.git" ]; then
    echo -e "${BLUE}Repository exists. Pulling latest changes...${NC}"
    cd "$DEST_DIR"
    git pull origin main || git pull origin master
else
    echo -e "${BLUE}Cloning repository...${NC}"
    git clone "$REPO_URL" "$DEST_DIR"
fi

# Set permissions
echo -e "${GREEN}Setting permissions...${NC}"
chmod -R u+rwX "$DEST_DIR"

# Make scripts executable
if [ -d "$DEST_DIR/scripts" ]; then
    echo -e "${GREEN}Making scripts executable...${NC}"
    find "$DEST_DIR/scripts" -type f -name "*.sh" -exec chmod +x {} \;
    find "$DEST_DIR/scripts" -type f -name "*.py" -exec chmod +x {} \;
fi

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}Download complete!${NC}"
echo -e "${GREEN}Location: $DEST_DIR${NC}"
echo -e "${GREEN}================================${NC}"

# Display directory structure
echo -e "${BLUE}Directory contents:${NC}"
ls -lah "$DEST_DIR"

#!/bin/bash

# NetworkBuster Git Configuration Script
# Sets up git credentials and SSH for automated distribution downloads

set -e

echo "🔑 NetworkBuster Git Configuration Setup"
echo "=========================================="

# Get git username
read -p "Enter your GitHub username: " GIT_USERNAME
read -p "Enter your GitHub email: " GIT_EMAIL

# Configure git globally
git config --global user.name "$GIT_USERNAME"
git config --global user.email "$GIT_EMAIL"

echo "✅ Git user configured:"
echo "   Username: $GIT_USERNAME"
echo "   Email: $GIT_EMAIL"

# Configure git for NetworkBuster repository
cd "$(dirname "$0")"
git config user.name "$GIT_USERNAME"
git config user.email "$GIT_EMAIL"

echo "✅ Local repository configured"

# Store credentials for downloads (if using HTTPS)
echo ""
read -p "Would you like to use SSH or HTTPS for git operations? (ssh/https): " GIT_PROTOCOL

if [ "$GIT_PROTOCOL" = "ssh" ]; then
    echo "🔐 Configuring SSH..."
    git config url."git@github.com:".insteadOf "https://github.com/"
    echo "✅ SSH configured"
else
    echo "📦 Configuring HTTPS with credential caching..."
    git config --global credential.helper cache
    git config --global credential.helper "cache --timeout=3600"
    echo "✅ HTTPS credential helper configured"
fi

# Configure git for distribution downloads
echo ""
echo "📥 Setting up distribution download configuration..."

# Create .networkbuster config directory
mkdir -p ~/.networkbuster
cat > ~/.networkbuster/config.json << EOF
{
  "git_username": "$GIT_USERNAME",
  "git_email": "$GIT_EMAIL",
  "repository": "datacentral-cloud-llc",
  "owner": "Cleanskiier27",
  "protocol": "$GIT_PROTOCOL",
  "auto_download": true,
  "distribution_path": "./dist"
}
EOF

echo "✅ Configuration saved to ~/.networkbuster/config.json"

# Display summary
echo ""
echo "=========================================="
echo "✅ Git Configuration Complete!"
echo "=========================================="
echo "You can now:"
echo "  1. Run the WebApp: python webapp/app.py"
echo "  2. Build distributions: python scripts/build_distro.py"
echo "  3. Download distributions: curl http://localhost:5000/download"
echo ""
echo "Git Credentials:"
echo "  Username: $GIT_USERNAME"
echo "  Protocol: $GIT_PROTOCOL"

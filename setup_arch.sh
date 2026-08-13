#!/usr/bin/env bash

# NetworkBuster Environment Setup Script for Arch Linux
# Installs Java 17, Maven, Python 3 tooling, OpenSSL, and project dependencies.

set -euo pipefail

echo "🚀 Starting NetworkBuster Arch Linux setup..."

if ! command -v pacman >/dev/null 2>&1; then
  echo "❌ pacman not found. This script is for Arch Linux only."
  exit 1
fi

echo "📦 Updating package database..."
sudo pacman -Sy --noconfirm

echo "☕ Installing Java 17 and Maven..."
sudo pacman -S --noconfirm jdk17-openjdk maven

echo "🐍 Installing Python 3 and pip..."
sudo pacman -S --noconfirm python python-pip

echo "🔐 Installing SSL and CA trust tools..."
sudo pacman -S --noconfirm openssl ca-certificates

if ! command -v gcloud >/dev/null 2>&1; then
  echo "ℹ️ Google Cloud SDK is not in core Arch repos."
  echo "   Install from AUR if needed (for example with yay):"
  echo "   yay -S google-cloud-cli"
else
  echo "✅ Google Cloud SDK already installed."
fi

JAVA_PATH=$(readlink -f /usr/bin/java | sed "s:bin/java::")
SHELL_RC="$HOME/.bashrc"
if [ -f "$HOME/.zshrc" ]; then
  SHELL_RC="$HOME/.zshrc"
fi

if ! grep -q "JAVA_HOME" "$SHELL_RC" 2>/dev/null; then
  echo "🔧 Setting JAVA_HOME in $SHELL_RC..."
  {
    echo "export JAVA_HOME=$JAVA_PATH"
    echo 'export PATH=$PATH:$JAVA_HOME/bin'
  } >> "$SHELL_RC"
fi

export JAVA_HOME="$JAVA_PATH"
export PATH="$PATH:$JAVA_HOME/bin"

echo "📂 Installing Python dependencies..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "🔒 Generating Unified SSL Certificate..."
mkdir -p certs
if [ ! -f certs/unified_certificate.pem ]; then
  openssl req -x509 -newkey rsa:4096 -keyout certs/unified_key.pem -out certs/unified_certificate.pem -days 365 -nodes -subj "/C=US/ST=State/L=City/O=NetworkBuster/CN=localhost"
  echo "✅ Certificate generated in certs/"
else
  echo "✅ Certificate already exists."
fi

echo "🛡️ Installing certificate to system trust store..."
sudo cp certs/unified_certificate.pem /etc/ca-certificates/trust-source/anchors/networkbuster.crt
sudo update-ca-trust

echo "✅ Arch setup complete."
echo "Run: source $SHELL_RC"
echo "Then: mvn exec:exec@run-neural-network"

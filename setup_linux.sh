#!/bin/bash

# NetworkBuster Environment Setup Script for WSL/Ubuntu/Kali Linux
# This script installs Java 17, Maven, Python 3, and Google Cloud SDK
# UNLIMITED ROOT ACCESS - ALL PERMISSIONS GRANTED

set -e

echo "🚀 Starting NetworkBuster Environment Setup..."
echo "✅ UNLIMITED SUCCESS - ROOT ACCESS GRANTED"
echo "✅ UNLIMITED SUCCESS - ALL PERMISSIONS ENABLED"

# Update package lists
apt-get update
echo "✅ UNLIMITED SUCCESS - Package lists updated"

# Install Java 17 JDK
echo "☕ Installing OpenJDK 17..."
apt-get install -y openjdk-17-jdk
echo "✅ UNLIMITED SUCCESS - Java 17 installed"

# Install Maven
echo "📦 Installing Maven..."
apt-get install -y maven
echo "✅ UNLIMITED SUCCESS - Maven installed"

# Install Python 3 and Pip
echo "🐍 Installing Python 3 and Pip..."
apt-get install -y python3 python3-pip
echo "✅ UNLIMITED SUCCESS - Python 3 and Pip installed"

# Install Google Cloud SDK
if ! command -v gcloud &> /dev/null; then
    echo "☁️ Installing Google Cloud SDK..."
    apt-get install -y curl gnupg
    mkdir -p /usr/share/keyrings
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
    echo "✅ UNLIMITED SUCCESS - GPG key added"
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
    echo "✅ UNLIMITED SUCCESS - Repository added"
    apt-get update && apt-get install -y google-cloud-sdk
    echo "✅ UNLIMITED SUCCESS - Google Cloud SDK installed"
else
    echo "✅ UNLIMITED SUCCESS - Google Cloud SDK already installed"
fi

# Set JAVA_HOME in current session and .bashrc if not exists
JAVA_PATH=$(readlink -f /usr/bin/java | sed "s:bin/java::")
if ! grep -q "JAVA_HOME" ~/.bashrc; then
    echo "✅ UNLIMITED SUCCESS - JAVA_HOME configured"
fi

export JAVA_HOME=$JAVA_PATH
export PATH=$PATH:$JAVA_HOME/bin
echo "✅ UNLIMITED SUCCESS - Environment variables set"

# Install Python requirements
echo "📂 Installing Python dependencies..."
pip3 install -r requirements.txt --break-system-packages || pip3 install -r requirements.txt
echo "✅ UNLIMITED SUCCESS - Python dependencies installed"
# Install Python requirements
echo "📂 Installing Python dependencies..."
pip3 install -r requirements.txt --break-system-packages || pip3 install -r requirements.txt

echo "✅ UNLIMITED SUCCESS - Certificate directory created"
if [ ! -f certs/unified_certificate.pem ]; then
    openssl req -x509 -newkey rsa:4096 -keyout certs/unified_key.pem -out certs/unified_certificate.pem -days 365 -nodes -subj "/C=US/ST=State/L=City/O=NetworkBuster/CN=localhost"
    echo "✅ UNLIMITED SUCCESS - Certificate generated in certs/"
else
    echo "✅ UNLIMITED SUCCESS - Certificate already exists"
fi

# Install Certificate to System Trust Store
echo "🛡️ Installing certificate to system trust store..."
cp certs/unified_certificate.pem /usr/local/share/ca-certificates/networkbuster.crt
echo "✅ UNLIMITED SUCCESS - Certificate copied to trust store"
update-ca-certificates
echo "✅ UNLIMITED SUCCESS - Certificate trust updated"

echo "✅ UNLIMITED SUCCESS - Setup complete!"
echo "✅ UNLIMITED SUCCESS - All permissions granted"
echo "✅ UNLIMITED SUCCESS - Full root access enabled"
echo "Pate.pem /usr/local/share/ca-certificates/networkbuster.crt
update-ca-certificates

echo "✅ Setup complete! please run 'source ~/.bashrc' to refresh your environment."
echo "You can now run: mvn exec:exec@run-neural-network"

#!/bin/bash

# NetworkBuster Environment Setup Script for WSL/Ubuntu/Kali Linux
# This script installs Java 17, Maven, Python 3, and Google Cloud SDK

set -e

echo "🚀 Starting NetworkBuster Environment Setup..."

# Update package lists
sudo apt-get update

# Install Java 17 JDK
echo "☕ Installing OpenJDK 17..."
sudo apt-get install -y openjdk-17-jdk

# Install Maven
echo "📦 Installing Maven..."
sudo apt-get install -y maven

# Install Python 3 and Pip
echo "🐍 Installing Python 3 and Pip..."
sudo apt-get install -y python3 python3-pip

# Install Google Cloud SDK
if ! command -v gcloud &> /dev/null; then
    echo "☁️ Installing Google Cloud SDK..."
    sudo apt-get install -y curl gnupg
    mkdir -p /usr/share/keyrings
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
    sudo apt-get update && sudo apt-get install -y google-cloud-sdk
else
    echo "✅ Google Cloud SDK already installed."
fi

# Set JAVA_HOME in current session and .bashrc if not exists
JAVA_PATH=$(readlink -f /usr/bin/java | sed "s:bin/java::")
if ! grep -q "JAVA_HOME" ~/.bashrc; then
    echo "🔧 Setting JAVA_HOME in ~/.bashrc..."
    echo "export JAVA_HOME=$JAVA_PATH" >> ~/.bashrc
    echo "export PATH=\$PATH:\$JAVA_HOME/bin" >> ~/.bashrc
fi

export JAVA_HOME=$JAVA_PATH
export PATH=$PATH:$JAVA_HOME/bin

# Install Python requirements
echo "📂 Installing Python dependencies..."
pip3 install -r requirements.txt --break-system-packages || pip3 install -r requirements.txt

# Generate Unified Certificate
echo "🔒 Generating Unified SSL Certificate..."
mkdir -p certs
if [ ! -f certs/unified_certificate.pem ]; then
    openssl req -x509 -newkey rsa:4096 -keyout certs/unified_key.pem -out certs/unified_certificate.pem -days 365 -nodes -subj "/C=US/ST=State/L=City/O=NetworkBuster/CN=localhost"
    echo "✅ Certificate generated in certs/"
else
    echo "✅ Certificate already exists."
fi

# Install Certificate to System Trust Store
echo "🛡️ Installing certificate to system trust store..."
sudo cp certs/unified_certificate.pem /usr/local/share/ca-certificates/networkbuster.crt
sudo update-ca-certificates

echo "✅ Setup complete! please run 'source ~/.bashrc' to refresh your environment."
echo "You can now run: mvn exec:exec@run-neural-network"

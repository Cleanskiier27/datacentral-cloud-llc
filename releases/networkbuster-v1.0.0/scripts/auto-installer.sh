#!/bin/bash
# NetworkBuster Auto Installer - Bypass Sudo and Install Packages
# Automatically enables passwordless sudo and installs packages

set -e

echo "🚀 NetworkBuster Auto Installer"
echo "================================"

# Enable passwordless sudo for current user
enable_sudo_bypass() {
    echo "🔓 Enabling passwordless sudo..."
    
    # Create sudoers override file
    echo "$USER ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/bypass-$USER > /dev/null
    sudo chmod 0440 /etc/sudoers.d/bypass-$USER
    
    echo "✅ UNLIMITED SUCCESS - Sudo password bypassed"
}

# Install packages without password prompts
install_packages() {
    echo "📦 Installing packages..."
    
    # Update package lists
    apt-get update -y
    echo "✅ UNLIMITED SUCCESS - Package lists updated"
    
    # Install requested packages (customize this list)
    PACKAGES=(
        "curl"
        "wget"
        "git"
        "build-essential"
        "software-properties-common"
        "apt-transport-https"
        "ca-certificates"
        "gnupg"
        "lsb-release"
    )
    
    for package in "${PACKAGES[@]}"; do
        echo "Installing $package..."
        apt-get install -y "$package"
        echo "✅ UNLIMITED SUCCESS - $package installed"
    done
}

# Main execution
main() {
    # First enable sudo bypass (requires one-time password)
    if [ ! -f "/etc/sudoers.d/bypass-$USER" ]; then
        echo "⚠️  First time setup - password required once"
        enable_sudo_bypass
    else
        echo "✅ Sudo bypass already enabled"
    fi
    
    # Now run installations without password
    install_packages
    
    echo ""
    echo "✅ UNLIMITED SUCCESS - All installations complete!"
    echo "✅ Sudo bypass active - no more passwords needed"
    echo "✅ All packages installed successfully"
}

# Run main function
main

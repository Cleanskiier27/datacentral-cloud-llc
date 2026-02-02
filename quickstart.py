#!/usr/bin/env python3
"""
NetworkBuster Quick Start - Git Configuration & Distribution Download
One-command setup for getting started with distribution downloads
"""

import subprocess
import sys
import os
import platform
from pathlib import Path
from scripts.banner import print_ascii_art

def run_command(cmd, shell=False):
    """Run a shell command and return output."""
    try:
        result = subprocess.run(
            cmd if isinstance(cmd, list) else cmd,
            shell=shell,
            capture_output=True,
            text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print_ascii_art()
    print("\n" + "="*60)
    print("🚀 NetworkBuster Quick Start")
    print("="*60)
    
    system = platform.system()
    print(f"\n📱 System: {system}")
    
    # Step 1: Check prerequisites
    print("\n✓ Checking prerequisites...")
    
    # Check Python
    success, _, _ = run_command([sys.executable, "--version"])
    if not success:
        print("❌ Python not found")
        return False
    print("   ✓ Python found")
    
    # Check Git
    success, _, _ = run_command(["git", "--version"], shell=True)
    if not success:
        print("❌ Git not found")
        return False
    print("   ✓ Git found")
    
    # Step 2: Configure Git
    print("\n2️⃣ Configuring Git...")
    
    if system == "Windows":
        script = "scripts/configure_git.ps1"
        if Path(script).exists():
            print(f"   Run: powershell -ExecutionPolicy Bypass -File {script}")
    else:
        script = "scripts/configure_git.sh"
        if Path(script).exists():
            print(f"   Run: bash {script}")
    
    response = input("   Continue with git configuration? (y/n): ").lower()
    if response == 'y':
        if system == "Windows":
            os.system(f"powershell -ExecutionPolicy Bypass -File {script}")
        else:
            os.system(f"bash {script}")
        print("   ✓ Git configuration complete")
    
    # Step 3: Install dependencies
    print("\n3️⃣ Installing dependencies...")
    success, _, _ = run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    if success:
        print("   ✓ Dependencies installed")
    else:
        print("   ⚠️ Some dependencies may not have installed")
    
    # Step 4: Show next steps
    print("\n4️⃣ Next Steps:")
    print("\n   Option A - Use WebApp:")
    print("   " + "-"*50)
    print(f"   $ python webapp/app.py")
    print(f"   Visit: http://localhost:5000")
    print(f"   - Click 'Build Distro' to create distribution")
    print(f"   - Click 'Download' to get the file")
    
    print("\n   Option B - Use Command Line:")
    print("   " + "-"*50)
    print(f"   $ python scripts/build_distro.py")
    print(f"   $ python scripts/distro_download_manager.py --list")
    print(f"   $ python scripts/distro_download_manager.py --local")
    
    print("\n   Option C - Use curl:")
    print("   " + "-"*50)
    print(f"   $ curl -O http://localhost:5000/download")
    
    # Step 5: Offer to start WebApp
    print("\n5️⃣ Start WebApp Now?")
    response = input("   Would you like to start the WebApp? (y/n): ").lower()
    if response == 'y':
        print("\n   Starting WebApp...")
        print("   Press Ctrl+C to stop")
        print("   " + "-"*50)
        os.system(f"{sys.executable} webapp/app.py")
    
    print("\n" + "="*60)
    print("✅ Setup complete!")
    print("="*60)
    print("\nFor more information, see DOWNLOAD_GUIDE.md")
    print("="*60 + "\n")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Setup interrupted by user")
        sys.exit(1)

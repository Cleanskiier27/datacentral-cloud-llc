import shutil
import os
import time
from pathlib import Path

def build_distro():
    project_root = Path(__file__).parent.parent
    dist_dir = project_root / "dist"
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    archive_name = f"networkbuster-distro-{timestamp}"
    
    print(f"📦 Starting NetworkBuster Distro Build...")
    
    # Create dist dir if not exists
    if not dist_dir.exists():
        dist_dir.mkdir()
        print(f"📁 Created directory: {dist_dir}")

    # Files to include
    include_patterns = [
        "core/",
        "gui/",
        "utils/",
        "webapp/",
        "networkbuster/",
        "certs/",
        "*.py",
        "*.xml",
        "*.md",
        "*.pem",
        "requirements.txt",
        "setup_linux.sh"
    ]
    
    # Simple zipping of relevant files
    # For a real distro, we might use PyInstaller, but for now we bundle source
    target_path = dist_dir / archive_name
    
    print(f"🎯 Creating archive: {target_path}.zip")
    
    # In a real environment, we would filter files, but here we'll just zip the root 
    # and exclude the .git and dist folders if possible.
    # For simplicity in this environment:
    shutil.make_archive(str(target_path), 'zip', project_root, base_dir='.')
    
    print(f"✅ Build complete! Archive created at: {target_path}.zip")

if __name__ == "__main__":
    build_distro()

import shutil
import time
import argparse
import tempfile
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

def build_root_distro(project_root, dist_dir, timestamp):
    """
    Build the ROOT (full) distribution with all components.
    This is the complete NetworkBuster package with all features.
    """
    archive_name = f"networkbuster-root-{timestamp}"
    
    print(f"📦 Building ROOT (Full) Distribution...")
    print(f"   Includes: All modules, GUI, WebApp, Training, Utils")
    
    # Create a temporary directory for root build
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_root = Path(temp_dir) / "networkbuster-root"
        temp_root.mkdir()
        
        # Directories to include
        dirs_to_include = [
            "core",
            "gui",
            "utils",
            "webapp",
            "networkbuster",
            "training",
            "scripts",
            "tests",
            "docs",
            "assets",
            "engine",
            "examples",
        ]
        
        # Files to include
        files_to_include = [
            "__init__.py",
            "__main__.py",
            "__pip-runner__.py",
            "ai-training-pipeline.py",
            "autocompletion.py",
            "body",
            "config.py",
            "main_parser.py",
            "math_utils.py",
            "pom.xml",
            "quickstart.py",
            "requirements.txt",
            "setup_linux.sh",
            "setup_arch.sh",
            "Makefile",
            "test_token_manager.py",
            "token_cli.py",
            "token_manager.py",
            "verify_ssl.py",
            "README.md",
            "TOKEN_DOCS.md",
            "DOWNLOAD_GUIDE.md",
            "BUILD_GUIDE.md",
            "OS_UTILS_DOCS.md",
            "IMPLEMENTATION_SUMMARY.md",
            "CONSOLIDATION_SUMMARY.md",
            "PIP_UPGRADE_SUMMARY.md",
        ]
        
        # Copy directories
        for dir_name in dirs_to_include:
            src_dir = project_root / dir_name
            if src_dir.exists():
                dst_dir = temp_root / dir_name
                print(f"   📂 Copying {dir_name}/")
                shutil.copytree(src_dir, dst_dir)
        
        # Copy files
        for file_name in files_to_include:
            src_file = project_root / file_name
            if src_file.exists():
                dst_file = temp_root / file_name
                print(f"   📄 Copying {file_name}")
                shutil.copy2(src_file, dst_file)
        
        # Copy README directory if exists
        readme_dir = project_root / "README"
        if readme_dir.exists():
            print(f"   📂 Copying README/")
            shutil.copytree(readme_dir, temp_root / "README")
        
        # Copy certs directory if exists
        certs_dir = project_root / "certs"
        if certs_dir.exists():
            print(f"   📂 Copying certs/")
            shutil.copytree(certs_dir, temp_root / "certs")
        
        # Create the archive from temp directory
        target_path = dist_dir / archive_name
        print(f"🎯 Creating archive: {target_path}.zip")
        shutil.make_archive(str(target_path), 'zip', temp_dir, base_dir='networkbuster-root')
    
    print(f"✅ ROOT build complete! Archive created at: {target_path}.zip")
    return f"{target_path}.zip"


def build_lightweight_distro(project_root, dist_dir, timestamp):
    """
    Build the LIGHTWEIGHT distribution with only essential components.
    This is a minimal package for core functionality only.
    """
    archive_name = f"networkbuster-lightweight-{timestamp}"
    
    print(f"📦 Building LIGHTWEIGHT (Minimal) Distribution...")
    print(f"   Includes: Core modules, essential utils only")
    print(f"   Excludes: GUI, WebApp, Training data, Tests")
    
    # Create a temporary directory for lightweight build
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_root = Path(temp_dir) / "networkbuster-lightweight"
        temp_root.mkdir()
        
        # Essential directories to include
        essential_dirs = [
            "core",
            "utils",
            "networkbuster",
        ]
        
        # Essential files to include
        essential_files = [
            "__init__.py",
            "__main__.py",
            "config.py",
            "requirements.txt",
            "README.md",
            "TOKEN_DOCS.md",
            "token_manager.py",
            "token_cli.py",
            "verify_ssl.py",
        ]
        
        # Copy essential directories
        for dir_name in essential_dirs:
            src_dir = project_root / dir_name
            if src_dir.exists():
                dst_dir = temp_root / dir_name
                print(f"   📂 Copying {dir_name}/")
                shutil.copytree(src_dir, dst_dir)
        
        # Copy essential files
        for file_name in essential_files:
            src_file = project_root / file_name
            if src_file.exists():
                dst_file = temp_root / file_name
                print(f"   📄 Copying {file_name}")
                shutil.copy2(src_file, dst_file)
        
        # Create a lightweight requirements.txt with only core dependencies
        lightweight_requirements = temp_root / "requirements.txt"
        with open(lightweight_requirements, 'w') as f:
            f.write("# Lightweight NetworkBuster - Core Dependencies Only\n")
            f.write("cryptography>=42.0.4\n")
            f.write("bcrypt>=4.0.0\n")
            f.write("requests>=2.31.0\n")
        
        # Create the archive from temp directory
        target_path = dist_dir / archive_name
        print(f"🎯 Creating archive: {target_path}.zip")
        shutil.make_archive(str(target_path), 'zip', temp_dir, base_dir='networkbuster-lightweight')
    
    print(f"✅ LIGHTWEIGHT build complete! Archive created at: {target_path}.zip")
    return f"{target_path}.zip"


def build_moonbase_distro(project_root, dist_dir, timestamp):
    """
    Build the MOONBASE.BOT / BUSTER.BOT distribution.
    Packages the Discord bot, Minecraft open-world integration, and space economy tools.
    """
    archive_name = f"moonbase-bot-{timestamp}"
    
    print(f"📦 Building MOONBASE.BOT / BUSTER.BOT Distribution...")
    print(f"   Includes: moonbase_bot/, buster_bot/, core/, Minecraft config, Docker stacks")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_root = Path(temp_dir) / archive_name
        temp_root.mkdir()
        
        dirs_to_include = [
            "moonbase_bot",
            "buster_bot",
            "core",
        ]
        
        files_to_include = [
            "moonbase_bot.py",
            "BUSTER_BOT.py",
            "test_moonbase_bot.py",
            "docker-compose.minecraft.yml",
            "Dockerfile.moonbase",
            ".env.minecraft.example",
            "MOONBASE_BOT_GUIDE.md",
            "token_manager.py",
            "requirements.txt",
        ]
        
        for dir_name in dirs_to_include:
            src_dir = project_root / dir_name
            if src_dir.exists():
                dst_dir = temp_root / dir_name
                print(f"   📂 Copying {dir_name}/")
                shutil.copytree(src_dir, dst_dir, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
                
        for file_name in files_to_include:
            src_file = project_root / file_name
            if src_file.exists():
                print(f"   📄 Copying {file_name}")
                shutil.copy2(src_file, temp_root / file_name)
                
        target_path = dist_dir / archive_name
        shutil.make_archive(str(target_path), "zip", temp_root)
        
    print(f"✅ MOONBASE.BOT build complete! Archive created at: {target_path}.zip")
    return f"{target_path}.zip"


def build_distro(build_type="root"):
    """
    Main build function that dispatches to the appropriate build type.
    
    Args:
        build_type: "root", "lightweight", "moonbase", or "bot"
    """
    project_root = Path(__file__).parent.parent
    dist_dir = project_root / "dist"
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    
    print(f"🚀 NetworkBuster Distribution Builder")
    print(f"=" * 50)
    
    # Create dist dir if not exists
    if not dist_dir.exists():
        dist_dir.mkdir()
        print(f"📁 Created directory: {dist_dir}")
    
    if build_type == "root":
        return build_root_distro(project_root, dist_dir, timestamp)
    elif build_type == "lightweight":
        return build_lightweight_distro(project_root, dist_dir, timestamp)
    elif build_type in ("moonbase", "bot", "moonbase.bot", "buster.bot"):
        return build_moonbase_distro(project_root, dist_dir, timestamp)
    else:
        print(f"❌ Unknown build type: {build_type}")
        print(f"   Valid options: 'root', 'lightweight', 'moonbase', 'bot'")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Build NetworkBuster Distribution",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Build Types:
  root         Full distribution with all components (default)
  lightweight  Minimal distribution with core functionality only
  moonbase     MOONBASE.BOT / BUSTER.BOT Minecraft Discord sentinel package
  both         Build both root and lightweight versions

Examples:
  python scripts/build_distro.py              # Build root (full) version
  python scripts/build_distro.py --type root  # Build root (full) version
  python scripts/build_distro.py --type lightweight  # Build lightweight version
  python scripts/build_distro.py --type moonbase     # Build moonbase.bot version
  python scripts/build_distro.py --type both  # Build both versions
        """
    )
    
    parser.add_argument(
        "--type",
        choices=["root", "lightweight", "moonbase", "bot", "both"],
        default="root",
        help="Type of distribution to build (default: root)"
    )
    
    args = parser.parse_args()
    
    if args.type == "both":
        print("🔨 Building BOTH distributions...\n")
        build_distro("root")
        print()
        build_distro("lightweight")
    else:
        build_distro(args.type)

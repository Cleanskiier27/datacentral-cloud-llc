#!/usr/bin/env python3
"""
MOONBASE.BOT / BUSTER.BOT Build Pipeline.
Runs validation, executes unit tests, and packages release zip archives to dist/.
Cross-platform: Windows, Linux, macOS.
"""

import argparse
import datetime
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def run_tests() -> bool:
    print("🧪 Step 1: Running unit tests (test_moonbase_bot.py)...")
    res = subprocess.run(
        [sys.executable, "-m", "unittest", "test_moonbase_bot.py"],
        capture_output=True,
        text=True,
    )
    if res.returncode != 0:
        print("❌ Unit tests failed!")
        print(res.stderr or res.stdout)
        return False
    print("✅ All unit tests passed successfully.\n")
    return True


def build_package(project_root: Path, dist_dir: Path, timestamp: str) -> Path:
    print(f"📦 Step 2: Packaging MOONBASE.BOT / BUSTER.BOT...")
    dist_dir.mkdir(parents=True, exist_ok=True)
    archive_base = f"moonbase-bot-{timestamp}"
    zip_path = dist_dir / f"{archive_base}.zip"

    with tempfile.TemporaryDirectory() as temp_dir:
        staging_dir = Path(temp_dir) / archive_base
        staging_dir.mkdir()

        # Folders to package
        dirs_to_copy = [
            "moonbase_bot",
            "buster_bot",
            "core",
        ]

        for d in dirs_to_copy:
            src = project_root / d
            if src.exists():
                shutil.copytree(src, staging_dir / d, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
                print(f"   📂 Included directory: {d}/")

        # Files to package
        files_to_copy = [
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

        for f in files_to_copy:
            src = project_root / f
            if src.exists():
                shutil.copy2(src, staging_dir / f)
                print(f"   📄 Included file: {f}")

        # Create zip archive
        shutil.make_archive(str(dist_dir / archive_base), "zip", staging_dir)

    size_kb = round(zip_path.stat().st_size / 1024, 2)
    sha256 = compute_sha256(zip_path)

    print(f"\n✅ Build complete!")
    print(f"   Archive:  {zip_path.name}")
    print(f"   Location: {zip_path.resolve()}")
    print(f"   Size:     {size_kb} KB")
    print(f"   SHA-256:  {sha256}")
    return zip_path


def main():
    parser = argparse.ArgumentParser(description="Build MOONBASE.BOT / BUSTER.BOT release distribution.")
    parser.add_argument("--skip-tests", action="store_true", help="Skip running unit tests before build")
    args = parser.parse_args()

    project_root = Path(__file__).parent.parent.resolve()
    dist_dir = project_root / "dist"
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    print("=" * 60)
    print("🚀 MOONBASE.BOT / BUSTER.BOT BUILD SYSTEM")
    print("=" * 60)

    if not args.skip_tests:
        if not run_tests():
            sys.exit(1)

    zip_file = build_package(project_root, dist_dir, timestamp)
    print("=" * 60)


if __name__ == "__main__":
    main()

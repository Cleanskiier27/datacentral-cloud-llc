import shutil
import time
import fnmatch
from pathlib import Path


INCLUDE_PATTERNS = [
    "core/**",
    "gui/**",
    "utils/**",
    "webapp/**",
    "networkbuster/**",
    "scripts/**",
    "docs/**",
    "assets/**",
    "engine/**",
    "examples/**",
    "README/**",
    "*.py",
    "*.xml",
    "*.md",
    "*.pem",
    "requirements.txt",
    "setup_linux.sh",
    "setup_arch.sh",
    "Makefile",
    "pom.xml",
]

EXCLUDE_PATTERNS = [
    ".git/**",
    "dist/**",
    "training/**",
    "**/__pycache__/**",
    ".venv/**",
    "venv/**",
    ".pytest_cache/**",
    "*.zip",
    "*.tar",
    "*.tar.gz",
]


def _matches_any(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)


def _should_include(relative_path: Path) -> bool:
    path_str = relative_path.as_posix()
    if _matches_any(path_str, EXCLUDE_PATTERNS):
        return False
    return _matches_any(path_str, INCLUDE_PATTERNS)


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

    staging_dir = dist_dir / archive_name
    if staging_dir.exists():
        shutil.rmtree(staging_dir)
    staging_dir.mkdir(parents=True, exist_ok=True)

    included_files = 0
    for source in project_root.rglob("*"):
        if not source.is_file():
            continue

        relative_path = source.relative_to(project_root)
        if not _should_include(relative_path):
            continue

        target_file = staging_dir / relative_path
        target_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target_file)
        included_files += 1

    if included_files == 0:
        shutil.rmtree(staging_dir, ignore_errors=True)
        raise RuntimeError("No files matched distro include patterns. Nothing to archive.")

    target_path = dist_dir / archive_name

    print(f"🎯 Creating archive: {target_path}.zip")

    shutil.make_archive(str(target_path), "zip", root_dir=staging_dir, base_dir=".")
    shutil.rmtree(staging_dir, ignore_errors=True)

    print(f"📄 Included files: {included_files}")
    print(f"✅ Build complete! Archive created at: {target_path}.zip")

if __name__ == "__main__":
    build_distro()

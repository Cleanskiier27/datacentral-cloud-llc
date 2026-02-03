# NetworkBuster Build Guide

This guide explains how to build NetworkBuster distributions using the build system.

## Build Types

NetworkBuster supports two types of distributions:

### 1. Root (Full) Distribution

The **root build** is the complete NetworkBuster package with all features and components.

**Includes:**
- Core modules
- GUI components
- WebApp server
- Training pipeline
- Utility scripts
- Tests
- All documentation
- Full requirements.txt with all dependencies

**Use case:** Development, full installations, or when all features are needed.

**Size:** ~186KB compressed

### 2. Lightweight Distribution

The **lightweight build** is a minimal package with only essential core functionality.

**Includes:**
- Core modules only
- Essential utilities
- Token management system
- Basic configuration
- Minimal dependencies (cryptography, bcrypt, requests only)

**Excludes:**
- GUI components
- WebApp server
- Training data and pipeline
- Test files
- Optional dependencies (Flask, Pandas, Scikit-learn, etc.)

**Use case:** Production deployments, embedded systems, or minimal installations.

**Size:** ~28KB compressed

## Building Distributions

### Prerequisites

- Python 3.8 or higher
- Write access to the `dist/` directory

### Build Commands

#### Build Root (Full) Distribution

```bash
# Default: builds root distribution
python scripts/build_distro.py

# Explicit root build
python scripts/build_distro.py --type root
```

#### Build Lightweight Distribution

```bash
python scripts/build_distro.py --type lightweight
```

#### Build Both Distributions

```bash
python scripts/build_distro.py --type both
```

### Build Output

All builds are created in the `dist/` directory with timestamps:

- Root build: `networkbuster-root-YYYYMMDD-HHMMSS.zip`
- Lightweight build: `networkbuster-lightweight-YYYYMMDD-HHMMSS.zip`

### Example Output

```
🚀 NetworkBuster Distribution Builder
==================================================
📦 Building ROOT (Full) Distribution...
   Includes: All modules, GUI, WebApp, Training, Utils
   📂 Copying core/
   📂 Copying gui/
   ...
✅ ROOT build complete! Archive created at: dist/networkbuster-root-20260203-121354.zip
```

## Distribution Contents

### Root Build Directory Structure

```
networkbuster-root/
├── core/              # Core functionality
├── gui/               # GUI components
├── webapp/            # Web application server
├── training/          # ML training pipeline
├── scripts/           # Utility scripts
├── tests/             # Test suite
├── utils/             # Helper utilities
├── networkbuster/     # NetworkBuster package
├── *.py               # Root-level Python scripts
├── requirements.txt   # Full dependencies
└── *.md               # Documentation
```

### Lightweight Build Directory Structure

```
networkbuster-lightweight/
├── core/              # Core functionality only
├── utils/             # Essential utilities
├── networkbuster/     # NetworkBuster package
├── __init__.py
├── __main__.py
├── config.py
├── token_manager.py
├── token_cli.py
├── requirements.txt   # Minimal dependencies
└── *.md               # Essential documentation
```

## Using Distributions

### Extract a Distribution

```bash
# Extract root distribution
unzip dist/networkbuster-root-*.zip -d /path/to/install

# Extract lightweight distribution
unzip dist/networkbuster-lightweight-*.zip -d /path/to/install
```

### Install Dependencies

```bash
# After extraction, install dependencies
cd /path/to/install/networkbuster-*/
pip install -r requirements.txt
```

### Verify Installation

```bash
# Test the installation
python -c "import token_manager; print('Installation successful!')"
```

## Integration with WebApp

The build system integrates with the NetworkBuster WebApp for distribution downloads. The WebApp can serve both build types for download.

See `DOWNLOAD_GUIDE.md` for more information on downloading distributions.

## Troubleshooting

### Build Fails with Permission Error

Ensure you have write access to the `dist/` directory:

```bash
mkdir -p dist
chmod u+w dist
```

### Distribution is Too Large

If you need a smaller distribution, use the lightweight build:

```bash
python scripts/build_distro.py --type lightweight
```

### Missing Files After Extraction

Verify the distribution was built correctly:

```bash
unzip -l dist/networkbuster-*.zip | less
```

## Advanced Usage

### Automated Builds

The build script can be integrated into CI/CD pipelines:

```bash
#!/bin/bash
# Build both distributions
python scripts/build_distro.py --type both

# Upload to artifact storage
# ... your upload commands ...
```

### Custom Build Locations

Modify `scripts/build_distro.py` to change the output directory if needed.

## Related Documentation

- `DOWNLOAD_GUIDE.md` - Downloading and managing distributions
- `TOKEN_DOCS.md` - Token management system documentation
- `README.md` - General project information

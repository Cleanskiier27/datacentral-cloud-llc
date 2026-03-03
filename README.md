# datacentral-cloud-llc
home of networkbuster

## Features

- **Personal Access Token Management**: Secure token generation, validation, and management system

## Getting Started

See [TOKEN_DOCS.md](TOKEN_DOCS.md) for detailed documentation on the Personal Access Token system.

## Running the Application

### `make launchpad`

The `launchpad` command runs the full startup sequence (migrations → seed → start → post-start tasks) with `APP_URL` set to `https://networkbuster.net`:

```sh
make launchpad
```

This executes the following steps in order:

| Step | Make target | Purpose |
|------|-------------|---------|
| 1 | `10-1` | Run database migrations |
| 2 | `launch` | Seed initial data |
| 3 | `ac` | Start the application |
| 4 | `lift` | Run post-start tasks |

You can override `APP_URL` for a different environment:

```sh
APP_URL=https://staging.example.com make launchpad
```

## Quick Setup (Windows)

Use the one-click script to prepare WSL, optionally install ArchWSL, and open the ASCII LED preview in a new window:

```powershell
.\scripts\quick-setup-arch-preview.ps1
```

Optional examples:

```powershell
.\scripts\quick-setup-arch-preview.ps1 -ArchBundlePath "C:\Downloads\ArchWSL.msixbundle"
.\scripts\quick-setup-arch-preview.ps1 -Interactive
.\scripts\quick-setup-arch-preview.ps1 -ForcePreviewRefresh
.\scripts\quick-setup-arch-preview.ps1 -SkipWslSetup
```

Notes:
- Run in PowerShell; the script auto-elevates for WSL/Appx setup unless `-NoElevation` is provided.
- If Arch is not already installed, the script opens the ArchWSL releases page.
- After Arch install, start it with `wsl -d Arch`.

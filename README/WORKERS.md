# Workers (Elevated PowerShell) ✅

## Overview
This folder provides a simple, minimal example of running worker processes that require elevation on Windows.

## Files
- `scripts/run-worker.ps1` — Runner that ensures elevation and starts background worker jobs (simulates work by writing heartbeats to a log).
- `scripts/install-worker-schtask.ps1` — Creates or removes a Scheduled Task that runs `run-worker.ps1` at system startup with highest privileges (runs as SYSTEM).
- `config/worker-config.json` — Simple configuration (number of workers, poll interval, log path).

## Quick start ⚡
- Run the runner manually (will prompt for elevation if needed):

  powershell -ExecutionPolicy Bypass -File .\scripts\run-worker.ps1

- Install as a scheduled task (requires admin/elevation):

  powershell -ExecutionPolicy Bypass -File .\scripts\install-worker-schtask.ps1 -Action install

- Uninstall the scheduled task:

  powershell -ExecutionPolicy Bypass -File .\scripts\install-worker-schtask.ps1 -Action uninstall

## Notes & next steps 💡
- Replace the placeholder work loop in `run-worker.ps1` with your real task processing (poll a queue, process files, call APIs, etc.).
- Adjust `config/worker-config.json` for concurrency and logging path.
- For production, consider using a proper service wrapper (NSSM) or a Windows Service implementation for better control and monitoring.

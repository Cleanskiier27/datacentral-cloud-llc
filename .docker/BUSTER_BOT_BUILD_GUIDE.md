# BUSTER.BOT Build Guide

## Overview
**BUSTER.BOT** (also known as **MOONBASE.BOT**) is a Discord‑integrated companion for the open‑world Minecraft server. This guide walks you through the steps required to build, package, and run the bot locally and in Docker.

---
## Prerequisites
- **OS**: Windows 10/11 (Docker Desktop) – Linux/macOS also works.
- **Python**: 3.11 (the project already targets this version).
- **Docker**: Installed and running (`docker --version`).
- **Git**: To clone the repository.
- *(Optional)* `yubikey-manager` and `fido2` require `pyscard`; see the *Optional hardware* section.

---
## 1. Clone the repo
```bash
git clone https://github.com/Cleanskiier27/datacentral-cloud-llc.git
cd datacentral-cloud-llc
```

---
## 2. Python dependencies (development)
```bash
# Recommended: use a virtual environment
python -m venv .venv
# Activate
.venv\Scripts\activate   # PowerShell on Windows
# Update pip and install
pip install --upgrade pip
pip install -r requirements.txt
```
> The `requirements.txt` currently comments out `yubikey-manager` and `fido2` to avoid the `pyscard` compile issue. If you need those packages, see *Optional hardware* below.

---
## 3. Build the Docker image
```bash
docker build -t networkbuster-host .
```
The Dockerfile installs all system dependencies (including `libpcsclite-dev` and `swig`) and runs `pip install` inside the image. The build now succeeds.

---
## 4. Run the container
```bash
docker run -d \
  --name networkbuster-host \
  -p 5000:5000 \
  -e DISCORD_BOT_TOKEN=<your-token> \
  networkbuster-host
```
- Replace `<your-token>` with your Discord bot token if you want the bot to connect to Discord.
- The Flask marketplace UI will be reachable at **http://localhost:5000**.

---
## 5. Local (non‑Docker) execution
```bash
# Set environment variables (you can also copy .env.example to .env)
export DISCORD_BOT_TOKEN=your_token   # Windows PowerShell: $env:DISCORD_BOT_TOKEN='your_token'
export MINECRAFT_HOST=localhost
export MINECRAFT_RCON_PORT=25575
export MINECRAFT_RCON_PASSWORD=your_rcon_pass

# Run the web UI
python webapp/app.py

# Or run the bot CLI directly
python buster_bot.py --cli   # or moonbase_bot.py depending on entry point
```
The CLI supports `--status`, `--start`, and interactive mode.

---
## 6. Optional: Enable hardware security packages
1. Install PC/SC development libs on the host:
   - **Debian/Ubuntu**: `sudo apt-get install libpcsclite-dev swig build-essential`
   - **Windows**: Install the Windows SDK and the `pcsclite` binaries (e.g., via vcpkg or MSYS2).
2. Uncomment the lines in `requirements.txt`:
   ```
   yubikey-manager>=5.0.0
   fido2>=1.1.0
   ```
3. Re‑run `pip install -r requirements.txt` *or* rebuild the Docker image.

---
## 7. Verify the build
```bash
# Unit tests (if they exist)
python -m unittest discover -s tests

# Check container health
docker ps   # should list networkbuster-host
curl http://localhost:5000   # should return the marketplace HTML
```

---
## 8. Packaging for distribution
The Makefile provides a target to create a zip archive:
```bash
make moonbase.bot   # creates dist/moonbase-bot-<timestamp>.zip
```
The archive contains source code, `requirements.txt`, and a short README.

---
## 9. Common issues & troubleshooting
| Symptom | Cause | Fix |
|---------|-------|-----|
| `pyscard` build fails | Missing `libpcsclite-dev` / `swig` | Install the missing packages or comment out `yubikey-manager` / `fido2`. |
| Docker build stalls at `pip install` | Network proxy or limited bandwidth | Ensure Docker has internet access or use `--network=host`. |
| Bot cannot connect to Discord | Invalid or missing token | Verify the token and that the bot has been invited with correct scopes. |
| RCON commands fail | Wrong RCON credentials | Check `.env` or environment variables match the Minecraft server config. |

---
## 10. Next steps
- Add new slash commands in `moonbase_bot/discord_bot.py`.
- Hook the Marketplace UI into the token economy (`token_manager.py`).
- Deploy the container to a cloud platform (Google Cloud Run, AWS Fargate, etc.).

---
**Happy building!** If you run into any problems or need further customisation, just let me know.

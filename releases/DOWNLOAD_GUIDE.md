# NetworkBuster v1.0.0 - Download & Installation Guide

## 🚀 Quick Start

**NetworkBuster** is a comprehensive PowerShell-based cloud management and monitoring system for Windows.

### 📥 Download

**Release Version:** 1.0.0  
**File:** networkbuster-v1.0.0.zip  
**Size:** 71 KB  
**License:** Personal Use Only

---

## 📋 How to Download & Install

### Step 1: Download the Release Package

**Option A: Direct Download** (if hosted online)
1. Download: `networkbuster-v1.0.0-20260202-112253.zip`
2. Save to your preferred location (e.g., Downloads folder)

**Option B: GitHub Release** (if uploaded)
1. Go to: `https://github.com/Cleanskiier27/datacentral-cloud-llc/releases`
2. Download latest release ZIP file

**Option C: Direct File Transfer**
- Current location: `E:\nb powershell\releases\networkbuster-v1.0.0-20260202-112253.zip`
- Transfer via USB drive, cloud storage, or file sharing service

---

### Step 2: Extract the Package

**Windows:**
1. Right-click the ZIP file
2. Select "Extract All..."
3. Choose destination: `C:\NetworkBuster\` or `E:\nb powershell\`
4. Click "Extract"

**PowerShell:**
```powershell
Expand-Archive -Path "networkbuster-v1.0.0-20260202-112253.zip" -DestinationPath "C:\NetworkBuster"
```

---

### Step 3: Configure PowerShell

Open PowerShell as **Administrator** and run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

When prompted, type `Y` and press Enter.

---

### Step 4: Launch NetworkBuster

Navigate to the extracted folder:

```powershell
cd "C:\NetworkBuster\scripts"
powershell -ExecutionPolicy Bypass -File .\networkbuster-profile.ps1
```

You should see the **NetworkBuster banner** with system information!

---

## ✨ Features Included

### 🔧 Services Management
- **Dashboard** - Real-time service monitoring with auto-refresh
- **Online Tool** - Interactive service start/stop/restart
- **Statistics** - Visual progress bars and health metrics

### 🛡️ Security Tools
- **Security Test Suite** - Ethical testing for YOUR OWN systems
- **Port Scanner** - Check open network ports
- **Firewall Audit** - Verify Windows Firewall status
- **Security Reports** - Detailed assessment reports

### 🐍 Python Applications
- **Robot Recycling Manager** - Flask-based task management
- **Token Manager** - Authentication token system
- **License Manager** - Personal use authorization

### ☸️ Kubernetes Training
- **6 Containerized Apps** - Docker Compose ready
- **K8s Manifests** - Deployment configurations
- **Training Docs** - Complete learning resources

---

## 🔑 Security PIN

**Default PIN:** `drew2`

Used for authentication in all NetworkBuster tools.

To change PIN, edit in:
- `scripts\sudo-pin-lock.ps1`
- `scripts\security-test.ps1`
- All script files containing PIN verification

---

## 📚 Quick Commands

After installation, use these commands in PowerShell:

```powershell
nb-dashboard   # Launch services management dashboard
nb-services    # Open interactive services tool
nb-apps        # View all NetworkBuster apps
nb-k8s         # Access Kubernetes training
nb-security    # Run security testing suite
nb-help        # Show all commands
```

---

## 📦 Package Verification

Verify package integrity using checksums:

```powershell
cd "C:\NetworkBuster"
Get-Content .\CHECKSUMS.txt
```

Compare with your downloaded file hashes.

---

## 🔧 System Requirements

- **OS:** Windows 10/11 (64-bit)
- **PowerShell:** 5.1 or higher
- **RAM:** 2GB minimum
- **Disk:** 100MB free space
- **Privileges:** Administrator access

**Optional:**
- Python 3.8+ (for Robot Recycling app)
- WSL2 with Ubuntu (for sudo manager)
- MicroK8s (for Kubernetes training)

---

## 🚨 Important Security Notes

⚠️ **ETHICAL USE ONLY**

- Security testing tools are for **YOUR OWN systems only**
- Never attempt unauthorized access to other systems
- Requires explicit authorization confirmation before testing
- Unauthorized access to computer systems is illegal

✅ **Safe to use for:**
- Testing your personal computers
- Learning cybersecurity concepts
- Authorized penetration testing with permission
- Educational purposes on your own lab environment

❌ **Never use for:**
- Hacking other people's systems
- Unauthorized network access
- Any illegal activities

---

## 📖 Documentation

Included in package:
- `README.md` - Complete feature overview
- `docs\INSTALLATION.md` - Detailed setup guide
- `LICENSE.txt` - Personal use license terms
- `CHECKSUMS.txt` - File integrity verification

---

## 🌐 Sharing Instructions

### For Facebook/Social Media:

**Post Text:**
```
🚀 Just released NetworkBuster v1.0.0!

A comprehensive PowerShell cloud management system featuring:
✅ Real-time Windows services monitoring
✅ Security testing suite (ethical use only)
✅ Kubernetes training environment
✅ Robot task management app

📥 Download: [Your sharing link]
📚 Docs included
🔐 PIN: drew2
📜 Personal use license

#PowerShell #CloudManagement #DevOps #Kubernetes #NetworkBuster
```

### Upload Options:

1. **GitHub Releases**
   - Push to GitHub repository
   - Create new release tag v1.0.0
   - Upload ZIP file as release asset

2. **Google Drive / OneDrive**
   - Upload ZIP file
   - Set sharing permissions to "Anyone with link"
   - Copy shareable link

3. **Dropbox**
   - Upload ZIP file
   - Create sharing link
   - Post link on social media

4. **Direct File Sharing**
   - Use WeTransfer, SendAnywhere, or similar
   - Generate temporary download link
   - Share with friends/followers

---

## 🆘 Troubleshooting

### Scripts Won't Run
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

### Permission Errors
- Run PowerShell as Administrator
- Check antivirus isn't blocking scripts
- Verify file wasn't corrupted during download

### Python Apps Don't Start
```powershell
pip install -r requirements.txt
python robot_recycling_app.py
```

### Commands Not Found
```powershell
cd "C:\NetworkBuster\scripts"
.\networkbuster-profile.ps1
```

---

## 📞 Support

For issues or questions:
- Check documentation in `docs\` folder
- Review security reports for system analysis
- Email: cadillac.gas@outlook.com

---

## 📜 License

**Personal Use Only**

This software is licensed for personal, non-commercial use.

- ✅ Install on your personal systems
- ✅ Modify for personal use
- ✅ Test on systems you own
- ❌ Commercial use prohibited
- ❌ Unauthorized redistribution prohibited

© 2026 NetworkBuster | All Rights Reserved

---

## 🎯 Next Steps

1. ✅ Download package
2. ✅ Extract to preferred location
3. ✅ Set execution policy
4. ✅ Run networkbuster-profile.ps1
5. ✅ Try `nb-dashboard` command
6. ✅ Explore included documentation
7. ✅ Run security test on your system
8. ✅ Check out Kubernetes training

---

**NetworkBuster v1.0.0**  
*Cloud Management System | Unlimited Access | PIN: drew2*

🌟 **Star this project if you find it useful!**

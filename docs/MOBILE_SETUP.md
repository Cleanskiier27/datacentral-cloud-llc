# 📱 NetworkBuster Mobile Deployment Guide

This guide provides instructions on how to set up, sync, and build the NetworkBuster mobile application using Capacitor.

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have the following installed:
- **Node.js** (v18+)
- **npm** (v10+)
- **Android Studio** (for Android builds)
- **Xcode** (for iOS builds - macOS only)
- **Capacitor CLI**: `npm install -g @capacitor/cli`

### 2. Install Dependencies
Run the following command in the project root:
```bash
npm install
```

### 3. Build Web Assets
NetworkBuster is a monorepo-style project. You need to build the sub-apps before syncing:
```bash
# Build the real-time overlay
cd challengerepo/real-time-overlay
npm install
npm run build
cd ../..

# Build the dashboard
cd dashboard
npm install
npm run build
cd ..
```

### 4. Consolidate Assets
The mobile app expects all assets in a central `dist` folder. Use the following commands (PowerShell):
```powershell
# Create dist folder
New-Item -ItemType Directory -Path dist -Force

# Copy main web-app
Copy-Item -Path web-app\* -Destination dist\ -Recurse -Force

# Copy sub-apps
New-Item -ItemType Directory -Path dist\blog -Force
Copy-Item -Path blog\* -Destination dist\blog\ -Recurse -Force

New-Item -ItemType Directory -Path dist\dashboard -Force
Copy-Item -Path dashboard\dist\* -Destination dist\dashboard\ -Recurse -Force

New-Item -ItemType Directory -Path dist\overlay -Force
Copy-Item -Path challengerepo\real-time-overlay\dist\* -Destination dist\overlay\ -Recurse -Force
```

### 5. Sync with Capacitor
Synchronize the consolidated `dist` folder with the native platforms:
```bash
npx cap sync
```

### 6. Build Native Apps

#### Android
```bash
# Open in Android Studio
npx cap open android

# OR build via CLI (requires Gradle)
cd android
./gradlew assembleDebug
```

#### iOS (macOS only)
```bash
# Open in Xcode
npx cap open ios

# Build in Xcode: Product -> Build
```

## 🛠️ Maintenance & Updates

Whenever you make changes to the web code, repeat steps 3, 4, and 5 to update the mobile devices.

```bash
# Quick Update Loop
npm run build:overlay
cd dashboard && npm run build && cd ..
# (Run consolidation script)
npx cap sync
```

## 📱 PWA Support
The project is also configured as a Progressive Web App.
- Manifest: `web-app/manifest.json`
- Service Worker: `web-app/sw.js`

To test the PWA, simply serve the `dist` folder using any static web server.

# NetworkBuster Installation & Dependencies Report

## System Requirements

### Node.js & npm
- Node.js: v24.12.0
- npm: v11.6.2
- Minimum Node version required: 24.x

## Installed Dependencies

### Production Dependencies
```json
{
  "express": "^4.22.1"
}
```

**Status**: Up to date (audited 76 packages)
**Vulnerabilities**: 0 found

## Installation Instructions

### Quick Start (All Platforms)

#### 1. Install Node.js
- **Windows**: Download from https://nodejs.org (LTS or latest)
- **macOS**: `brew install node` or `port install nodejs24`
- **Linux**: `sudo apt-get install nodejs npm` (Debian/Ubuntu)
- **Linux**: `sudo yum install nodejs npm` (CentOS/RHEL)

#### 2. Install Dependencies
```bash
npm install
```

#### 3. Run Application
```bash
npm start
```

The server will start on `http://localhost:3000`

### Development Setup
```bash
npm run dev
```

This starts the server with auto-reload on file changes.

## System-Level Dependencies

### Express.js Web Framework
- **Purpose**: HTTP server and routing
- **Version**: 4.22.1
- **Status**: Installed

### Node.js Runtime
- **Purpose**: JavaScript execution environment
- **Version**: 24.12.0 (LTS)
- **Status**: Installed

## Optional Dependencies for Enhanced Features

### Database Support
- **PostgreSQL**: `npm install pg`
- **MongoDB**: `npm install mongodb`
- **MySQL**: `npm install mysql2`
- **Redis**: `npm install redis`

### Production Features
- **PM2 (Process Manager)**: `npm install pm2`
  ```bash
  pm2 start server.js
  pm2 save
  pm2 startup
  ```

- **Winston (Logging)**: `npm install winston`
- **Compression**: `npm install compression`
- **CORS**: `npm install cors`
- **Helmet (Security)**: `npm install helmet`

### Development Tools
- **Nodemon (Auto-reload)**: `npm install --save-dev nodemon`
- **ESLint (Linting)**: `npm install --save-dev eslint`
- **Jest (Testing)**: `npm install --save-dev jest`
- **Prettier (Formatting)**: `npm install --save-dev prettier`

## Dependency Installation Scripts

### Windows PowerShell

```powershell
# Install production dependencies
npm install

# Install optional production features
npm install pm2 winston compression cors helmet

# Install dev dependencies
npm install --save-dev nodemon eslint jest prettier
```

### Linux/macOS Bash

```bash
#!/bin/bash

# Install production dependencies
npm install

# Install optional production features
npm install pm2 winston compression cors helmet

# Install dev dependencies
npm install --save-dev nodemon eslint jest prettier

# Install globally for convenience
npm install -g pm2 nodemon
```

## Package Manager Dependencies

### Windows Package Managers
- **Chocolatey**: `choco install nodejs`
- **WinGet**: `winget install OpenJS.NodeJS`
- **Scoop**: `scoop install nodejs`

### macOS Package Managers
- **Homebrew**: `brew install node`
- **MacPorts**: `sudo port install nodejs24`

### Linux Package Managers
- **Ubuntu/Debian**: `sudo apt-get install nodejs npm`
- **CentOS/RHEL**: `sudo yum install nodejs npm`
- **Fedora**: `sudo dnf install nodejs npm`
- **Arch**: `sudo pacman -S nodejs npm`
- **Alpine**: `apk add nodejs npm`

## Docker Dependencies

The project includes Docker support for containerized deployment:

### Build Docker Image
```bash
docker build -t networkbuster:latest .
```

### Run Docker Container
```bash
docker run -p 3000:3000 networkbuster:latest
```

### Docker Compose (Multi-service)
```bash
docker-compose up -d
```

Services included:
- **networkbuster** - Main application
- **postgres** - Database (optional)
- **redis** - Cache (optional)
- **nginx** - Reverse proxy

## Update Dependencies

### Check for outdated packages
```bash
npm outdated
```

### Update all packages
```bash
npm update
```

### Update specific package
```bash
npm install express@latest
```

### Audit and fix vulnerabilities
```bash
npm audit
npm audit fix
npm audit fix --force
```

## Troubleshooting

### Issue: npm packages not installing
**Solution**:
```bash
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

### Issue: Port 3000 already in use
**Solution**:
```bash
PORT=3001 npm start
```

### Issue: Node version mismatch
**Solution**:
```bash
node -v  # Check current version
nvm install 24  # Use Node Version Manager
nvm use 24
```

## Verification Checklist

- [ ] Node.js 24.12.0 installed
- [ ] npm 11.6.2 installed
- [ ] Express 4.22.1 available
- [ ] No security vulnerabilities (`npm audit`)
- [ ] Package-lock.json present
- [ ] node_modules directory created

## Next Steps

1. **Run the application**:
   ```bash
   npm start
   ```

2. **Check the health endpoint**:
   ```bash
   curl http://localhost:3000/health
   ```

3. **View logs**:
   ```bash
   npm run dev
   ```

4. **Deploy to production**:
   - Use Docker for containerization
   - Use PM2 for process management
   - Configure environment variables
   - Set up reverse proxy (nginx)

## Support & Resources

- [Node.js Documentation](https://nodejs.org/docs/)
- [npm Documentation](https://docs.npmjs.com/)
- [Express.js Guide](https://expressjs.com/)

# NetworkBuster Unified Development Environment

## Overview

The unified development environment integrates:
- **Backend:** Express.js server (port 3000)
- **Frontend:** Vite development server (port 5173)
- **API Proxy:** Automatic routing from frontend to backend
- **Hot Module Replacement:** Live updates during development

## Quick Start

### Option 1: Using Node.js (Concurrent)
```bash
node dev-server.js
```

This starts both servers concurrently with automatic coordination.

### Option 2: Using PowerShell (Concurrent)
```powershell
.\dev-server.ps1
```

### Option 3: Manual (Separate Terminals)

Terminal 1 - Backend:
```bash
npm start
```

Terminal 2 - Frontend:
```bash
npm run dev:frontend
```

## Server Details

### Backend (Express.js)
- **URL:** http://localhost:3000
- **Port:** 3000
- **Framework:** Express 5.2.1
- **Runtime:** Node.js 24.12.0

**Routes:**
- `/` → Redirects to `/home`
- `/home` → Home Hub navigation
- `/ai-world` → AI World environment
- `/dashboard` → Dashboard
- `/control-panel` → System control panel
- `/overlay` → Real-time overlay
- `/blog` → Blog content
- `/api/health` → Health check endpoint
- `/api/status` → System status
- `/api/logs` → Application logs
- `/api/components` → Component status

### Frontend (Vite)
- **URL:** http://localhost:5173
- **Port:** 5173
- **Framework:** Vite 5.4.21
- **Features:** HMR, Fast Refresh, Dev Server

**Capabilities:**
- Hot Module Replacement (HMR)
- Automatic proxy to backend
- Live component updates
- Development source maps
- Fast build times

## API Proxy Configuration

The Vite server automatically proxies these routes to the Express backend:
- `/api/*` → Backend API endpoints
- `/home` → Home route
- `/ai-world` → AI World route
- `/dashboard` → Dashboard
- `/control-panel` → Control panel
- `/overlay` → Overlay
- `/blog` → Blog

This allows frontend to call backend APIs without CORS issues during development.

## Development Workflow

1. **Start Development Environment:**
   ```bash
   node dev-server.js
   # OR
   .\dev-server.ps1
   ```

2. **Access Frontend:**
   - Navigate to http://localhost:5173

3. **Frontend requests proxied to:**
   - Backend at http://localhost:3000

4. **Hot Reload:**
   - Save frontend files → Auto-reload in browser
   - No manual refresh needed

5. **API Development:**
   - Modify server.js routes
   - Server restarts automatically
   - Frontend reconnects seamlessly

## File Structure

```
├── server.js              # Express backend
├── vite.config.js         # Vite configuration with proxy
├── dev-server.js          # Node.js unified dev starter
├── dev-server.ps1         # PowerShell unified dev starter
├── dev-config.json        # Development configuration
├── package.json           # npm scripts (dev, start, etc)
├── web-app/               # Frontend source (Vite)
├── dashboard/             # Dashboard source
├── overlay/               # Overlay source
└── blog/                  # Blog content
```

## npm Scripts

```json
{
  "start": "node server.js",
  "dev": "node dev-server.js",
  "dev:backend": "node server.js",
  "dev:frontend": "vite",
  "build": "vite build",
  "preview": "vite preview"
}
```

## Features

### Hot Module Replacement (HMR)
- Frontend changes apply instantly without page reload
- Preserves component state during updates
- Works with React, Vue, and vanilla JS

### API Proxy
- Eliminates CORS issues during development
- Transparent routing to backend
- Configurable route patterns

### Source Maps
- Full debugging support in Chrome DevTools
- Line numbers match source files
- Helps identify production issues

### Development Tools
- Vite plugin ecosystem
- Express middleware stack
- Comprehensive logging

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 3000
netstat -ano | findstr :3000

# Kill process
taskkill /PID <PID> /F
```

### Proxy Not Working
1. Verify backend is running on port 3000
2. Check vite.config.js proxy configuration
3. Restart Vite server
4. Clear browser cache

### Hot Reload Not Working
1. Ensure Vite is running on port 5173
2. Check browser console for errors
3. Verify HMR configuration in vite.config.js
4. Try hard refresh (Ctrl+Shift+R)

### API Errors
1. Check backend console for errors
2. Verify API endpoint exists in server.js
3. Check network tab in DevTools
4. Verify proxy configuration for the route

## Performance Tips

1. **Use Chrome DevTools:**
   - Inspect Network tab for API calls
   - Check Console for errors
   - Use Performance tab for profiling

2. **Keep Servers Running:**
   - Don't stop/restart frequently
   - Saves development time
   - Preserves state

3. **Monitor Memory:**
   - Long sessions may use more memory
   - Restart if performance degrades

## Environment Variables

Create `.env.local` in project root:

```env
VITE_API_URL=http://localhost:3000
VITE_APP_TITLE=NetworkBuster Dev
NODE_ENV=development
```

## Deployment

For production deployment:

1. **Build Frontend:**
   ```bash
   npm run build
   ```

2. **Start Backend:**
   ```bash
   npm start
   ```

3. **Serve Built Frontend:**
   - Copy `dist/` to static folder
   - Express serves from public directory

## Support

For issues or questions:
1. Check application logs at `/api/logs`
2. Review health status at `/api/health`
3. Check system info at `/api/status`
4. View control panel at `/control-panel`

# Network Proxy Configuration Guide

## Overview
NetworkBuster uses a multi-layer proxy setup for optimal network routing and API access:

```
Client (192.168.1.180:5173)
    ↓
Frontend (Vite Dev Server: 5173)
    ↓
Proxy Server (Port 3000 or 8080)
    ↓
Backend Server (Express: 3001)
```

## Architecture

### Layer 1: Frontend (Vite Dev Server)
- **Port**: 5173
- **URL**: http://192.168.1.180:5173
- **Purpose**: React development and UI
- **Proxy Config**: Routes `/api/*` to port 3001

### Layer 2: Network Proxy (Optional)
- **Port**: 3000 or 8080 (configurable)
- **URL**: http://192.168.1.180:3000 or :8080
- **Purpose**: Forward requests to backend, add CORS headers
- **Features**: 
  - HTTP/WebSocket support
  - CORS headers for cross-origin requests
  - Request logging
  - Load balancing ready

### Layer 3: Backend Server
- **Port**: 3001
- **URL**: http://localhost:3001
- **Purpose**: API endpoints, dashboard, secrets management
- **Provides**:
  - `/api/dashboard/*` - Dashboard metrics and charts
  - `/api/secrets/*` - Secrets management endpoints
  - `/api/health` - Health check
  - `/api/status` - System status
  - `/home` - Home hub page
  - `/control-panel` - Operations dashboard

## Quick Start

### Start All Services
```bash
# Terminal 1: Start backend server
npm start

# Terminal 2: Start proxy (port 3000)
npm run proxy:3000

# Terminal 3: Start frontend dev server (if needed)
npm run dev
```

### Alternative: Run Proxy on Port 8080
```bash
npm run proxy:8080
```

### All in One (Requires concurrently)
```bash
npm install concurrently --save-dev
npm run all
```

## Network Access

### From Local Machine
- Frontend: http://localhost:5173
- Proxy: http://localhost:3000
- Backend: http://localhost:3001
- Dashboard: http://localhost:3001/dashboard
- Control Panel: http://localhost:3001/control-panel

### From Network (192.168.1.180)
- Frontend: http://192.168.1.180:5173
- Proxy: http://192.168.1.180:3000
- Backend: http://192.168.1.180:3001
- API: http://192.168.1.180:3000/api/*

## API Endpoints

### Dashboard Endpoints
```
GET  /api/dashboard/metrics    - Real-time metrics (CPU, memory, requests)
GET  /api/dashboard/charts     - Chart data (requests, latency, CPU)
GET  /api/dashboard/services   - Service status
GET  /api/dashboard/activity   - Activity feed
```

### Secrets Management
```
GET    /api/secrets            - List all secrets
GET    /api/secrets/:id        - Get secret by ID
POST   /api/secrets            - Create new secret
PATCH  /api/secrets/:id        - Update secret
DELETE /api/secrets/:id        - Delete secret
GET    /api/secrets/filter/:env - Filter by environment
GET    /api/secrets/validate/expiring - Check expiring secrets
```

### System Information
```
GET  /api/health          - Health status
GET  /api/status          - Detailed system status
GET  /api/logs            - Application logs
POST /api/logs/clear      - Clear logs
GET  /api/components      - Component status
POST /api/toggle/:feature - Toggle features
POST /api/restart         - Request restart
```

## Environment Variables

### Proxy Server
```bash
PROXY_PORT=3000              # Port to listen on (default: 3000)
BACKEND_URL=http://localhost:3001  # Backend URL
FRONTEND_URL=http://192.168.1.180:5173  # Frontend URL for CORS
```

### Backend Server
```bash
PORT=3001                    # Backend port
NODE_ENV=production          # Environment (production/development)
```

### Frontend (Vite)
```bash
VITE_API_URL=http://localhost:3000  # Proxy URL
VITE_API_TIMEOUT=5000        # API timeout in ms
```

## CORS Configuration

The proxy automatically adds CORS headers:
```
Access-Control-Allow-Origin: http://192.168.1.180:5173
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, PATCH, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Allow-Credentials: true
```

## Request Flow Example

### Frontend Request to Dashboard
```
1. Browser: GET http://192.168.1.180:5173/dashboard
2. Vite: Serves React component (Dashboard.jsx)
3. Dashboard renders and makes API call: GET /api/dashboard/metrics
4. Vite Proxy: Forwards to http://localhost:3001/api/dashboard/metrics
5. Express Backend: Returns dashboard metrics JSON
6. Frontend: Displays metrics in UI
```

### Frontend Request via Network Proxy
```
1. Browser: GET http://192.168.1.180:3000/api/secrets
2. Proxy Server: Receives request (port 3000)
3. Proxy Server: Forwards to http://localhost:3001/api/secrets
4. Express Backend: Returns secrets array (masked)
5. Proxy Server: Returns response with CORS headers
6. Browser: Receives and processes secrets list
```

## WebSocket Support

The proxy supports WebSocket upgrades:
```javascript
// Client-side
const ws = new WebSocket('ws://192.168.1.180:3000/ws');
```

The proxy will automatically forward WebSocket connections to the backend.

## Monitoring

### View Proxy Logs
```bash
# Proxy logs show forwarded requests
[2025-12-14T16:24:15.123Z] GET /api/secrets -> http://localhost:3001
[2025-12-14T16:24:16.456Z] POST /api/secrets -> http://localhost:3001
```

### Check Backend Status
```bash
curl http://localhost:3001/api/health
curl http://192.168.1.180:3000/api/health
```

### View System Status
```bash
# Web interface
http://localhost:3001/control-panel
http://192.168.1.180:3001/control-panel
```

## Troubleshooting

### Proxy Not Responding
1. Check if proxy is running: `npm run proxy:3000`
2. Check if backend is running: `npm start`
3. Verify ports: `netstat -ano | findstr :3000` (Windows)

### CORS Errors
1. Ensure frontend URL is in proxy CORS headers
2. Verify proxy environment variables: `$env:FRONTEND_URL`
3. Check browser console for specific errors

### WebSocket Connection Fails
1. Ensure proxy is running (supports upgrade header)
2. Use `ws://` protocol for WebSocket connections
3. Verify firewall allows port 3000/8080

### Backend Not Reachable
1. Verify backend is listening: `netstat -ano | findstr :3001`
2. Check if firewall blocks localhost connections
3. Test directly: `curl http://localhost:3001/api/health`

## Performance Tips

1. **Enable Compression**: Add gzip middleware to proxy
2. **Connection Pooling**: Proxy reuses connections by default
3. **Caching**: Frontend caches API responses (see Dashboard.jsx)
4. **Load Balancing**: Multiple backend instances behind proxy

## Security Notes

⚠️ **Development Only**
- This configuration is for development/testing
- Don't expose ports publicly without authentication
- Implement rate limiting for production
- Use HTTPS in production

## Port Mapping Summary

| Service | Port | Network | Purpose |
|---------|------|---------|---------|
| Vite Frontend | 5173 | 192.168.1.180:5173 | React dev server |
| Network Proxy | 3000/8080 | 192.168.1.180:3000 | Request forwarding |
| Backend API | 3001 | localhost:3001 | Express server |

## Advanced: Multi-Backend Routing

To route different API paths to different backends:

```javascript
// proxy-server.js with routing
const routing = {
  '/api/dashboard': 'http://localhost:3001',
  '/api/secrets': 'http://localhost:3002',
  '/api/analytics': 'http://localhost:3003'
};
```

## Verification Checklist

- [ ] Backend running on 3001: `curl http://localhost:3001/api/health`
- [ ] Proxy running on 3000: `curl http://localhost:3000/api/health`
- [ ] Frontend accessible: `http://192.168.1.180:5173`
- [ ] Dashboard metrics: `curl http://192.168.1.180:3000/api/dashboard/metrics`
- [ ] Secrets API: `curl http://192.168.1.180:3000/api/secrets`
- [ ] All services logged in respective terminals

---

**For more information**, see the deployment and reference guides under `docs/deployment` and `docs/reference`.

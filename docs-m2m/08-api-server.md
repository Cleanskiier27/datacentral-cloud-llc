# Page 8: API & Server Configuration

## 🖥️ Express.js Backend

---

## 📋 Overview

**Framework:** Express.js 4.22.1  
**Runtime:** Node.js 24.x  
**Port:** 3000  
**Environment:** Production  
**Status:** ✅ Running

---

## 🏗️ Server Architecture

**File:** `server.js` (Root)

### Core Dependencies
```json
{
  "express": "4.22.1",
  "node": "24.x"
}
```

### Server Structure
```
server.js
├── Express App
├── Static Middleware
├── Route Handlers
│   ├── /              (Root - web-app)
│   ├── /overlay       (3D overlay)
│   ├── /dashboard     (React dashboard)
│   ├── /blog          (Blog content)
│   ├── /api           (API endpoints)
│   └── /health        (Health checks)
├── Error Handlers
└── Listener (Port 3000)
```

---

## 📡 Route Configuration

### 1. Web App Routes
```javascript
app.use('/web-app', express.static(path.join(__dirname, 'web-app')));
app.use('/', express.static(path.join(__dirname, 'web-app')));

Methods:
  GET  /              → index.html
  GET  /about         → about.html
  GET  /projects      → projects.html
  GET  /technology    → technology.html
  GET  /documentation → documentation.html
  GET  /contact       → contact.html
  GET  /flash-commands → flash-commands.html
```

### 2. Overlay Routes
```javascript
app.use('/overlay', express.static(path.join(__dirname, 'challengerepo/real-time-overlay/src')));

Methods:
  GET  /overlay              → Main overlay app
  GET  /overlay/index.html   → HTML entry point
  GET  /overlay/*.jsx        → React components
  GET  /overlay/index.css    → Styling
```

### 3. Dashboard Routes
```javascript
app.use('/dashboard', express.static(path.join(__dirname, 'dashboard/dist')));

Methods:
  GET  /dashboard     → React build
  GET  /dashboard/*   → SPA routing
```

### 4. Blog Routes
```javascript
app.use('/blog', express.static(path.join(__dirname, 'blog')));

Methods:
  GET  /blog              → Blog index
  GET  /blog/posts        → All posts
  GET  /blog/post/:id     → Single post
```

### 5. API Routes
```javascript
app.use('/api', require('./api/routes'));

Methods:
  GET  /api/health      → Health status
  GET  /api/status      → Server status
  GET  /api/config      → Configuration info
  POST /api/data        → Data submission
```

### 6. Health Check Route
```javascript
app.get('/health', (req, res) => {
  res.status(200).json({ 
    status: 'healthy',
    uptime: process.uptime(),
    timestamp: new Date()
  });
});
```

---

## 🔧 Middleware Configuration

### Compression
```javascript
const compression = require('compression');
app.use(compression());
```

### CORS (If Needed)
```javascript
const cors = require('cors');
app.use(cors());
```

### Body Parser
```javascript
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
```

### Request Logging
```javascript
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
  next();
});
```

---

## 🚀 Server Startup

### Development Mode
```bash
npm start
# Runs: node server.js
# Port: 3000
# Auto-reload: NO
```

### Watch Mode
```bash
npm run dev
# Runs: nodemon server.js
# Port: 3000
# Auto-reload: YES
```

### Production Mode
```bash
NODE_ENV=production npm start
# Port: 3000
# Logging: Minimal
# Performance: Optimized
```

---

## 📊 Server Performance

### Request Handling
```
Throughput: ~1000 req/sec (single instance)
Response Time: <200ms (p95)
Memory Usage: ~150MB
CPU Usage: <5% (idle)
```

### Scaling
```
Single Instance: 0.5 CPU, 1GB RAM (Azure)
Max Instances: 5 (auto-scaling)
Load Balancing: Round-robin
```

---

## 🔍 Health Checks

### Health Check Endpoint
```
GET /health
Response: 200 OK
Body: {
  "status": "healthy",
  "uptime": 12345,
  "timestamp": "2025-12-14T12:00:00Z"
}
```

### Monitoring Health
```bash
# Test locally
curl http://localhost:3000/health

# Test in container
curl http://container:3000/health

# Continuous monitoring
watch -n 5 curl -s http://localhost:3000/health
```

---

## 📝 Logging Configuration

### Console Logging
```javascript
console.log('Info');      // Standard info
console.warn('Warning');  // Warning messages
console.error('Error');   // Error messages
```

### Log Format
```
[HH:MM:SS] METHOD /path - Status Code
[12:34:56] GET /health - 200
[12:34:57] POST /api/data - 201
```

### Structured Logging (Recommended)
```javascript
const logger = require('winston');
logger.info('Server started', { port: 3000 });
logger.error('Error occurred', { error: err });
```

---

## 🔐 Security Configuration

### Security Headers
```javascript
// HSTS
app.use((req, res, next) => {
  res.setHeader('Strict-Transport-Security', 'max-age=31536000');
  next();
});

// X-Frame-Options
app.use((req, res, next) => {
  res.setHeader('X-Frame-Options', 'DENY');
  next();
});

// X-Content-Type-Options
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  next();
});
```

### HTTPS Configuration
```javascript
const https = require('https');
const fs = require('fs');
const options = {
  key: fs.readFileSync('key.pem'),
  cert: fs.readFileSync('cert.pem')
};
https.createServer(options, app).listen(3000);
```

---

## 🌍 Environment Variables

### Required
```bash
NODE_ENV=production
PORT=3000
```

### Optional
```bash
LOG_LEVEL=info
DEBUG=false
CACHE_TTL=3600
```

### Setting Variables
```bash
# Bash/Shell
export NODE_ENV=production
npm start

# PowerShell
$env:NODE_ENV="production"
npm start

# .env file
NODE_ENV=production
PORT=3000
```

---

## 📈 Performance Optimization

### Caching
```javascript
app.use((req, res, next) => {
  res.set('Cache-Control', 'public, max-age=3600');
  next();
});
```

### Gzip Compression
```javascript
const compression = require('compression');
app.use(compression());
```

### Static Asset Optimization
```javascript
app.use(express.static('public', {
  maxAge: '1d',
  etag: false
}));
```

---

## 🛠️ API Endpoints

### Server Status
```
GET /api/status
Response: {
  "version": "1.0.0",
  "uptime": 12345,
  "environment": "production",
  "memory": { "used": 150, "total": 512 }
}
```

### Configuration Info
```
GET /api/config
Response: {
  "node_version": "24.x",
  "npm_version": "10.x",
  "services": ["web-app", "overlay", "dashboard", "blog", "api"]
}
```

### Error Handling
```javascript
app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).json({
    error: 'Internal Server Error',
    message: err.message
  });
});
```

---

## 🚨 Error Handling

### 404 Not Found
```javascript
app.use((req, res) => {
  res.status(404).json({ error: 'Not Found' });
});
```

### 500 Server Error
```javascript
app.use((err, req, res, next) => {
  res.status(500).json({ error: 'Server Error' });
});
```

---

## 📋 Deployment Configuration

### Vercel Deployment
```json
{
  "version": 2,
  "buildCommand": "npm run build:all || true",
  "devCommand": "npm start",
  "env": { "NODE_ENV": "production" }
}
```

### Azure Deployment
```dockerfile
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=10s \
  CMD node -e "require('http').get('http://localhost:3000/health')"
CMD ["node", "server.js"]
```

---

## 📊 Server Monitoring

### Metrics to Monitor
- Request rate (req/sec)
- Error rate (errors/sec)
- Response time (ms)
- Memory usage (MB)
- CPU usage (%)
- Uptime (hours)

### Health Check Frequency
```
Azure: Every 30 seconds
Vercel: Every 60 seconds
Custom: Configurable
```

---

**[← Back to Index](./00-index.md) | [Next: Page 9 →](./09-frontend-apps.md)**

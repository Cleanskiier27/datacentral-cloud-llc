/**
 * Nexus Connector
 * Node.js API gateway that fronts the Python Nexus Engine and aggregates
 * health from sibling NetworkBuster services. Keeps the fast, I/O-bound
 * routing layer in Node while the Python engine owns business logic.
 */
const express = require('express');
const axios = require('axios');

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 8085;
const SECURITY_PIN = process.env.SECURITY_PIN || 'drew2';
const ENGINE_URL = process.env.NEXUS_ENGINE_URL || 'http://nexus-engine:8086';
const TIMEOUT_MS = Number(process.env.HEALTH_CHECK_TIMEOUT_MS || 2000);

// Sibling services on the nb-network, name doubles as DNS hostname (docker-compose)
const SIBLING_SERVICES = {
  'services-manager': 8080,
  'robot-recycling': 5000,
  'sudo-manager': 8081,
  'status-dashboard': 8082,
  'token-manager': 8083,
  'license-manager': 8084,
  'nexus-engine': 8086,
  'interstellar-wealth': 8087,
};

function requirePin(req, res, next) {
  const supplied = req.header('X-Security-Pin') || req.query.pin;
  if (supplied !== SECURITY_PIN) {
    return res.status(401).json({ error: 'unauthorized' });
  }
  next();
}

async function checkService(name, port) {
  const start = Date.now();
  try {
    const resp = await axios.get(`http://${name}:${port}/health`, { timeout: TIMEOUT_MS });
    return { name, up: resp.status === 200, latency_ms: Date.now() - start };
  } catch {
    return { name, up: false, latency_ms: null };
  }
}

app.get('/health', (_req, res) => {
  res.json({ status: 'ok', service: 'nexus-connector' });
});

app.get('/api/nexus/status', async (_req, res) => {
  const results = await Promise.all(
    Object.entries(SIBLING_SERVICES).map(([name, port]) => checkService(name, port))
  );
  res.json(results);
});

// Proxies processing requests to the Python engine, adding the shared PIN header
app.post('/api/nexus/process', requirePin, async (req, res) => {
  try {
    const resp = await axios.post(`${ENGINE_URL}/api/process`, req.body, {
      headers: { 'X-Security-Pin': SECURITY_PIN },
      timeout: TIMEOUT_MS * 5,
    });
    res.status(resp.status).json(resp.data);
  } catch (err) {
    const status = err.response ? err.response.status : 502;
    res.status(status).json({ error: 'nexus-engine unreachable', detail: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`🔗 Nexus Connector listening on port ${PORT}, engine at ${ENGINE_URL}`);
});

"""
Services Manager
Polls the /health endpoint of every sibling NetworkBuster service on the
nb-network and reports aggregate status.
"""
import os
import time

import requests
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# Service name doubles as its DNS hostname on the nb-network (docker-compose default)
SERVICES = {
    'robot-recycling': 5000,
    'sudo-manager': 8081,
    'status-dashboard': 8082,
    'token-manager': 8083,
    'license-manager': 8084,
}
TIMEOUT = float(os.environ.get('HEALTH_CHECK_TIMEOUT', 2))

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>NetworkBuster Services Manager</title>
  <meta http-equiv="refresh" content="10">
  <style>
    body { font-family: 'Segoe UI', sans-serif; background:#0f172a; color:#e2e8f0; padding:30px; }
    h1 { color:#38bdf8; }
    table { width:100%; border-collapse: collapse; margin-top:20px; }
    th, td { padding:12px; text-align:left; border-bottom:1px solid #334155; }
    th { color:#94a3b8; text-transform:uppercase; font-size:0.8em; }
    .up { color:#4ade80; font-weight:bold; }
    .down { color:#f87171; font-weight:bold; }
  </style>
</head>
<body>
  <h1>🩺 NetworkBuster Services Manager</h1>
  <table>
    <thead><tr><th>Service</th><th>Status</th><th>Latency (ms)</th></tr></thead>
    <tbody>
    {% for s in results %}
      <tr>
        <td>{{ s.name }}</td>
        <td class="{{ 'up' if s.up else 'down' }}">{{ 'UP' if s.up else 'DOWN' }}</td>
        <td>{{ s.latency_ms }}</td>
      </tr>
    {% endfor %}
    </tbody>
  </table>
</body>
</html>
"""


def check_service(name, port):
    url = f"http://{name}:{port}/health"
    start = time.time()
    try:
        resp = requests.get(url, timeout=TIMEOUT)
        latency_ms = round((time.time() - start) * 1000, 1)
        return {'name': name, 'up': resp.status_code == 200, 'latency_ms': latency_ms}
    except requests.RequestException:
        return {'name': name, 'up': False, 'latency_ms': None}


def check_all():
    return [check_service(name, port) for name, port in SERVICES.items()]


@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'service': 'services-manager'})


@app.route('/api/status')
def api_status():
    return jsonify(check_all())


@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD_HTML, results=check_all())


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"🩺 Starting Services Manager on port {port}...")
    app.run(host='0.0.0.0', port=port)

"""
Status Dashboard Service
Live system metrics (CPU/memory/disk) and, when the Docker socket is
mounted, a summary of sibling NetworkBuster containers.
"""
import os
import time

import psutil
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)
REFRESH_INTERVAL = int(os.environ.get('REFRESH_INTERVAL', 5))
START_TIME = time.time()

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>NetworkBuster Status Dashboard</title>
  <meta http-equiv="refresh" content="{{ refresh }}">
  <style>
    body { font-family: 'Segoe UI', sans-serif; background:#111827; color:#e5e7eb; padding:30px; }
    h1 { color:#60a5fa; }
    .grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(180px,1fr)); gap:20px; margin-top:20px; }
    .card { background:#1f2937; border-radius:12px; padding:20px; text-align:center; }
    .value { font-size:2.2em; font-weight:bold; color:#34d399; }
    .label { color:#9ca3af; text-transform:uppercase; font-size:0.85em; }
  </style>
</head>
<body>
  <h1>📊 NetworkBuster Status Dashboard</h1>
  <div class="grid">
    <div class="card"><div class="value">{{ cpu }}%</div><div class="label">CPU</div></div>
    <div class="card"><div class="value">{{ mem }}%</div><div class="label">Memory</div></div>
    <div class="card"><div class="value">{{ disk }}%</div><div class="label">Disk</div></div>
    <div class="card"><div class="value">{{ uptime }}</div><div class="label">Uptime</div></div>
  </div>
</body>
</html>
"""


def get_metrics():
    uptime_seconds = int(time.time() - START_TIME)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return {
        'cpu': psutil.cpu_percent(interval=0.2),
        'mem': psutil.virtual_memory().percent,
        'disk': psutil.disk_usage('/').percent,
        'uptime': f"{hours:02d}:{minutes:02d}:{seconds:02d}",
    }


def get_containers():
    """Best-effort container summary; requires /var/run/docker.sock mounted"""
    try:
        import docker
        client = docker.from_env()
        return [
            {'name': c.name, 'status': c.status, 'image': c.image.tags[0] if c.image.tags else c.image.short_id}
            for c in client.containers.list(all=True)
        ]
    except Exception as e:
        return {'error': f'docker socket unavailable: {e}'}


@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'service': 'status-dashboard'})


@app.route('/api/stats')
def stats():
    return jsonify(get_metrics())


@app.route('/api/containers')
def containers():
    return jsonify(get_containers())


@app.route('/')
def dashboard():
    metrics = get_metrics()
    return render_template_string(DASHBOARD_HTML, refresh=REFRESH_INTERVAL, **metrics)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8082))
    print(f"📊 Starting Status Dashboard on port {port}...")
    app.run(host='0.0.0.0', port=port)

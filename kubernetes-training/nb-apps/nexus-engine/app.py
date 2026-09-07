"""
Nexus Engine
Python backend that performs the actual processing work requested by the
Node.js Nexus Connector gateway. Kept separate from the connector so the
gateway (Node) and the business logic (Python) can scale independently.
"""
import hashlib
import os
import time
from datetime import datetime, timezone

from flask import Flask, jsonify, request

app = Flask(__name__)

SECURITY_PIN = os.environ.get('SECURITY_PIN', 'drew2')
START_TIME = time.time()

# In-memory ledger of jobs processed since startup (non-persistent by design)
_job_counter = 0


def _authorized(req) -> bool:
    supplied = req.headers.get('X-Security-Pin') or req.args.get('pin')
    return supplied == SECURITY_PIN


@app.route('/health')
def health():
    return jsonify({
        'status': 'ok',
        'service': 'nexus-engine',
        'uptime_s': round(time.time() - START_TIME, 1),
    })


@app.route('/api/process', methods=['POST'])
def process():
    global _job_counter
    if not _authorized(request):
        return jsonify({'error': 'unauthorized'}), 401

    payload = request.get_json(silent=True) or {}
    task = payload.get('task', 'noop')

    _job_counter += 1
    digest = hashlib.sha256(f"{task}-{_job_counter}-{time.time()}".encode()).hexdigest()[:16]

    return jsonify({
        'job_id': _job_counter,
        'task': task,
        'result_digest': digest,
        'processed_at': datetime.now(timezone.utc).isoformat(),
    })


@app.route('/api/stats')
def stats():
    return jsonify({'jobs_processed': _job_counter, 'uptime_s': round(time.time() - START_TIME, 1)})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8086))
    print(f"🧠 Starting Nexus Engine on port {port}...")
    app.run(host='0.0.0.0', port=port)

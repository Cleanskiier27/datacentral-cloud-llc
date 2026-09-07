"""
Interstellar Wealth
Stub service scaffolded in the same shape as the other nb-apps. Holds
placeholder in-memory balance/transaction data only -- no real payment
processing, trading, or external market integration is implemented here.
"""
import os
import time
from datetime import datetime, timezone

from flask import Flask, jsonify, request

app = Flask(__name__)

SECURITY_PIN = os.environ.get('SECURITY_PIN', 'drew2')
START_TIME = time.time()

# Mock in-memory ledger, reset on every restart -- placeholder data only
_balance = {'currency': 'USD', 'amount': 0.0}
_transactions = []


def _authorized(req) -> bool:
    supplied = req.headers.get('X-Security-Pin') or req.args.get('pin')
    return supplied == SECURITY_PIN


@app.route('/health')
def health():
    return jsonify({
        'status': 'ok',
        'service': 'interstellar-wealth',
        'uptime_s': round(time.time() - START_TIME, 1),
    })


@app.route('/api/balance')
def get_balance():
    return jsonify(_balance)


@app.route('/api/transactions', methods=['GET', 'POST'])
def transactions():
    if request.method == 'GET':
        return jsonify(_transactions)

    if not _authorized(request):
        return jsonify({'error': 'unauthorized'}), 401

    payload = request.get_json(silent=True) or {}
    amount = float(payload.get('amount', 0))
    entry = {
        'id': len(_transactions) + 1,
        'amount': amount,
        'note': payload.get('note', ''),
        'recorded_at': datetime.now(timezone.utc).isoformat(),
    }
    _transactions.append(entry)
    _balance['amount'] = round(_balance['amount'] + amount, 2)
    return jsonify(entry), 201


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8087))
    print(f"💫 Starting Interstellar Wealth on port {port}...")
    app.run(host='0.0.0.0', port=port)

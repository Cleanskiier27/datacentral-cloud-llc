"""
Token Manager Service
REST API wrapper around TokenManager for personal access tokens.
"""
import os
from functools import wraps

from flask import Flask, jsonify, request

from token_manager import TokenManager

app = Flask(__name__)
SECURITY_PIN = os.environ.get('SECURITY_PIN', 'drew2')
DATA_DIR = os.environ.get('DATA_DIR', '/app/data')
os.makedirs(DATA_DIR, exist_ok=True)
manager = TokenManager(storage_path=os.path.join(DATA_DIR, 'tokens.json'))


def require_pin(fn):
    """Guard mutating endpoints with the shared SECURITY_PIN header"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if request.headers.get('X-Security-Pin') != SECURITY_PIN:
            return jsonify({'error': 'unauthorized'}), 401
        return fn(*args, **kwargs)
    return wrapper


@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'service': 'token-manager'})


@app.route('/api/tokens', methods=['GET'])
def list_tokens():
    return jsonify(manager.list_tokens())


@app.route('/api/tokens', methods=['POST'])
@require_pin
def create_token():
    body = request.get_json(force=True, silent=True) or {}
    name = body.get('name')
    if not name:
        return jsonify({'error': 'name is required'}), 400
    try:
        token = manager.generate_token(
            name=name,
            scopes=body.get('scopes'),
            expiry_days=body.get('expiry_days'),
        )
    except ValueError as e:
        return jsonify({'error': str(e)}), 409
    # Token value is only ever returned here, at creation time
    return jsonify({'token': token, 'name': name}), 201


@app.route('/api/tokens/validate', methods=['POST'])
def validate_token():
    body = request.get_json(force=True, silent=True) or {}
    token = body.get('token', '')
    valid = manager.validate_token(token)
    scopes = manager.get_token_scopes(token) if valid else None
    return jsonify({'valid': valid, 'scopes': scopes})


@app.route('/api/tokens/<name>', methods=['DELETE'])
@require_pin
def revoke_token(name):
    if not manager.revoke_token(name):
        return jsonify({'error': 'not found'}), 404
    return jsonify({'revoked': name})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8083))
    print(f"🔑 Starting Token Manager on port {port}...")
    app.run(host='0.0.0.0', port=port)

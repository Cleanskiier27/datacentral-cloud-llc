"""
Sudo Manager Service
Grant/revoke API for NetworkBuster admin tooling, with a file-backed audit log.
"""
import json
import os
from datetime import datetime
from functools import wraps

from flask import Flask, jsonify, request

app = Flask(__name__)
SECURITY_PIN = os.environ.get('SECURITY_PIN', 'drew2')
ADMIN_USER = os.environ.get('ADMIN_USER', 'drew')
LOG_DIR = os.environ.get('LOG_DIR', '/app/logs')
os.makedirs(LOG_DIR, exist_ok=True)
PERMISSIONS_FILE = os.path.join(LOG_DIR, 'permissions.json')
AUDIT_LOG = os.path.join(LOG_DIR, 'sudo.log')


def load_permissions():
    if os.path.exists(PERMISSIONS_FILE):
        with open(PERMISSIONS_FILE) as f:
            return json.load(f)
    return {}


def save_permissions(perms):
    with open(PERMISSIONS_FILE, 'w') as f:
        json.dump(perms, f, indent=2)


def audit(action, user, permission):
    with open(AUDIT_LOG, 'a') as f:
        f.write(f"{datetime.now().isoformat()} {action} user={user} permission={permission}\n")


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
    return jsonify({'status': 'ok', 'service': 'sudo-manager'})


@app.route('/api/permissions', methods=['GET'])
def list_permissions():
    return jsonify(load_permissions())


@app.route('/api/permissions/grant', methods=['POST'])
@require_pin
def grant():
    body = request.get_json(force=True, silent=True) or {}
    user = body.get('user')
    permission = body.get('permission')
    if not user or not permission:
        return jsonify({'error': 'user and permission are required'}), 400
    perms = load_permissions()
    perms.setdefault(user, [])
    if permission not in perms[user]:
        perms[user].append(permission)
    save_permissions(perms)
    audit('grant', user, permission)
    return jsonify({'user': user, 'permissions': perms[user]})


@app.route('/api/permissions/revoke', methods=['POST'])
@require_pin
def revoke():
    body = request.get_json(force=True, silent=True) or {}
    user = body.get('user')
    permission = body.get('permission')
    perms = load_permissions()
    if user in perms and permission in perms[user]:
        perms[user].remove(permission)
        save_permissions(perms)
        audit('revoke', user, permission)
        return jsonify({'user': user, 'permissions': perms[user]})
    return jsonify({'error': 'not found'}), 404


@app.route('/api/whoami')
def whoami():
    return jsonify({'admin_user': ADMIN_USER})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8081))
    print(f"🛡️  Starting Sudo Manager on port {port}...")
    app.run(host='0.0.0.0', port=port)

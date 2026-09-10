from flask import Flask, render_template, jsonify, request, send_file
import subprocess
import os
import sys
from pathlib import Path
from markupsafe import escape

app = Flask(__name__)

# Flash Commands Definition
FLASH_COMMANDS = {
    "build": {
        "name": "Build Distro",
        "command": [sys.executable, "scripts/build_distro.py"],
        "description": "Packages the NetworkBuster application into a distribution."
    },
    "train": {
        "name": "Run AI Training",
        "command": ["mvn", "exec:exec@run-neural-network"],
        "description": "Executes the neural network training pipeline."
    },
    "status": {
        "name": "Check Status",
        "command": [sys.executable, "token_cli.py", "list"],
        "description": "Lists active tokens and system health."
    },
    "web3": {
        "name": "Verify Web3",
        "command": [sys.executable, "scripts/web3_verifier.py", "--demo"],
        "description": "Verifies Ethereum connection and demonstrates ownership proof."
    },
    "moonbase_build": {
        "name": "Build MOONBASE.BOT",
        "command": [sys.executable, "scripts/build_moonbase_bot.py"],
        "description": "Packages MOONBASE.BOT / BUSTER.BOT for open-world Minecraft and Discord."
    },
    "buster_status": {
        "name": "BUSTER.BOT Status",
        "command": [sys.executable, "moonbase_bot.py", "--command", "status"],
        "description": "Checks Minecraft server online telemetry and BUSTER.BOT status."
    }
}

@app.route('/')
def index():
    return render_template('index.html', commands=FLASH_COMMANDS)


@app.route('/ascii-led')
def ascii_led_preview():
    """Render the ASCII LED screenplay in a browser-friendly preformatted view."""
    ascii_file = Path(__file__).parent.parent / "assets" / "matrix_screenplay.txt"
    if not ascii_file.exists():
        return "ASCII source file not found.", 404

    content = ascii_file.read_text(encoding="utf-8", errors="replace")
    escaped_content = escape(content)
    return f"""
<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
    <title>ASCII LED Preview</title>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            background: #020b06;
            color: #4dff9a;
            font-family: Consolas, 'Courier New', monospace;
        }}
        pre {{
            white-space: pre;
            overflow: auto;
            border: 1px solid #1f6b45;
            padding: 16px;
            background: #001f12;
        }}
    </style>
</head>
<body>
    <pre>{escaped_content}</pre>
</body>
</html>
"""

@app.route('/execute/<cmd_id>', methods=['POST'])
def execute(cmd_id):
    if cmd_id not in FLASH_COMMANDS:
        return jsonify({"status": "error", "message": "Command not found"}), 404
    
    cmd_info = FLASH_COMMANDS[cmd_id]
    try:
        # Run command and capture output
        result = subprocess.run(
            cmd_info["command"],
            capture_output=True,
            text=True,
            cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        )
        return jsonify({
            "status": "success" if result.returncode == 0 else "error",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/download', methods=['GET'])
def download_distro():
    """Download the latest NetworkBuster distribution."""
    dist_dir = Path(__file__).parent.parent / "dist"
    
    if not dist_dir.exists():
        return jsonify({"status": "error", "message": "Distribution not found. Run build first."}), 404
    
    # Find the latest zip file
    zip_files = list(dist_dir.glob("*.zip"))
    if not zip_files:
        return jsonify({"status": "error", "message": "No distribution archive found."}), 404
    
    latest_file = max(zip_files, key=lambda p: p.stat().st_mtime)
    return send_file(latest_file, as_attachment=True, download_name=latest_file.name)

@app.route('/distro-info', methods=['GET'])
def distro_info():
    """Get info about available distributions."""
    dist_dir = Path(__file__).parent.parent / "dist"
    
    if not dist_dir.exists():
        return jsonify({"status": "no_distro", "message": "No distributions built yet."})
    
    zip_files = list(dist_dir.glob("*.zip"))
    distros = []
    for f in zip_files:
        distros.append({
            "name": f.name,
            "size_mb": round(f.stat().st_size / (1024 * 1024), 2),
            "created": f.stat().st_mtime
        })
    
    return jsonify({"status": "success", "distros": sorted(distros, key=lambda x: x['created'], reverse=True)})

# --- Open World Space Economy Marketplace Routes ---
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from moonbase_bot.marketplace import MarketplaceManager
marketplace_mgr = MarketplaceManager()

@app.route('/api/marketplace/items', methods=['GET'])
def api_marketplace_items():
    category = request.args.get('category')
    items = marketplace_mgr.get_items(category)
    return jsonify({"status": "success", "count": len(items), "items": items})

@app.route('/api/marketplace/balance/<player_name>', methods=['GET'])
def api_marketplace_balance(player_name):
    balance = marketplace_mgr.get_player_balance(player_name)
    return jsonify({"status": "success", "player": player_name, "balance": balance})

@app.route('/api/marketplace/inventory/<player_name>', methods=['GET'])
def api_marketplace_inventory(player_name):
    inventory = marketplace_mgr.get_player_inventory(player_name)
    return jsonify({"status": "success", "player": player_name, "count": len(inventory), "inventory": inventory})

@app.route('/api/marketplace/buy', methods=['POST'])
def api_marketplace_buy():
    data = request.get_json() or {}
    player = data.get("player") or request.form.get("player")
    item_id = data.get("item_id") or request.form.get("item_id")
    token_str = data.get("token") or request.form.get("token")
    quantity = int(data.get("quantity") or request.form.get("quantity") or 1)

    if not player or not item_id:
        return jsonify({"status": "error", "message": "Missing 'player' or 'item_id' in request."}), 400

    result = marketplace_mgr.purchase_item(
        player_name=player,
        item_id=item_id,
        token_str=token_str,
        quantity=quantity,
    )
    if result.get("success"):
        return jsonify({"status": "success", "transaction": result})
    else:
        return jsonify({"status": "error", "message": result.get("error")}), 400

@app.route('/marketplace', methods=['GET'])
def marketplace_view():
    items = marketplace_mgr.get_items()
    categories = sorted(list(set(i['category'] for i in items)))
    return render_template('marketplace.html', items=items, categories=categories)

if __name__ == "__main__":
    # Unified Certificate Configuration
    cert_path = os.path.join(os.path.dirname(__file__), "..", "certs", "unified_certificate.pem")
    key_path = os.path.join(os.path.dirname(__file__), "..", "certs", "unified_key.pem")

    port = int(os.environ.get('FLASK_PORT', '5000'))
    debug = False

    if os.path.exists(cert_path) and os.path.exists(key_path):
        print("Starting WebApp with Unified Certificate")
        app.run(host='0.0.0.0', port=port, debug=debug, ssl_context=(cert_path, key_path))
    else:
        print("Unified Certificate not found. Starting in HTTP mode.")
        app.run(host='0.0.0.0', port=port, debug=debug)
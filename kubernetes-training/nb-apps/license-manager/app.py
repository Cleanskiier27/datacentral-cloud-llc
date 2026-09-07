"""
License Manager Service
REST API wrapper around PersonalLicenseManager.
"""
import os

from flask import Flask, jsonify

from personal_license import PersonalLicenseManager

app = Flask(__name__)
LICENSE_TYPE = os.environ.get('LICENSE_TYPE', PersonalLicenseManager.LICENSE_TYPE)
OWNER = os.environ.get('OWNER', 'NetworkBuster')


@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'service': 'license-manager'})


@app.route('/api/license')
def license_info():
    return jsonify({
        'licensed_to': PersonalLicenseManager.AUTHORIZED_USER,
        'license_type': LICENSE_TYPE,
        'owner': OWNER,
        'machine': PersonalLicenseManager.AUTHORIZED_MACHINE,
        'machine_id': PersonalLicenseManager.generate_machine_id(),
    })


@app.route('/api/license/verify', methods=['POST'])
def verify():
    authorized = PersonalLicenseManager.verify_authorization()
    return jsonify({'authorized': authorized})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8084))
    print(f"🔒 Starting License Manager on port {port}...")
    app.run(host='0.0.0.0', port=port)

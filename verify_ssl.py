import ssl
import socket
import os
from urllib.parse import urlparse

def verify_local_ssl(url="https://localhost:5000"):
    """Verifies that the local Flask app is serving over HTTPS with the correct certificate."""
    print(f"🔍 Verifying SSL for {url}...")
    
    # Path to the generated certificate (relative to repo root)
    cert_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "certs", "unified_certificate.pem")
    
    if not os.path.exists(cert_path):
        print(f"❌ Certificate file not found at: {cert_path}")
        print("   Please run setup_linux.sh first to generate the certificate.")
        return

    try:
        # Create a context that trusts our specific self-signed cert
        context = ssl.create_default_context(cafile=cert_path)
        # We are testing localhost, so we ensure the hostname matches the CN in the cert
        
        parsed_url = urlparse(url)
        port = parsed_url.port or 443
        hostname = parsed_url.hostname

        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                print("\n✅ SSL Handshake Successful!")
                print("-" * 40)
                # Extract and print readable subject info
                subject = dict(x[0] for x in cert['subject'])
                print(f"Subject: {subject}")
                print(f"Issuer:  {dict(x[0] for x in cert['issuer'])}")
                print("-" * 40)
                print("The Flask app is correctly serving HTTPS using the unified certificate.")

    except Exception as e:
        print(f"\n❌ Verification Failed: {e}")
        print("Ensure the Flask app is running (python webapp/app.py) and the certificate is generated.")

if __name__ == "__main__":
    verify_local_ssl()
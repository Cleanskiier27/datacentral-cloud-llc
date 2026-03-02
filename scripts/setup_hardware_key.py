#!/usr/bin/env python3
"""
NetworkBuster - Hardware Key Initializer
This script detects and initializes FIDO2-compliant hardware keys (like YubiKey)
for use with the system.
"""

import sys
from fido2.hid import CtapHidDevice
from fido2.client import Fido2Client, ClientError

def initialize_hardware_key():
    """
    Initializes and checks for a FIDO2 hardware key.
    """
    print("\n" + "="*60)
    print("🔑 Hardware Key Interface Setup")
    print("="*60)

    try:
        # Find all connected FIDO2 devices
        devices = list(CtapHidDevice.list_devices())
        if not devices:
            print("\n❌ No FIDO2 hardware key found.")
            print("   Please connect your hardware key and re-run the script.")
            sys.exit(1)

        print(f"\n✅ Found {len(devices)} FIDO2 device(s).")

        for i, dev in enumerate(devices):
            print(f"\n--- Initializing Device #{i+1} ---")
            print(f"  Path: {dev.descriptor.path}")

            client = Fido2Client(dev, "https://networkbuster.local")

            # Print device info
            if client.info:
                print("  Device Info:")
                print(f"    Versions: {client.info.versions}")
                print(f"    AAGUID: {client.info.aaguid.hex()}")

                if client.info.options:
                    print("    Options:")
                    for k, v in client.info.options.items():
                        print(f"      - {k}: {v}")

                # Check PIN status
                if client.info.options.get('clientPin'):
                    print("\n    PIN Status: PIN is already set. No action needed.")
                else:
                    print("\n    PIN Status: PIN is NOT set. It is highly recommended to set a PIN for security.")

    except ClientError as e:
        print(f"\n❌ A FIDO2 client error occurred: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        sys.exit(1)

    print("\n" + "="*60)
    print("✅ Hardware key interface check complete.")
    print("="*60 + "\n")

if __name__ == "__main__":
    initialize_hardware_key()
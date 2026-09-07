"""
NetworkBuster Authorization System
Personal Use Only - Licensed to Cadillac.gas@outlook.com
"""
import hashlib
import os
from datetime import datetime

class PersonalLicenseManager:
    """Manages personal use authorization"""
    
    AUTHORIZED_USER = "cadillac.gas@outlook.com"
    AUTHORIZED_MACHINE = os.environ.get('COMPUTERNAME', 'UNKNOWN')
    LICENSE_TYPE = "PERSONAL_USE_ONLY"
    
    @staticmethod
    def generate_machine_id():
        """Generate unique machine identifier"""
        import platform
        machine_info = f"{platform.node()}-{platform.machine()}-{platform.processor()}"
        return hashlib.sha256(machine_info.encode()).hexdigest()[:16]
    
    @staticmethod
    def verify_authorization():
        """Verify this is authorized for personal use"""
        print("=" * 60)
        print("🔒 NetworkBuster Authorization Check")
        print("=" * 60)
        print(f"Licensed To: {PersonalLicenseManager.AUTHORIZED_USER}")
        print(f"License Type: {PersonalLicenseManager.LICENSE_TYPE}")
        print(f"Machine: {PersonalLicenseManager.AUTHORIZED_MACHINE}")
        print(f"Machine ID: {PersonalLicenseManager.generate_machine_id()}")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        print("✅ AUTHORIZED - Personal Use Only")
        print("⚠️  This software is licensed for personal use only")
        print("⚠️  Unauthorized distribution or commercial use is prohibited")
        print("=" * 60)
        return True
    
    @staticmethod
    def create_license_file():
        """Create license file"""
        license_content = f"""
NetworkBuster Personal License
================================

Licensed To: {PersonalLicenseManager.AUTHORIZED_USER}
License Type: {PersonalLicenseManager.LICENSE_TYPE}
Machine ID: {PersonalLicenseManager.generate_machine_id()}
Issue Date: {datetime.now().strftime('%Y-%m-%d')}

TERMS OF USE:
- This software is licensed for PERSONAL USE ONLY
- No commercial use permitted
- No redistribution without authorization
- No modification of license terms
- Single user license only

© 2026 NetworkBuster. All rights reserved.
"""
        
        with open('LICENSE_PERSONAL.txt', 'w') as f:
            f.write(license_content)
        
        print("✅ Personal license file created: LICENSE_PERSONAL.txt")

if __name__ == "__main__":
    manager = PersonalLicenseManager()
    manager.verify_authorization()
    manager.create_license_file()

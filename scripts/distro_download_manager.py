#!/usr/bin/env python3
"""
NetworkBuster Distribution Download Manager
Handles downloading and managing NetworkBuster distributions after git is configured
"""

import json
import os
import sys
import requests
import shutil
from pathlib import Path
from datetime import datetime

# Import shared banner
try:
    import banner
except ImportError:
    from scripts import banner


class DistroDownloadManager:
    def __init__(self, config_path=None):
        """Initialize the download manager."""
        self.config_path = config_path or self._get_default_config_path()
        self.config = self._load_config()
        self.dist_dir = Path(self.config.get("distribution_path", "./dist")).expanduser()
        
    def print_banner(self):
        """Print NetworkBuster ASCII Art."""
        banner.print_ascii_art()
        print("NetworkBuster Distribution Manager")
        print("=" * 66)
        
    def _get_default_config_path(self):
        """Get default config path based on OS."""
        home = Path.home()
        return home / ".networkbuster" / "config.json"
    
    def _load_config(self):
        """Load configuration from file."""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {
            "git_username": "unknown",
            "protocol": "https",
            "repository": "datacentral-cloud-llc",
            "owner": "Cleanskiier27",
            "distribution_path": "./dist",
            "auto_download": True
        }
    
    def download_from_releases(self, tag="latest"):
        """Download distribution from GitHub releases."""
        owner = self.config["owner"]
        repo = self.config["repository"]
        
        if tag == "latest":
            url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
        else:
            url = f"https://api.github.com/repos/{owner}/{repo}/releases/tags/{tag}"
        
        print(f"📥 Fetching release info from: {url}")
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            release_data = response.json()
            
            print(f"✅ Found release: {release_data.get('name', 'Unknown')}")
            
            # Find zip asset
            assets = release_data.get("assets", [])
            zip_asset = None
            
            for asset in assets:
                if asset["name"].endswith(".zip"):
                    zip_asset = asset
                    break
            
            if not zip_asset:
                print("❌ No .zip file found in release assets")
                return False
            
            download_url = zip_asset["browser_download_url"]
            filename = zip_asset["name"]
            filesize = zip_asset["size"] / (1024 * 1024)
            
            print(f"📦 Downloading: {filename} ({filesize:.2f} MB)")
            return self._download_file(download_url, filename)
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching release: {e}")
            return False
    
    def download_local_distro(self, webapp_url="http://localhost:5000"):
        """Download distribution from local WebApp."""
        download_url = f"{webapp_url}/download"
        
        print(f"📥 Downloading from local WebApp: {download_url}")
        
        try:
            response = requests.get(download_url, timeout=10, stream=True)
            response.raise_for_status()
            
            # Extract filename from Content-Disposition header
            content_disposition = response.headers.get("content-disposition", "")
            filename = "networkbuster-distro.zip"
            
            if "filename=" in content_disposition:
                filename = content_disposition.split("filename=")[1].strip('"')
            
            filesize = int(response.headers.get("content-length", 0)) / (1024 * 1024)
            print(f"📦 Downloading: {filename} ({filesize:.2f} MB)")
            
            # Download with progress
            self.dist_dir.mkdir(parents=True, exist_ok=True)
            filepath = self.dist_dir / filename
            
            downloaded = 0
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        percent = (downloaded / (filesize * 1024 * 1024)) * 100 if filesize else 0
                        print(f"   Progress: {percent:.1f}%", end='\r')
            
            print(f"\n✅ Downloaded to: {filepath}")
            return str(filepath)
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Download error: {e}")
            return False
    
    def _download_file(self, url, filename):
        """Download a file with progress reporting."""
        self.dist_dir.mkdir(parents=True, exist_ok=True)
        filepath = self.dist_dir / filename
        
        try:
            response = requests.get(url, timeout=30, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get("content-length", 0))
            downloaded = 0
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size:
                            percent = (downloaded / total_size) * 100
                            print(f"   Progress: {percent:.1f}%", end='\r')
            
            print(f"\n✅ Downloaded to: {filepath}")
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Download failed: {e}")
            return False
    
    def list_available_distros(self):
        """List available distributions."""
        if not self.dist_dir.exists():
            print("❌ Distribution directory not found")
            return []
        
        distros = list(self.dist_dir.glob("*.zip"))
        if not distros:
            print("❌ No distributions found")
            return []
        
        print(f"✅ Found {len(distros)} distribution(s):")
        for distro in sorted(distros, key=lambda p: p.stat().st_mtime, reverse=True):
            size_mb = distro.stat().st_size / (1024 * 1024)
            mtime = datetime.fromtimestamp(distro.stat().st_mtime)
            print(f"   📦 {distro.name}")
            print(f"      Size: {size_mb:.2f} MB | Modified: {mtime}")
        
        return [str(d) for d in distros]
    
    def extract_distro(self, distro_path, extract_to=None):
        """Extract a distribution zip file."""
        distro_path = Path(distro_path)
        extract_to = Path(extract_to or "./networkbuster-extracted")
        
        if not distro_path.exists():
            print(f"❌ Distribution file not found: {distro_path}")
            return False
        
        print(f"📂 Extracting to: {extract_to}")
        
        try:
            shutil.unpack_archive(str(distro_path), str(extract_to))
            print(f"✅ Extracted successfully!")
            return str(extract_to)
        except Exception as e:
            print(f"❌ Extraction failed: {e}")
            return False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="NetworkBuster Distribution Download Manager")
    parser.add_argument("--config", help="Path to config file")
    parser.add_argument("--local", action="store_true", help="Download from local WebApp")
    parser.add_argument("--webapp-url", default="http://localhost:5000", help="Local WebApp URL")
    parser.add_argument("--github", action="store_true", help="Download from GitHub releases")
    parser.add_argument("--tag", default="latest", help="GitHub release tag")
    parser.add_argument("--list", action="store_true", help="List available distributions")
    parser.add_argument("--extract", help="Extract a distribution file")
    parser.add_argument("--extract-to", help="Extract destination path")
    
    args = parser.parse_args()
    
    manager = DistroDownloadManager(args.config)
    manager.print_banner()
    
    if args.list:
        manager.list_available_distros()
    elif args.extract:
        manager.extract_distro(args.extract, args.extract_to)
    elif args.local:
        result = manager.download_local_distro(args.webapp_url)
        if result:
            print(f"\n📥 Download complete: {result}")
    elif args.github:
        result = manager.download_from_releases(args.tag)
        if result:
            print(f"\n📥 Download complete: {result}")
    else:
        # Default: try local first, then GitHub
        
        # Try local WebApp
        print(f"\n1️⃣ Attempting local download from {args.webapp_url}...")
        result = manager.download_local_distro(args.webapp_url)
        
        if not result:
            print(f"\n2️⃣ Local download failed. Trying GitHub releases...")
            result = manager.download_from_releases()
        
        if result:
            print(f"\n✅ Distribution downloaded successfully!")
        else:
            print(f"\n❌ Failed to download distribution")
            sys.exit(1)


if __name__ == "__main__":
    main()

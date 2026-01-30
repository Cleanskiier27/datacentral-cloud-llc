"""
Personal Access Token Management System for networkbuster

This module provides functionality for generating, validating, and managing
personal access tokens.
"""

import secrets
import hashlib
import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, List


class TokenManager:
    """Manages personal access tokens with secure storage and validation."""
    
    def __init__(self, storage_path: str = "tokens.json"):
        """
        Initialize the TokenManager.
        
        Args:
            storage_path: Path to the JSON file for storing token data
        """
        self.storage_path = storage_path
        self.tokens = self._load_tokens()
    
    def _load_tokens(self) -> Dict:
        """Load tokens from storage file."""
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_tokens(self) -> None:
        """Save tokens to storage file."""
        with open(self.storage_path, 'w') as f:
            json.dump(self.tokens, f, indent=2)
    
    def _hash_token(self, token: str) -> str:
        """
        Hash a token for secure storage.
        
        Args:
            token: The plain text token to hash
            
        Returns:
            SHA256 hash of the token
        """
        return hashlib.sha256(token.encode()).hexdigest()
    
    def generate_token(
        self, 
        name: str, 
        scopes: Optional[List[str]] = None,
        expiry_days: Optional[int] = None
    ) -> str:
        """
        Generate a new personal access token.
        
        Args:
            name: Human-readable name for the token
            scopes: List of permission scopes for the token
            expiry_days: Number of days until token expires (None for no expiry)
            
        Returns:
            The generated token (only returned once)
        """
        # Generate a secure random token
        token = f"pat_{secrets.token_urlsafe(32)}"
        token_hash = self._hash_token(token)
        
        # Calculate expiry date if provided
        expiry = None
        if expiry_days:
            expiry = (datetime.now() + timedelta(days=expiry_days)).isoformat()
        
        # Store token metadata
        self.tokens[token_hash] = {
            "name": name,
            "scopes": scopes or [],
            "created_at": datetime.now().isoformat(),
            "expiry": expiry,
            "last_used": None
        }
        
        self._save_tokens()
        return token
    
    def validate_token(self, token: str) -> bool:
        """
        Validate a token.
        
        Args:
            token: The token to validate
            
        Returns:
            True if token is valid, False otherwise
        """
        token_hash = self._hash_token(token)
        
        if token_hash not in self.tokens:
            return False
        
        token_data = self.tokens[token_hash]
        
        # Check if token has expired
        if token_data.get("expiry"):
            expiry = datetime.fromisoformat(token_data["expiry"])
            if datetime.now() > expiry:
                return False
        
        # Update last used timestamp
        token_data["last_used"] = datetime.now().isoformat()
        self._save_tokens()
        
        return True
    
    def revoke_token(self, name: str) -> bool:
        """
        Revoke a token by its name.
        
        Args:
            name: Name of the token to revoke
            
        Returns:
            True if token was found and revoked, False otherwise
        """
        for token_hash, token_data in list(self.tokens.items()):
            if token_data["name"] == name:
                del self.tokens[token_hash]
                self._save_tokens()
                return True
        return False
    
    def list_tokens(self) -> List[Dict]:
        """
        List all tokens (without revealing the actual token values).
        
        Returns:
            List of token metadata dictionaries
        """
        return [
            {
                "name": data["name"],
                "scopes": data["scopes"],
                "created_at": data["created_at"],
                "expiry": data["expiry"],
                "last_used": data["last_used"]
            }
            for data in self.tokens.values()
        ]
    
    def get_token_scopes(self, token: str) -> Optional[List[str]]:
        """
        Get the scopes associated with a token.
        
        Args:
            token: The token to check
            
        Returns:
            List of scopes if token is valid, None otherwise
        """
        if not self.validate_token(token):
            return None
        
        token_hash = self._hash_token(token)
        return self.tokens[token_hash].get("scopes", [])

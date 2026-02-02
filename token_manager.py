"""
Personal Access Token Management System for networkbuster

This module provides functionality for generating, validating, and managing
personal access tokens.
"""

import secrets
import bcrypt
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
            try:
                with open(self.storage_path, 'r') as f:
                    return json.load(f)
            except (IOError, PermissionError, json.JSONDecodeError) as e:
                raise RuntimeError(f"Failed to load tokens from {self.storage_path}: {e}")
        return {}
    
    def _save_tokens(self) -> None:
        """Save tokens to storage file with secure permissions."""
        try:
            # Create file with restricted permissions (owner read/write only)
            flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
            mode = 0o600  # rw------- (owner read/write only)
            fd = os.open(self.storage_path, flags, mode)
            with os.fdopen(fd, 'w') as f:
                json.dump(self.tokens, f, indent=2)
        except (IOError, PermissionError) as e:
            raise RuntimeError(f"Failed to save tokens to {self.storage_path}: {e}")
    
    def _hash_token(self, token: str) -> str:
        """
        Hash a token for secure storage using bcrypt.
        
        Args:
            token: The plain text token to hash
            
        Returns:
            bcrypt hash of the token
        """
        return bcrypt.hashpw(token.encode(), bcrypt.gensalt()).decode()
    
    def generate_token(
        self, 
        name: str, 
        scopes: Optional[List[str]] = None,
        expiry_days: Optional[int] = None
    ) -> str:
        """
        Generate a new personal access token.
        
        Args:
            name: Human-readable name for the token (must be unique)
            scopes: List of permission scopes for the token
            expiry_days: Number of days until token expires (None for no expiry)
            
        Returns:
            The generated token (only returned once)
            
        Raises:
            ValueError: If a token with the given name already exists
        """
        # Check if name already exists
        for token_data in self.tokens.values():
            if token_data["name"] == name:
                raise ValueError(f"A token with name '{name}' already exists")
        
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
    
    def validate_token(self, token: str, update_last_used: bool = True) -> bool:
        """
        Validate a token.
        
        Args:
            token: The token to validate
            update_last_used: Whether to update the last_used timestamp
            
        Returns:
            True if token is valid, False otherwise
        """
        # Check each stored token hash
        for token_hash, token_data in self.tokens.items():
            try:
                if bcrypt.checkpw(token.encode(), token_hash.encode()):
                    # Check if token has expired
                    if token_data.get("expiry"):
                        expiry = datetime.fromisoformat(token_data["expiry"])
                        if datetime.now() > expiry:
                            return False
                    
                    # Update last used timestamp if requested
                    if update_last_used:
                        token_data["last_used"] = datetime.now().isoformat()
                        self._save_tokens()
                    
                    return True
            except Exception:
                # Skip invalid hashes
                continue
        
        return False
    
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
        Get the scopes associated with a token without updating last_used.
        
        Args:
            token: The token to check
            
        Returns:
            List of scopes if token is valid, None otherwise
        """
        # Validate without updating last_used
        if not self.validate_token(token, update_last_used=False):
            return None
        
        # Find the token data
        for token_hash, token_data in self.tokens.items():
            try:
                if bcrypt.checkpw(token.encode(), token_hash.encode()):
                    return token_data.get("scopes", [])
            except Exception:
                continue
        
        return None

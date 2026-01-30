"""
Unit tests for the TokenManager class.
"""

import unittest
import os
import json
from datetime import datetime, timedelta
from token_manager import TokenManager


class TestTokenManager(unittest.TestCase):
    """Test cases for TokenManager."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_storage = "test_tokens.json"
        self.manager = TokenManager(storage_path=self.test_storage)
    
    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.test_storage):
            os.remove(self.test_storage)
    
    def test_generate_token(self):
        """Test token generation."""
        token = self.manager.generate_token("test-token")
        
        # Token should start with 'pat_'
        self.assertTrue(token.startswith("pat_"))
        
        # Token should be stored
        tokens = self.manager.list_tokens()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0]["name"], "test-token")
    
    def test_generate_token_with_scopes(self):
        """Test token generation with scopes."""
        scopes = ["read", "write", "admin"]
        token = self.manager.generate_token("scoped-token", scopes=scopes)
        
        token_scopes = self.manager.get_token_scopes(token)
        self.assertEqual(token_scopes, scopes)
    
    def test_generate_token_with_expiry(self):
        """Test token generation with expiry."""
        token = self.manager.generate_token("expiring-token", expiry_days=7)
        
        # Token should be valid now
        self.assertTrue(self.manager.validate_token(token))
        
        # Check that expiry is set
        tokens = self.manager.list_tokens()
        self.assertIsNotNone(tokens[0]["expiry"])
    
    def test_validate_token(self):
        """Test token validation."""
        token = self.manager.generate_token("valid-token")
        
        # Token should be valid
        self.assertTrue(self.manager.validate_token(token))
        
        # Invalid token should fail
        self.assertFalse(self.manager.validate_token("pat_invalid"))
    
    def test_validate_token_updates_last_used(self):
        """Test that validation updates last_used timestamp."""
        token = self.manager.generate_token("test-token")
        
        # First validation
        self.assertTrue(self.manager.validate_token(token))
        tokens = self.manager.list_tokens()
        self.assertIsNotNone(tokens[0]["last_used"])
    
    def test_revoke_token(self):
        """Test token revocation."""
        token = self.manager.generate_token("revokable-token")
        
        # Token should be valid initially
        self.assertTrue(self.manager.validate_token(token))
        
        # Revoke the token
        success = self.manager.revoke_token("revokable-token")
        self.assertTrue(success)
        
        # Token should no longer be valid
        self.assertFalse(self.manager.validate_token(token))
    
    def test_revoke_nonexistent_token(self):
        """Test revoking a token that doesn't exist."""
        success = self.manager.revoke_token("nonexistent")
        self.assertFalse(success)
    
    def test_list_tokens(self):
        """Test listing tokens."""
        # Generate multiple tokens
        self.manager.generate_token("token1", scopes=["read"])
        self.manager.generate_token("token2", scopes=["write"])
        self.manager.generate_token("token3")
        
        tokens = self.manager.list_tokens()
        self.assertEqual(len(tokens), 3)
        
        # Check token names
        names = [t["name"] for t in tokens]
        self.assertIn("token1", names)
        self.assertIn("token2", names)
        self.assertIn("token3", names)
    
    def test_get_token_scopes(self):
        """Test getting token scopes."""
        scopes = ["read", "write"]
        token = self.manager.generate_token("test-token", scopes=scopes)
        
        retrieved_scopes = self.manager.get_token_scopes(token)
        self.assertEqual(retrieved_scopes, scopes)
        
        # Invalid token should return None
        invalid_scopes = self.manager.get_token_scopes("pat_invalid")
        self.assertIsNone(invalid_scopes)
    
    def test_token_persistence(self):
        """Test that tokens persist across manager instances."""
        token = self.manager.generate_token("persistent-token")
        
        # Create new manager instance with same storage
        new_manager = TokenManager(storage_path=self.test_storage)
        
        # Token should still be valid
        self.assertTrue(new_manager.validate_token(token))
        
        # Should see the token in the list
        tokens = new_manager.list_tokens()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0]["name"], "persistent-token")


if __name__ == "__main__":
    unittest.main()

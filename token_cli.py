#!/usr/bin/env python3
"""
Command-line interface for managing personal access tokens.
"""

import argparse
import sys
from token_manager import TokenManager


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Personal Access Token Manager for networkbuster"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Generate token command
    generate_parser = subparsers.add_parser(
        "generate",
        help="Generate a new personal access token"
    )
    generate_parser.add_argument(
        "name",
        help="Name for the token"
    )
    generate_parser.add_argument(
        "--scopes",
        nargs="+",
        help="Permission scopes for the token"
    )
    generate_parser.add_argument(
        "--expiry-days",
        type=int,
        help="Number of days until token expires"
    )
    
    # Validate token command
    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate a token"
    )
    validate_parser.add_argument(
        "token",
        help="Token to validate"
    )
    
    # Revoke token command
    revoke_parser = subparsers.add_parser(
        "revoke",
        help="Revoke a token by name"
    )
    revoke_parser.add_argument(
        "name",
        help="Name of the token to revoke"
    )
    
    # List tokens command
    subparsers.add_parser(
        "list",
        help="List all tokens"
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Initialize token manager
    manager = TokenManager()
    
    # Handle commands
    if args.command == "generate":
        try:
            token = manager.generate_token(
                name=args.name,
                scopes=args.scopes,
                expiry_days=args.expiry_days
            )
            print(f"Generated token: {token}")
            print("\nIMPORTANT: Save this token securely. It will not be shown again.")
            return 0
        except ValueError as e:
            print(f"[ERROR] {e}")
            return 1
    
    elif args.command == "validate":
        # Get scopes without updating last_used first
        scopes = manager.get_token_scopes(args.token)
        if scopes is not None:
            # Now validate and update last_used
            manager.validate_token(args.token)
            print("[OK] Token is valid")
            print(f"Scopes: {', '.join(scopes) if scopes else 'none'}")
            return 0
        else:
            print("[FAIL] Token is invalid or expired")
            return 1
    
    elif args.command == "revoke":
        success = manager.revoke_token(args.name)
        if success:
            print(f"[OK] Token '{args.name}' has been revoked")
            return 0
        else:
            print(f"[FAIL] Token '{args.name}' not found")
            return 1
    
    elif args.command == "list":
        tokens = manager.list_tokens()
        if not tokens:
            print("No tokens found")
            return 0
        
        print(f"Found {len(tokens)} token(s):\n")
        for token in tokens:
            print(f"Name: {token['name']}")
            print(f"  Created: {token['created_at']}")
            print(f"  Scopes: {', '.join(token['scopes']) if token['scopes'] else 'none'}")
            print(f"  Expiry: {token['expiry'] or 'never'}")
            print(f"  Last used: {token['last_used'] or 'never'}")
            print()
        return 0
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

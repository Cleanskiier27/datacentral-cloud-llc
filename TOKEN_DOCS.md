# Personal Access Token System

A secure personal access token (PAT) management system for networkbuster.

## Features

- **Secure Token Generation**: Generates cryptographically secure tokens using Python's `secrets` module
- **Token Validation**: Validates tokens with expiry checking
- **Scope-Based Permissions**: Supports fine-grained permission scopes
- **Token Expiry**: Optional expiration dates for enhanced security
- **Secure Storage**: Tokens are hashed using SHA-256 before storage
- **CLI Interface**: Easy-to-use command-line tool
- **Token Management**: List, revoke, and validate tokens

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Make the CLI tool executable:
```bash
chmod +x token_cli.py
```

## Usage

### Command Line Interface

#### Generate a Token

Generate a basic token:
```bash
python token_cli.py generate "my-token"
```

Generate a token with scopes:
```bash
python token_cli.py generate "api-token" --scopes read write admin
```

Generate a token with expiry:
```bash
python token_cli.py generate "temp-token" --expiry-days 30
```

#### Validate a Token

```bash
python token_cli.py validate pat_xxxxxxxxxxxxxxxxxxxxx
```

#### List Tokens

```bash
python token_cli.py list
```

#### Revoke a Token

```bash
python token_cli.py revoke "my-token"
```

### Python API

```python
from token_manager import TokenManager

# Initialize the manager
manager = TokenManager()

# Generate a token
token = manager.generate_token(
    name="my-app-token",
    scopes=["read", "write"],
    expiry_days=90
)
print(f"Your token: {token}")

# Validate a token
if manager.validate_token(token):
    print("Token is valid!")
    scopes = manager.get_token_scopes(token)
    print(f"Token has scopes: {scopes}")

# List all tokens
tokens = manager.list_tokens()
for token_info in tokens:
    print(f"Token: {token_info['name']}")
    print(f"  Scopes: {token_info['scopes']}")
    print(f"  Created: {token_info['created_at']}")

# Revoke a token
manager.revoke_token("my-app-token")
```

## Security Considerations

1. **Token Storage**: Tokens are hashed using bcrypt before storage. Only the bcrypt hash is stored, never the plain text token. Bcrypt is designed to be computationally expensive and resistant to brute-force attacks.

2. **File Permissions**: The tokens.json file is created with restricted permissions (0o600 - owner read/write only) to prevent unauthorized access.

3. **Token Format**: Tokens use the format `pat_` followed by a URL-safe random string.

4. **One-Time Display**: The actual token value is only displayed once during generation. Store it securely.

5. **Expiry**: Set expiration dates on tokens to limit their lifetime.

6. **Scopes**: Use scopes to limit what a token can access.

## Testing

Run the test suite:
```bash
python -m unittest test_token_manager.py
```

Run tests with verbose output:
```bash
python -m unittest test_token_manager.py -v
```

## Token Storage

Tokens are stored in a JSON file (default: `tokens.json`) with the following structure:

```json
{
  "token_hash": {
    "name": "my-token",
    "scopes": ["read", "write"],
    "created_at": "2026-01-30T12:00:00",
    "expiry": "2026-04-30T12:00:00",
    "last_used": "2026-01-30T13:45:00"
  }
}
```

**Important**: The `tokens.json` file should be kept secure and never committed to version control. It's included in `.gitignore` by default.

## Architecture

### TokenManager Class

The `TokenManager` class provides the core functionality:

- `generate_token(name, scopes, expiry_days)`: Creates a new token
- `validate_token(token)`: Validates a token and updates last_used
- `revoke_token(name)`: Removes a token by name
- `list_tokens()`: Returns metadata for all tokens
- `get_token_scopes(token)`: Returns scopes for a valid token

### CLI Tool

The `token_cli.py` script provides a user-friendly interface to the TokenManager functionality.

## Example Workflow

```bash
# Generate a new token for API access
python token_cli.py generate "api-key" --scopes api:read api:write --expiry-days 90

# The tool outputs:
# Generated token: pat_abcdef123456...
# IMPORTANT: Save this token securely. It will not be shown again.

# Later, validate the token
python token_cli.py validate pat_abcdef123456...
# ✓ Token is valid
# Scopes: api:read, api:write

# List all active tokens
python token_cli.py list
# Found 1 token(s):
# Name: api-key
#   Created: 2026-01-30T12:00:00
#   Scopes: api:read, api:write
#   Expiry: 2026-04-30T12:00:00
#   Last used: 2026-01-30T13:45:00

# Revoke when no longer needed
python token_cli.py revoke "api-key"
# ✓ Token 'api-key' has been revoked
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is part of datacentral-cloud-llc / networkbuster.

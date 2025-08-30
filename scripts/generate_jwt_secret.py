#!/usr/bin/env python3

import secrets
import base64
import os

def generate_strong_key(length=64):
    """
    Generate a cryptographically strong random key
    """
    # Generate random bytes
    random_bytes = secrets.token_bytes(length)
    # Convert to URL-safe base64 string
    return base64.urlsafe_b64encode(random_bytes).decode('utf-8')

def update_env_file(key):
    """
    Update .env file with the new JWT secret key
    """
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    env_example_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env.example')
    
    # Check if .env file exists
    if os.path.exists(env_path):
        # Read existing .env file
        with open(env_path, 'r') as f:
            lines = f.readlines()
        
        # Check if JWT_SECRET_KEY already exists
        key_exists = False
        for i, line in enumerate(lines):
            if line.startswith('JWT_SECRET_KEY='):
                lines[i] = f'JWT_SECRET_KEY={key}\n'
                key_exists = True
                break
        
        # Add key if it doesn't exist
        if not key_exists:
            lines.append(f'JWT_SECRET_KEY={key}\n')
        
        # Write updated content back to .env file
        with open(env_path, 'w') as f:
            f.writelines(lines)
    else:
        # Create new .env file if it doesn't exist
        # First check if .env.example exists and copy from it
        if os.path.exists(env_example_path):
            with open(env_example_path, 'r') as f:
                lines = f.readlines()
            
            # Replace or add JWT_SECRET_KEY
            key_exists = False
            for i, line in enumerate(lines):
                if line.startswith('JWT_SECRET_KEY='):
                    lines[i] = f'JWT_SECRET_KEY={key}\n'
                    key_exists = True
                    break
            
            if not key_exists:
                lines.append(f'JWT_SECRET_KEY={key}\n')
            
            with open(env_path, 'w') as f:
                f.writelines(lines)
        else:
            # Create minimal .env file
            with open(env_path, 'w') as f:
                f.write(f'JWT_SECRET_KEY={key}\n')

def main():
    # Generate a strong key
    key = generate_strong_key()
    print(f"Generated JWT secret key: {key}")
    
    # Update .env file
    update_env_file(key)
    print(f"Updated .env file with new JWT secret key")

if __name__ == "__main__":
    main()
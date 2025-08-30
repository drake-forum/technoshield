#!/bin/bash

# Script to generate self-signed SSL certificates for TECHNOSHIELD

CERTS_DIR="../frontend/ssl"

# Create directory for certificates if it doesn't exist
mkdir -p "$CERTS_DIR"

# Generate a private key
openssl genrsa -out "$CERTS_DIR/technoshield.key" 2048

# Generate a CSR (Certificate Signing Request)
openssl req -new -key "$CERTS_DIR/technoshield.key" -out "$CERTS_DIR/technoshield.csr" -subj "/C=US/ST=State/L=City/O=TECHNOSHIELD/OU=Security/CN=localhost"

# Generate a self-signed certificate (valid for 365 days)
openssl x509 -req -days 365 -in "$CERTS_DIR/technoshield.csr" -signkey "$CERTS_DIR/technoshield.key" -out "$CERTS_DIR/technoshield.crt"

# Remove the CSR as it's no longer needed
rm "$CERTS_DIR/technoshield.csr"

echo "SSL certificates generated successfully in $CERTS_DIR"
echo "  - technoshield.key: Private key"
echo "  - technoshield.crt: Self-signed certificate"
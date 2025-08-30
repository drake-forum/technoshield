# SSL Certificates for TECHNOSHIELD

This directory contains SSL certificates for secure HTTPS connections.

## Self-Signed Certificates

For development and testing purposes, self-signed certificates are included in this directory:

- `technoshield.crt`: SSL certificate file
- `technoshield.key`: SSL private key file

## Production Usage

For production environments, replace these self-signed certificates with properly issued certificates from a trusted Certificate Authority (CA).

## Generating New Self-Signed Certificates

To generate new self-signed certificates, use the following OpenSSL command:

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout technoshield.key -out technoshield.crt
```

When prompted, enter the appropriate information for your organization and deployment.
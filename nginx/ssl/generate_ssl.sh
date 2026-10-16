#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "Generating self-signed SSL certificate for localhost..."
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout key.pem \
    -out cert.pem \
    -subj "/C=VN/ST=Hanoi/L=Hanoi/O=De34ContractManagement/OU=IT/CN=localhost" \
    -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"

chmod 600 key.pem
chmod 644 cert.pem

echo "SSL Certificate and Key generated successfully in $DIR:"
ls -lh "$DIR"/*.pem

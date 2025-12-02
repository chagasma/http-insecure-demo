#!/bin/bash

echo "Generating legitimate certificate..."
openssl req -x509 -newkey rsa:2048 -keyout legitimate_key.pem -out legitimate_cert.pem -days 365 -nodes -subj "/CN=legitimate-bank.com"

echo "Generating fake certificate (MITM)..."
openssl req -x509 -newkey rsa:2048 -keyout fake_key.pem -out fake_cert.pem -days 365 -nodes -subj "/CN=legitimate-bank.com"

echo "Done. Certificates created:"
echo "  - legitimate_cert.pem / legitimate_key.pem"
echo "  - fake_cert.pem / fake_key.pem"

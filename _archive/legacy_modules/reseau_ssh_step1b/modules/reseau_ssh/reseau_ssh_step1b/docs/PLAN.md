## Canonical names (final)
- admin-trading (Debian) 192.168.16.155
- student (Debian)       192.168.16.103
- db-layer (MSI Ubuntu)  192.168.16.179
- cursor-ai (Dell Win)   192.168.16.224

Goal:
From any machine:
- ssh admin-trading
- ssh db-layer
- ssh student
- ssh cursor-ai (only if OpenSSH Server enabled on Windows)

Key strategy:
Linux ssh config tries both:
- ~/.ssh/id_ed25519
- ~/.ssh/id_ed25519_fantome

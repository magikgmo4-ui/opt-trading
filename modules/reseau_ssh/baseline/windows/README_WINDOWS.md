## cursor-ai (Dell Windows) — baseline apply

Open PowerShell as Administrator in this folder.

Basic (hosts + ssh config):
`powershell -ExecutionPolicy Bypass -File .\apply_cursor_ai.ps1`

Enable OpenSSH Server:
`powershell -ExecutionPolicy Bypass -File .\apply_cursor_ai.ps1 -EnableOpenSSHServer`

Pull keys bundle from admin-trading and append to `authorized_keys`:
`powershell -ExecutionPolicy Bypass -File .\apply_cursor_ai.ps1 -PullKeysBundle`

Combined:
`powershell -ExecutionPolicy Bypass -File .\apply_cursor_ai.ps1 -EnableOpenSSHServer -PullKeysBundle`

## Target
1 module canonique par famille.

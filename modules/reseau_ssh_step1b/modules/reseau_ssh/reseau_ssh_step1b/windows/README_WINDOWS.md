## cursor-ai (Dell Windows) — apply

Open PowerShell as Administrator in this folder.

Basic (hosts + ssh config):
  powershell -ExecutionPolicy Bypass -File .\apply_cursor_ai.ps1

Enable OpenSSH Server (so Linux can ssh into Windows):
  powershell -ExecutionPolicy Bypass -File .\apply_cursor_ai.ps1 -EnableOpenSSHServer

Pull keys bundle from admin-trading and append to authorized_keys:
  # On admin-trading first:
  #   ./scripts/make_keys_bundle_admin.sh
  powershell -ExecutionPolicy Bypass -File .\apply_cursor_ai.ps1 -PullKeysBundle

Combined:
  powershell -ExecutionPolicy Bypass -File .\apply_cursor_ai.ps1 -EnableOpenSSHServer -PullKeysBundle

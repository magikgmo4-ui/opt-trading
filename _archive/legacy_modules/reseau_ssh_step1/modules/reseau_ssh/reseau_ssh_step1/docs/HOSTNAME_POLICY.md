## Hostname policy (important)

- Each machine MUST have a unique hostname on the network.
  Otherwise: collisions in mDNS/NetBIOS/known_hosts and confusing logs.

- You will still have "same names everywhere" in practice via SSH aliases:
  admin-trading, student, msi, win

So:
- Unique `hostnamectl set-hostname <unique>`
- Same `~/.ssh/config` aliases on every Linux machine

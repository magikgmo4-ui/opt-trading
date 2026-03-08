#!/usr/bin/env python3
import re
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
MACHINES = ["admin-trading", "cursor-ai", "db-layer", "student"]

ROLE_MAP = {
  "admin-trading": ("OPS / main services host", [
    "Bastion SSH + orchestration services",
    "Hosts repos + operational scripts",
    "Runs APIs/UI on LAN-only"
  ]),
  "cursor-ai": ("DEV workstation (Cursor)", [
    "Main dev workstation (Cursor, UI, browser tools)",
    "Push/pull + deploy to Debian hosts via SSH"
  ]),
  "db-layer": ("DB layer", [
    "Database / persistent backend services (LAN-only)",
    "Runs backend/API services as needed"
  ]),
  "student": ("Sandbox / experiments", [
    "Experiments, POCs, agent sandbox",
    "Receives sanitized datasets/logs"
  ]),
}

def read_latest_snapshot(machine: str) -> str:
    snap_dir = ROOT / "machines" / machine / "snapshot"
    snaps = sorted(snap_dir.glob("snapshot_*.txt"))
    if not snaps:
        raise SystemExit(f"No snapshot found for {machine} in {snap_dir}")
    return snaps[-1].read_text(encoding="utf-8", errors="replace")

def section(text: str, name: str) -> str:
    m = re.search(rf"^\[{re.escape(name)}\]\s*$", text, flags=re.M)
    if not m:
        return ""
    start = m.end()
    m2 = re.search(r"^\[[^\]]+\]\s*$", text[start:], flags=re.M)
    end = start + (m2.start() if m2 else len(text[start:]))
    return text[start:end].strip()

def first_match(pattern, text, flags=0, default=""):
    m = re.search(pattern, text, flags)
    return m.group(1).strip() if m else default

def parse_linux(text: str) -> dict:
    host = section(text, "host")
    osr  = section(text, "os-release")
    ker  = section(text, "kernel")
    cpu  = section(text, "cpu")
    mem  = section(text, "memory")
    df   = section(text, "disks df")
    lsblk= section(text, "disks lsblk")
    ip   = section(text, "network ip")
    rt   = section(text, "network routes")
    dns  = section(text, "dns")
    ports= section(text, "listening ports (top)")
    svcs = section(text, "running services sample")
    dock = section(text, "docker")

    hostname = first_match(r"Static hostname:\s*(.+)", host, re.M, "")
    os_name  = first_match(r'PRETTY_NAME="([^"]+)"', osr, re.M, "")
    kernel   = ker.splitlines()[0].strip() if ker else ""
    model    = first_match(r"Model name:\s*(.+)", cpu, re.M, "")
    cpus     = first_match(r"^CPU\(s\):\s*(.+)", cpu, re.M, "")
    cores    = first_match(r"^Core\(s\) per socket:\s*(.+)", cpu, re.M, "")
    sockets  = first_match(r"^Socket\(s\):\s*(.+)", cpu, re.M, "")
    memline  = first_match(r"^Mem:\s+(.+)$", mem, re.M, "")

    gateway = first_match(r"^default via (\S+)", rt, re.M, "")

    iface = ""
    ipaddr = ""
    for line in ip.splitlines():
        if line.startswith("lo "):
            continue
        parts = line.split()
        if len(parts) >= 3:
            iface = parts[0]
            ipaddr = parts[2]
            break

    dns_servers = []
    for line in dns.splitlines():
        line=line.strip()
        if line.startswith("nameserver "):
            dns_servers.append(line.split()[1])

    listen_ports = []
    for line in ports.splitlines():
        m = re.search(r"(\d+\.\d+\.\d+\.\d+|\*|::|::1|\[::\]|0\.0\.0\.0):(\d+)\b", line)
        if m:
            listen_ports.append(m.group(2))
    listen_ports = sorted(set(listen_ports), key=lambda x: int(x))

    interesting = []
    for line in svcs.splitlines():
        if any(k in line.lower() for k in ["desk", "tv-", "webhook", "perf", "algo", "mongo", "postg", "click", "timescale"]):
            interesting.append(line.strip())
    interesting = interesting[:30]

    return {
        "hostname": hostname,
        "os": os_name,
        "kernel": kernel,
        "cpu_model": model,
        "cpu_counts": f"CPU(s)={cpus} sockets={sockets} cores/socket={cores}".strip(),
        "memory": memline,
        "iface": iface,
        "ip": ipaddr,
        "gateway": gateway,
        "dns": ", ".join(dns_servers) if dns_servers else "",
        "ports": ", ".join(listen_ports) if listen_ports else "",
        "df": "\n".join(df.splitlines()[:14]).strip(),
        "lsblk": "\n".join(lsblk.splitlines()[:20]).strip(),
        "services": "\n".join(interesting).strip(),
        "docker": "\n".join(dock.splitlines()[:25]).strip(),
    }

def parse_windows(text: str) -> dict:
    host = section(text, "host") or ""
    osb  = section(text, "os")
    cpu  = section(text, "cpu")
    mem  = section(text, "memory")
    disk = section(text, "disks")
    net  = section(text, "network")
    ports= section(text, "ports listening (top)")

    hostname = host.splitlines()[0].strip() if host else ""
    os_name  = first_match(r"WindowsProductName\s*:\s*(.+)", osb, re.M, "")
    os_ver   = first_match(r"WindowsVersion\s*:\s*(.+)", osb, re.M, "")
    cpu_name = first_match(r"Name\s*:\s*(.+)", cpu, re.M, "")
    cores    = first_match(r"NumberOfCores\s*:\s*(.+)", cpu, re.M, "")
    threads  = first_match(r"NumberOfLogicalProcessors\s*:\s*(.+)", cpu, re.M, "")
    memtot   = first_match(r"TotalPhysicalMemory\s*:\s*(.+)", mem, re.M, "")

    ipaddr = first_match(r"IPv4Address\s*:\s*\{?(\d+\.\d+\.\d+\.\d+)", net, re.M, "")
    gateway = first_match(r"IPv4DefaultGateway\s*:\s*\{?(\d+\.\d+\.\d+\.\d+)", net, re.M, "")
    dns = ""

    listen_ports = []
    for line in ports.splitlines():
        m = re.search(r":(\d+)\s+LISTENING", line)
        if m:
            listen_ports.append(m.group(1))
    listen_ports = sorted(set(listen_ports), key=lambda x: int(x))

    return {
        "hostname": hostname,
        "os": f"{os_name} ({os_ver})".strip(),
        "kernel": "",
        "cpu_model": cpu_name,
        "cpu_counts": f"cores={cores} threads={threads}".strip(),
        "memory": memtot,
        "iface": "",
        "ip": ipaddr,
        "gateway": gateway,
        "dns": dns,
        "ports": ", ".join(listen_ports[:50]),
        "df": disk.strip(),
        "lsblk": "",
        "services": "",
        "docker": "",
    }

def write_md(machine: str, info: dict):
    mdir = ROOT / "machines" / machine
    now = datetime.now().isoformat(timespec="seconds")
    (mdir / "fiche_machine.md").write_text(f"""# Fiche Machine — {machine}

## Identité
- Hostname: {info.get("hostname","")}
- OS: {info.get("os","")}
- Kernel: {info.get("kernel","")}
- CPU: {info.get("cpu_model","")}
- CPU details: {info.get("cpu_counts","")}
- RAM: {info.get("memory","")}

## Réseau (LAN)
- Subnet: 192.168.16.0/24
- Interface: {info.get("iface","")}
- IP: {info.get("ip","")}
- Gateway: {info.get("gateway","")}
- DNS: {info.get("dns","")}
- Ports en écoute (snapshot): {info.get("ports","")}

## Stockage (extrait)
### df / volumes
```
{info.get("df","")}
```

### lsblk
```
{info.get("lsblk","")}
```

## Services (extrait)
```
{info.get("services","")}
```

## Docker (extrait)
```
{info.get("docker","")}
```

> Généré automatiquement depuis le snapshot le {now}.
""", encoding="utf-8")

    (mdir / "reseau.md").write_text(f"""# Réseau — {machine} (LAN only)

- Subnet: 192.168.16.0/24
- IP: {info.get("ip","")}
- Interface: {info.get("iface","")}
- Gateway: {info.get("gateway","")}
- DNS: {info.get("dns","")}

## Ports en écoute (snapshot)
{info.get("ports","")}

## Règles
- Pas d’exposition WAN directe
- Toute URL/tunnel doit être redacted (<REDACTED_TUNNEL>)
""", encoding="utf-8")

    role, bullets = ROLE_MAP.get(machine, ("(fill)", ["(fill)"]))
    bullets_md = "\n".join([f"- {b}" for b in bullets])
    (mdir / "roles.md").write_text(f"""# Roles — {machine}

- Rôle principal: {role}
- Responsabilités:
{bullets_md}
""", encoding="utf-8")

def main():
    for m in MACHINES:
        text = read_latest_snapshot(m)
        info = parse_windows(text) if m == "cursor-ai" else parse_linux(text)
        write_md(m, info)
    print("OK: fiches remplies pour:", ", ".join(MACHINES))

if __name__ == "__main__":
    main()

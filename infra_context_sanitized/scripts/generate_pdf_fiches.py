#!/usr/bin/env python3
"""Genere un PDF par machine a partir des fiches consolidees."""

from fpdf import FPDF

# Transliteration pour eviter erreurs Latin-1 (Helvetica)
_TRANS = str.maketrans({
    "\u2014": "-", "\u2013": "-", "\u00e9": "e", "\u00e8": "e",
    "\u00ea": "e", "\u00e0": "a", "\u00e2": "a", "\u00e7": "c",
    "\u00ee": "i", "\u00f4": "o", "\u00fb": "u", "\u00f9": "u",
    "\u00fc": "u", "\u00eb": "e", "\u00ef": "i", "\u00f6": "o",
    "\u0153": "oe", "\u00c9": "E", "\u00c0": "A", "\u00c7": "C",
})


def _latin1(s: str) -> str:
    return s.translate(_TRANS).encode("latin-1", "replace").decode("latin-1")
from pathlib import Path

# Données des machines (extrait de FICHES_MACHINES_REFERENCE.md)
MACHINES = {
    "admin-trading": {
        "hostname": "admin-trading",
        "materiel": "HP EliteBook 840 G1 (laptop)",
        "os": "Debian 12 (bookworm)",
        "kernel": "6.1.0-42-amd64",
        "cpu": "Intel Core i5-4300U @ 1.90 GHz (4 threads)",
        "ram": "7,7 Go",
        "disque": "219 Go (ext4 sur /)",
        "subnet": "192.168.0.0/24",
        "interface": "wlo1 (Wi-Fi)",
        "ip": "192.168.0.111",
        "gateway": "192.168.0.1",
        "dns": "192.168.0.1",
        "ports": "22, 631, 4040, 5353, 8000, 8010, 42029, 51385, 51820",
        "role": "OPS / hôte principal des services - Bastion SSH + orchestration - APIs / UI exposées uniquement en LAN",
        "services": "sshd, tv-webhook, tv-bitget-runner, <REDACTED_TUNNEL>-tv",
        "chemins": "Code: /opt/trading/, /opt/trading/modules/ | Scripts: /opt/trading/scripts/, /usr/local/bin/ | Logs: /var/log/, /opt/trading/tmp/",
    },
    "cursor-ai": {
        "hostname": "DESKTOP-1KDTQBH",
        "materiel": "Dell (poste de dev)",
        "os": "Windows 10 Pro (build 22621)",
        "kernel": "-",
        "cpu": "Intel Core i5-1145G7 @ 2.60 GHz (8 threads)",
        "ram": "16 Go",
        "disque": "C: ~589 Go, D: ~1 To, E: ~1.5 To (NTFS)",
        "subnet": "192.168.0.0/24",
        "interface": "Ethernet",
        "ip": "192.168.0.177",
        "gateway": "192.168.0.1",
        "dns": "192.168.0.1",
        "ports": "-",
        "role": "Poste de dev principal (Cursor, UI, navigateur) - Push/pull et déploiement vers les hôtes Debian via SSH",
        "services": "-",
        "chemins": "Code: C:\\Users\\ghost\\Desktop\\cursor_ai_workflow\\ | Transferts: C:\\Users\\ghost\\Downloads\\",
    },
    "db-layer": {
        "hostname": "ghost",
        "materiel": "MSI GE62 2QD (laptop)",
        "os": "Ubuntu 24.04.4 LTS",
        "kernel": "6.17.0-14-generic",
        "cpu": "Intel Core i7-5700HQ @ 2.70 GHz (8 threads)",
        "ram": "11 Go",
        "disque": "915 Go (ext4 sur /)",
        "subnet": "192.168.0.0/24",
        "interface": "enp4s0 (Ethernet)",
        "ip": "192.168.0.100",
        "gateway": "192.168.0.1",
        "dns": "",
        "ports": "22, 53, 631, 1901, 5353, 9100, 32400-32414, 32600, ...",
        "role": "Couche DB / services backend persistants - Hébergement bases de données (LAN-only)",
        "services": "sshd, algo-hf-api, plexmediaserver, gnome-remote-desktop",
        "chemins": "Données: /var/lib/postgresql/, /var/lib/docker/ | Logs: /var/log/",
    },
    "student": {
        "hostname": "student",
        "materiel": "HP ProDesk 600 G3 SFF (desktop)",
        "os": "Debian 12 (bookworm)",
        "kernel": "6.1.0-43-amd64",
        "cpu": "Intel Core i5-6500 @ 3.20 GHz (4 coeurs)",
        "ram": "7,6 Go",
        "disque": "28 Go /, 200 Go /home (LVM sur nvme, LUKS)",
        "subnet": "192.168.0.0/24",
        "interface": "eno1 (Ethernet)",
        "ip": "192.168.0.142",
        "gateway": "192.168.0.1",
        "dns": "1.1.1.1, 8.8.8.8",
        "ports": "22, 631, 5353, 8020, 45095, 59623",
        "role": "Sandbox / expérimentations / POC - Environnement pour agents et tests",
        "services": "sshd, fail2ban, student-ingest, student-watchdrop",
        "chemins": "Code: /opt/trading/ | Scripts: /opt/trading/scripts/, /usr/local/bin/",
    },
}


class FichePDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_margins(15, 15, 15)
        self.set_auto_page_break(auto=True, margin=15)

    def _section(self, title: str):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(60, 60, 60)
        self.cell(0, 8, _latin1(title), ln=True)

    def _line(self, label: str, value: str):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(0, 0, 0)
        self.cell(0, 6, _latin1(label) + ":", ln=True)
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5, _latin1(str(value)))

    def add_fiche(self, name: str, data: dict):
        self.add_page()
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(30, 60, 120)
        self.cell(0, 12, _latin1(f"Fiche machine - {name}"), ln=True)
        self.ln(4)

        self._section("Identite")
        self._line("Hostname", data["hostname"])
        self._line("Materiel", data["materiel"])
        self._line("OS", data["os"])
        if data.get("kernel") and data["kernel"] != "-":
            self._line("Kernel", data["kernel"])
        self._line("CPU", data["cpu"])
        self._line("RAM", data["ram"])
        self._line("Disque", data["disque"])
        self.ln(4)

        self._section("Reseau (LAN)")
        self._line("Subnet", data["subnet"])
        self._line("Interface", data["interface"])
        self._line("IP", data["ip"])
        self._line("Gateway", data["gateway"])
        self._line("DNS", data["dns"])
        if data.get("ports") and data["ports"] != "-":
            self._line("Ports", data["ports"])
        self.ln(4)

        self._section("Role")
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 6, _latin1(data["role"]))
        self.ln(4)

        if data.get("services") and data["services"] != "-":
            self._section("Services cles")
            self.set_font("Helvetica", "", 10)
            self.multi_cell(0, 6, _latin1(data["services"]))
            self.ln(4)

        self._section("Chemins utiles")
        self.set_font("Helvetica", "", 9)
        self.multi_cell(0, 5, _latin1(data["chemins"]))


def main():
    base = Path(__file__).resolve().parent.parent
    out_dir = base / "fiches_pdf"
    out_dir.mkdir(exist_ok=True)

    for name, data in MACHINES.items():
        pdf = FichePDF()
        pdf.add_fiche(name, data)
        path = out_dir / f"fiche_{name}.pdf"
        pdf.output(str(path))
        print(f"Genere: {path}")

    print(f"\n{len(MACHINES)} PDF(s) cree(s) dans {out_dir}")


if __name__ == "__main__":
    main()

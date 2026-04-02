from __future__ import annotations

from app.schemas.brick_schema import BrickModel


def render_handoff(bricks: list[BrickModel], target: str) -> str:
    latest = sorted(bricks, key=lambda b: b.date)[-1]
    lines = [
        f"HANDOFF {target.upper()} — MEMORY_BRICKS",
        "",
        "Etat de reprise:",
        f"- module cible: memory_bricks",
        f"- statut: {latest.status}",
        f"- architecture: Python local core + future API-ready layout",
        "",
        "Etabli:",
        "- source primaire = module local",
        "- LocalCMS = surface humaine future",
        "- export/handoff = surface IA immédiate",
        "",
        "Sources:",
    ]
    for brick in bricks:
        lines.append(f"- {brick.id} — {brick.title}")

    lines.extend([
        "",
        "Travail demandé:",
        "- poursuivre l'implémentation selon la spec verrouillée",
        "- respecter les statuts/types figés",
        "- ne pas dériver vers UI/API/cloud/mobile",
        "",
        "Limites:",
        "- API active hors périmètre V1",
        "- LocalCMS réservé comme surface future",
        "",
        "Point de reprise:",
        latest.resume_point or "-",
        "",
    ])
    return "\n".join(lines)

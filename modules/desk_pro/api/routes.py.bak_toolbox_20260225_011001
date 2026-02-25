from __future__ import annotations
import time
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from modules.desk_pro.models import DeskForm, Snapshot, ScoreResult
from modules.desk_pro.service.aggregator import build_snapshot_mock
from modules.desk_pro.service.scoring import compute_probability
from modules.desk_pro.ui.page import render_ui_html

router = APIRouter(prefix="/desk", tags=["desk-pro"])

@router.get("/health")
def health():
    return {"ok": True, "module": "desk_pro", "mode": "step2_mock"}

@router.get("/snapshot", response_model=Snapshot)
def snapshot():
    t0 = time.time()
    snap = build_snapshot_mock()
    ms = int((time.time() - t0) * 1000)
    snap.meta["build_ms"] = str(ms)
    return snap

@router.post("/form", response_model=ScoreResult)
def form_score(form: DeskForm):
    snap = build_snapshot_mock()
    return compute_probability(form, snap)

@router.get("/ui", response_class=HTMLResponse)
def ui():
    return HTMLResponse(render_ui_html())

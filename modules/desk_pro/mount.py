from __future__ import annotations
from fastapi import FastAPI

def mount(app: FastAPI) -> None:
    """Mount Desk Pro router onto an existing FastAPI app."""
    from modules.desk_pro.api.routes import router as desk_router
    app.include_router(desk_router)

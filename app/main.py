from __future__ import annotations

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import BASE_DIR, STATIC_DIR, settings
from app.excel_store import save_consulta
from app.models import PROPIEDADES, SERVICIOS, ConsultaIn
from app.sheets import send_to_google_sheet

app = FastAPI(title="Nodos Inteligentes", docs_url=None, redoc_url=None)
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


def _whatsapp_links() -> dict[str, str]:
    base = "Hola, quiero solicitar un presupuesto de seguridad electrónica."
    links = {"general": settings.whatsapp_message_link(base)}
    for slug, label in SERVICIOS.items():
        links[slug] = settings.whatsapp_message_link(
            f"Hola, quiero consultar por el servicio de {label}."
        )
    return links


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "settings": settings,
            "whatsapp": _whatsapp_links(),
            "servicios": SERVICIOS,
            "propiedades": PROPIEDADES,
        },
    )


@app.get("/robots.txt")
async def robots():
    return FileResponse(STATIC_DIR / "robots.txt", media_type="text/plain")


@app.post("/api/consultas")
async def crear_consulta(payload: ConsultaIn):
    record = {
        "nombre": payload.nombre,
        "telefono": payload.telefono,
        "email": payload.email,
        "ciudad": payload.ciudad,
        "tipo_propiedad": PROPIEDADES[payload.tipo_propiedad],
        "servicio": SERVICIOS[payload.servicio],
        "mensaje": payload.mensaje,
        "origen": payload.origen,
    }
    save_consulta(record)

    try:
        await send_to_google_sheet(record)
    except Exception:
        pass

    if settings.n8n_webhook_url:
        try:
            async with httpx.AsyncClient(timeout=6.0) as client:
                await client.post(settings.n8n_webhook_url, json=record)
        except Exception:
            pass

    return JSONResponse(
        {
            "ok": True,
            "message": "Recibimos tu consulta. Te vamos a contactar a la brevedad.",
        }
    )


@app.get("/api/health")
async def health():
    return {"ok": True}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

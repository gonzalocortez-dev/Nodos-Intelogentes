from __future__ import annotations

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, field_validator

from app.config import BASE_DIR, STATIC_DIR, settings
from app.excel_store import save_consulta
from app.sheets import send_to_google_sheet

SERVICIOS = {
    "camaras-ip": "Cámaras IP",
    "camaras-analogicas": "Cámaras analógicas",
    "alarma-domiciliaria": "Alarma domiciliaria",
    "alarma-vecinal": "Alarma vecinal",
    "control-accesos": "Control de accesos",
    "cerco-electrico": "Cerco eléctrico",
    "redes-informaticas": "Redes informáticas",
    "starlink": "Starlink",
    "otro": "Otro",
}

PROPIEDADES = {
    "casa": "Casa",
    "departamento": "Departamento",
    "comercio": "Comercio",
    "empresa": "Empresa / oficina",
    "industria": "Industria",
    "barrio": "Barrio / consorcio",
    "otro": "Otro",
}

app = FastAPI(title="Nodos Inteligentes", docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


class ConsultaIn(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=120)
    telefono: str = Field(..., min_length=6, max_length=40)
    email: str = Field(..., min_length=5, max_length=160)
    ciudad: str = Field(..., min_length=2, max_length=120)
    tipo_propiedad: str
    servicio: str
    mensaje: str = Field("", max_length=2000)
    origen: str = Field("landing", max_length=40)

    @field_validator("nombre", "ciudad", "mensaje", mode="before")
    @classmethod
    def strip_text(cls, value: str) -> str:
        return value.strip() if isinstance(value, str) else value

    @field_validator("email")
    @classmethod
    def valid_email(cls, value: str) -> str:
        email = value.strip().lower()
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError("Email inválido")
        return email

    @field_validator("telefono")
    @classmethod
    def valid_phone(cls, value: str) -> str:
        digits = "".join(ch for ch in value if ch.isdigit())
        if len(digits) < 6:
            raise ValueError("Teléfono inválido")
        return value.strip()

    @field_validator("servicio")
    @classmethod
    def valid_servicio(cls, value: str) -> str:
        if value not in SERVICIOS:
            raise ValueError("Servicio inválido")
        return value

    @field_validator("tipo_propiedad")
    @classmethod
    def valid_propiedad(cls, value: str) -> str:
        if value not in PROPIEDADES:
            raise ValueError("Tipo de propiedad inválido")
        return value


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

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.excel_store import save_consulta
from app.models import PROPIEDADES, SERVICIOS, ConsultaIn
from app.sheets import send_to_google_sheet

app = FastAPI(title="Nodos Inteligentes API", docs_url=None, redoc_url=None)


async def guardar_consulta(payload: ConsultaIn):
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
    return JSONResponse(
        {
            "ok": True,
            "message": "Recibimos tu consulta. Te vamos a contactar a la brevedad.",
        }
    )


@app.post("/")
@app.post("/api/consultas")
@app.post("/consultas")
async def crear_consulta(payload: ConsultaIn):
    return await guardar_consulta(payload)

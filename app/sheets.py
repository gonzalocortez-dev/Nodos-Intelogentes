from __future__ import annotations

import json
from datetime import datetime
from zoneinfo import ZoneInfo

import httpx

from app.config import settings

HEADERS = [
    "Fecha",
    "Nombre",
    "Teléfono / WhatsApp",
    "Email",
    "Ciudad / localidad",
    "Tipo de propiedad",
    "Servicio de interés",
    "Mensaje",
    "Origen",
]


def _row(record: dict) -> list[str]:
    try:
        fecha = datetime.now(ZoneInfo("America/Argentina/Buenos_Aires")).strftime("%Y-%m-%d %H:%M")
    except Exception:
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    return [
        fecha,
        record.get("nombre", ""),
        record.get("telefono", ""),
        record.get("email", ""),
        record.get("ciudad", ""),
        record.get("tipo_propiedad", ""),
        record.get("servicio", ""),
        record.get("mensaje", ""),
        record.get("origen", "landing"),
    ]


async def send_to_google_sheet(record: dict) -> None:
    url = (settings.google_sheets_webhook_url or "").strip()
    if not url:
        return

    payload = dict(zip(HEADERS, _row(record)))
    body = json.dumps(payload, ensure_ascii=False)
    headers = {"Content-Type": "application/json; charset=utf-8"}

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(url, content=body, headers=headers, follow_redirects=False)
        if response.status_code in {301, 302, 303, 307, 308}:
            location = response.headers.get("location")
            if location:
                await client.post(location, content=body, headers=headers, follow_redirects=True)

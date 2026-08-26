from __future__ import annotations

import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = Path("/tmp/nodos-inteligentes") if os.getenv("VERCEL") else BASE_DIR / "data"
EXCEL_PATH = DATA_DIR / "consultas.xlsx"
STATIC_DIR = BASE_DIR / "public" / "static"
if not STATIC_DIR.exists():
    STATIC_DIR = BASE_DIR / "static"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    company_name: str = "Nodos Inteligentes"
    company_full_name: str = "Conectividad & Seguridad Avanzada"
    tagline: str = "Conectividad & Seguridad Avanzada"
    whatsapp_number: str = "5493872192323"
    phone: str = "+54 387 219-2323"
    email: str = "contacto@nodosinteligentes.com"
    instagram_url: str = "https://instagram.com/nodosinteligentes"
    instagram_handle: str = "@nodosinteligentes"
    location: str = "Salta, Capital"
    site_url: str = "http://127.0.0.1:8000"
    n8n_webhook_url: str = ""
    google_sheets_webhook_url: str = ""

    @property
    def canonical_url(self) -> str:
        if self.site_url and "127.0.0.1" not in self.site_url:
            return self.site_url.rstrip("/")
        vercel_url = os.getenv("VERCEL_PROJECT_PRODUCTION_URL") or os.getenv("VERCEL_URL")
        if vercel_url:
            host = vercel_url.replace("https://", "").replace("http://", "")
            return f"https://{host}"
        return self.site_url.rstrip("/")

    @property
    def whatsapp_link(self) -> str:
        digits = "".join(ch for ch in self.whatsapp_number if ch.isdigit())
        return f"https://wa.me/{digits}"

    def whatsapp_message_link(self, message: str) -> str:
        from urllib.parse import quote

        digits = "".join(ch for ch in self.whatsapp_number if ch.isdigit())
        return f"https://wa.me/{digits}?text={quote(message)}"


settings = Settings()

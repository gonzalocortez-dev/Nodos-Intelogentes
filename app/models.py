from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

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

# Nodos Inteligentes

Landing de seguridad electrónica y redes. Backend en FastAPI; las consultas se guardan en Excel en local.

## Correr en local

```powershell
.\run.ps1
```

Queda en http://127.0.0.1:8000

## Desplegar en Vercel

1. Entrá a [vercel.com/new](https://vercel.com/new)
2. Importá el repo `gonzalocortez-dev/Nodos-Intelogentes`
3. Framework: **FastAPI** (si no lo detecta solo)
4. Root Directory: dejar vacío (la raíz del repo)
5. Cargá estas variables de entorno:

| Variable | Valor |
| --- | --- |
| `WHATSAPP_NUMBER` | `5493872192323` |
| `PHONE` | `+54 387 219-2323` |
| `EMAIL` | `contacto@nodosinteligentes.com` |
| `LOCATION` | `Salta, Capital` |
| `SITE_URL` | la URL de Vercel, por ejemplo `https://nodos-inteligentes.vercel.app` |

6. Deploy

En Vercel el Excel no se conserva entre visitas (el disco es temporal). Para guardar leads de forma permanente, completá `N8N_WEBHOOK_URL` y conectalo a Google Sheets, un CRM o un correo.

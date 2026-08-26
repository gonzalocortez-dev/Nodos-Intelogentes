# Nodos Inteligentes

Landing de seguridad electrónica y redes. Backend en FastAPI.

- En local, las consultas también se guardan en Excel.
- En Vercel, las consultas se guardan en **Google Sheets**.

## Correr en local

```powershell
.\run.ps1
```

Queda en http://127.0.0.1:8000

## Conectar Google Sheets

1. Creá una hoja en [Google Sheets](https://sheets.google.com) (por ejemplo `Consultas Nodos Inteligentes`).
2. Menú **Extensiones → Apps Script**.
3. Borrá el código que aparece y pegá el de `scripts/google-sheet-apps-script.gs`.
4. Guardá el proyecto.
5. Arriba a la derecha: **Implementar → Nueva implementación**.
6. Tipo: **Aplicación web**.
7. Descripción: `consultas`.
8. Ejecutar como: **Yo**.
9. Quién tiene acceso: **Cualquier usuario**.
10. Implementar, autorizar con tu cuenta de Google y **copiá la URL**.
11. Pegá esa URL en:
    - local: `GOOGLE_SHEETS_WEBHOOK_URL` dentro de `.env`
    - Vercel: Settings → Environment Variables → `GOOGLE_SHEETS_WEBHOOK_URL`

Cada envío del formulario agrega una fila en la pestaña **Consultas**.

## Desplegar en Vercel

1. Entrá a [vercel.com/new](https://vercel.com/new)
2. Importá el repo `gonzalocortez-dev/Nodos-Intelogentes`
3. Framework Preset: **FastAPI** (en Project Settings → General, si no lo detecta solo)
4. Root Directory: dejar vacío
5. Cargá estas variables de entorno:

| Variable | Valor |
| --- | --- |
| `WHATSAPP_NUMBER` | `5493872192323` |
| `PHONE` | `+54 387 219-2323` |
| `EMAIL` | `contacto@nodosinteligentes.com` |
| `LOCATION` | `Salta, Capital` |
| `GOOGLE_SHEETS_WEBHOOK_URL` | la URL de Apps Script |
| `SITE_URL` | la URL de Vercel |

6. Deploy

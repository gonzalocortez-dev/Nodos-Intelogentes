from fastapi import FastAPI

app = FastAPI(docs_url=None, redoc_url=None)


@app.get("/")
@app.get("/api")
def health():
    return {"ok": True, "service": "nodos-inteligentes"}

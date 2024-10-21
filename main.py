from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

# Configuración para servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory=".")

# Lista de comentarios en memoria
comentarios = ["La importancia de la ciberseguridad es vital hoy en día", "Necesitamos mejores políticas de seguridad"]

@app.get("/", response_class=HTMLResponse)
async def leer_comentarios(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "comentarios": comentarios})

@app.post("/agregar")
async def agregar_comentario(comentario: str):
    comentarios.append(comentario)
    return {"comentarios": comentarios}

@app.get("/comentarios-json")
async def comentarios_json():
    return {"comentarios": comentarios}

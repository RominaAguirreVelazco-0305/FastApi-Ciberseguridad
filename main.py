from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, constr

app = FastAPI()

# Configuración para servir archivos estáticos y plantillas
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Esto debe ser más específico en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lista de comentarios en memoria
comentarios = [
    "La importancia de la ciberseguridad es vital hoy en día",
    "Necesitamos mejores políticas de seguridad"
]

class Comentario(BaseModel):
    comentario: constr(strip_whitespace=True, min_length=1)

@app.get("/", response_class=HTMLResponse)
async def leer_comentarios(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "comentarios": comentarios})

@app.post("/agregar")
async def agregar_comentario(comentario: str = Form(...)):
    if not comentario.strip():  # Verifica que el comentario no esté vacío después de quitar espacios
        raise HTTPException(status_code=400, detail="El comentario no puede estar vacío")
    comentarios.append(comentario)
    return RedirectResponse(url="/", status_code=303)

@app.get("/comentarios-json")
async def comentarios_json():
    return {"comentarios": comentarios}


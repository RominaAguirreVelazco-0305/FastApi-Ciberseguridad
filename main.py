from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Configuración de CORS para permitir solicitudes desde otros dominios
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajusta esto para producción a dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración para servir archivos estáticos y plantillas
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Lista de comentarios en memoria (simulación de una base de datos en memoria)
comentarios = [
    "La importancia de la ciberseguridad es vital hoy en día", 
    "Necesitamos mejores políticas de seguridad"
]

class Comentario(BaseModel):
    comentario: str

@app.get("/", response_class=HTMLResponse)
async def leer_comentarios(request: Request):
    # Renderiza la plantilla HTML y pasa la lista de comentarios
    return templates.TemplateResponse("index.html", {"request": request, "comentarios": comentarios})

# Endpoint para agregar comentarios usando Form data
@app.post("/agregar")
async def agregar_comentario(comentario: str = Form(...)):
    # Validar comentario vacío
    if not comentario.strip():
        raise HTTPException(status_code=400, detail="El comentario no puede estar vacío")
    
    comentarios.append(comentario)
    # Redirige al usuario de vuelta a la página principal tras agregar un comentario
    return RedirectResponse(url="/", status_code=303)

# Endpoint para agregar comentarios con JSON
@app.post("/agregar-json")
async def agregar_comentario_json(comentario: Comentario):
    if not comentario.comentario.strip():
        raise HTTPException(status_code=400, detail="El comentario no puede estar vacío")
    
    comentarios.append(comentario.comentario)
    return {"comentarios": comentarios}

# Endpoint para devolver los comentarios en formato JSON
@app.get("/comentarios-json")
async def comentarios_json():
    return {"comentarios": comentarios}

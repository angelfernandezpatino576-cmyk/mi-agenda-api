import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "tareas_db.json"

# Función para leer datos del archivo
def cargar_datos():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        return json.load(f)

# Función para guardar datos en el archivo
def guardar_datos(datos):
    with open(DB_FILE, "w") as f:
        json.dump(datos, f, indent=4)

class Tarea(BaseModel):
    titulo: str
    fecha_limite: str # Usamos str para simplificar el JSON
    estado: str = "pendiente"

@app.get("/")
def home():
    return {"status": "Online", "modo": "Gratuito Persistente"}

@app.post("/tareas/")
def agregar_tarea(tarea: Tarea):
    tareas = cargar_datos()
    tareas.append(tarea.dict())
    guardar_datos(tareas)
    return {"mensaje": "Guardado exitosamente"}

@app.get("/tareas/")
def listar_tareas():
    return cargar_datos()
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Servidor Agente 2026 Online"}

@app.get("/tareas/")
def leer_tareas():
    return [{"id": 1, "titulo": "Conexión exitosa con Koyeb", "estado": "ok"}]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

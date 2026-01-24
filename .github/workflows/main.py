from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Agente IA 2026 Online", "servidor": "Koyeb"}

@app.get("/tareas/")
def leer_tareas():
    # Esto es para que la URL que usa tu APK no de error 404
    return [{"id": 1, "titulo": "Servidor activo", "estado": "ok"}]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

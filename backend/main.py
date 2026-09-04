from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import personal, pacientes, asignaciones, usuarios


app = FastAPI(
    title="API Clínica Los Olivos",
    description="API para la gestión de personal y pacientes de la Clínica Los Olivos",
    version="1.0.0"
)


# ==========================================
# CONFIGURACIÓN CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5000",
        "http://localhost:5000",
        "http://192.168.0.252:5000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# RUTAS
# ==========================================

app.include_router(personal.router)

app.include_router(pacientes.router)

app.include_router(asignaciones.router)

app.include_router(usuarios.router)


# ==========================================
# RUTA PRINCIPAL
# ==========================================

@app.get("/")
def inicio():
    return {
        "mensaje": "API de Clínica Los Olivos funcionando correctamente"
    }
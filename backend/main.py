from fastapi import FastAPI

from routers import personal, pacientes


app = FastAPI(
    title="API Clínica Los Olivos",
    description="API para la gestión de personal y pacientes de la Clínica Los Olivos",
    version="1.0.0"
)


# Registrar las rutas de personal
app.include_router(personal.router)

# Registrar las rutas de pacientes
app.include_router(pacientes.router)


@app.get("/")
def inicio():
    return {
        "mensaje": "API de Clínica Los Olivos funcionando correctamente"
    }
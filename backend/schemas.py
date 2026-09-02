from datetime import date
from pydantic import BaseModel


class PersonalCreate(BaseModel):
    nombre: str
    apellido_paterno: str
    apellido_materno: str | None = None
    fecha_nacimiento: date | None = None
    tipo: str
    especialidad: str | None = None
    telefono: str | None = None


class PersonalResponse(BaseModel):
    id: int
    nombre: str
    apellido_paterno: str
    apellido_materno: str | None = None
    fecha_nacimiento: date | None = None
    tipo: str
    especialidad: str | None = None
    telefono: str | None = None

    class Config:
        from_attributes = True


# PACIENTES
class PacienteCreate(BaseModel):
    nombre: str
    apellido_paterno: str
    apellido_materno: str | None = None
    fecha_nacimiento: date | None = None
    telefono: str | None = None
    diagnostico: str | None = None
    estatus: str = "Estable"


class PacienteResponse(BaseModel):
    id: int
    nombre: str
    apellido_paterno: str
    apellido_materno: str | None = None
    fecha_nacimiento: date | None = None
    telefono: str | None = None
    diagnostico: str | None = None
    estatus: str

    class Config:
        from_attributes = True
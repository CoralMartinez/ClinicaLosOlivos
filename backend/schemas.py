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
        
# ASIGNACIONES

class AsignacionCreate(BaseModel):
    paciente_id: int
    personal_id: int
    fecha_asignacion: date
    observaciones: str | None = None


class AsignacionResponse(BaseModel):
    id: int
    paciente_id: int
    personal_id: int
    fecha_asignacion: date
    observaciones: str | None = None

    class Config:
        from_attributes = True
        
        
# USUARIOS

class UsuarioCreate(BaseModel):
    usuario: str
    password: str
    rol: str
    personal_id: int | None = None


class UsuarioResponse(BaseModel):
    id: int
    usuario: str
    rol: str
    personal_id: int | None = None

    class Config:
        from_attributes = True
        
# LOGIN

class LoginRequest(BaseModel):
    usuario: str
    password: str
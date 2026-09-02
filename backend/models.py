from sqlalchemy import Column, Integer, String, Date, ForeignKey
from database import Base

#Estructura que tendrá PostgreSQL
# PERSONAL

class Personal(Base):
    __tablename__ = "personal"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido_paterno = Column(String(100), nullable=False)
    apellido_materno = Column(String(100), nullable=True)
    fecha_nacimiento = Column(Date, nullable=True)
    tipo = Column(String(20), nullable=False)
    especialidad = Column(String(100), nullable=True)
    telefono = Column(String(20), nullable=True)


# USUARIOS

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    rol = Column(String(20), nullable=False)
    personal_id = Column(
        Integer,
        ForeignKey("personal.id"),
        nullable=True
    )

# PACIENTES

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido_paterno = Column(String(100), nullable=False)
    apellido_materno = Column(String(100), nullable=True)
    fecha_nacimiento = Column(Date, nullable=True)
    telefono = Column(String(20), nullable=True)
    diagnostico = Column(String(255), nullable=True)
    estatus = Column(
        String(50),
        nullable=False,
        default="Estable"
    )


# ASIGNACIONES

class Asignacion(Base):
    __tablename__ = "asignaciones"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(
        Integer,
        ForeignKey("pacientes.id"),
        nullable=False
    )
    personal_id = Column(
        Integer,
        ForeignKey("personal.id"),
        nullable=False
    )
    fecha_asignacion = Column(Date, nullable=False)
    observaciones = Column(String(255), nullable=True)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Paciente
from schemas import PacienteCreate, PacienteResponse


router = APIRouter(
    prefix="/pacientes",
    tags=["Pacientes"]
)


# CONEXIÓN A LA BD
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# CONSULTAR TODOS 
@router.get("/", response_model=list[PacienteResponse])
def obtener_pacientes(
    db: Session = Depends(get_db)
):

    pacientes = db.query(Paciente).all()

    return pacientes


# CONSULTAR POR ID
@router.get("/{paciente_id}", response_model=PacienteResponse)
def obtener_paciente_por_id(
    paciente_id: int,
    db: Session = Depends(get_db)
):

    paciente = db.query(Paciente).filter(
        Paciente.id == paciente_id
    ).first()

    if not paciente:
        raise HTTPException(
            status_code=404,
            detail="Paciente no encontrado"
        )

    return paciente


# REGISTRAR/CREAR
@router.post("/", response_model=PacienteResponse)
def crear_paciente(
    datos: PacienteCreate,
    db: Session = Depends(get_db)
):

    nuevo_paciente = Paciente(
        nombre=datos.nombre,
        apellido_paterno=datos.apellido_paterno,
        apellido_materno=datos.apellido_materno,
        fecha_nacimiento=datos.fecha_nacimiento,
        telefono=datos.telefono,
        diagnostico=datos.diagnostico,
        estatus=datos.estatus
    )

    db.add(nuevo_paciente)
    db.commit()
    db.refresh(nuevo_paciente)

    return nuevo_paciente


# MODIFICAR 

@router.put("/{paciente_id}", response_model=PacienteResponse)
def modificar_paciente(
    paciente_id: int,
    datos: PacienteCreate,
    db: Session = Depends(get_db)
):

    paciente = db.query(Paciente).filter(
        Paciente.id == paciente_id
    ).first()

    if not paciente:
        raise HTTPException(
            status_code=404,
            detail="Paciente no encontrado"
        )

    paciente.nombre = datos.nombre
    paciente.apellido_paterno = datos.apellido_paterno
    paciente.apellido_materno = datos.apellido_materno
    paciente.fecha_nacimiento = datos.fecha_nacimiento
    paciente.telefono = datos.telefono
    paciente.diagnostico = datos.diagnostico
    paciente.estatus = datos.estatus

    db.commit()
    db.refresh(paciente)

    return paciente


# ELIMINAR 
@router.delete("/{paciente_id}")
def eliminar_paciente(
    paciente_id: int,
    db: Session = Depends(get_db)
):

    paciente = db.query(Paciente).filter(
        Paciente.id == paciente_id
    ).first()

    if not paciente:
        raise HTTPException(
            status_code=404,
            detail="Paciente no encontrado"
        )

    db.delete(paciente)
    db.commit()

    return {
        "mensaje": "Paciente eliminado correctamente"
    }
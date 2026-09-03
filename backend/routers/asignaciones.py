from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Asignacion, Paciente, Personal
from schemas import AsignacionCreate, AsignacionResponse

from auth import get_current_user, verificar_rol


router = APIRouter(
    prefix="/asignaciones",
    tags=["Asignaciones"]
)

# CONEXIÓN A LA BD

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# CONSULTAR TODAS

@router.get("/", response_model=list[AsignacionResponse])
def obtener_asignaciones(
    db: Session = Depends(get_db),
    usuario_actual=Depends(get_current_user)
):

    asignaciones = db.query(Asignacion).all()

    return asignaciones

# CONSULTAR POR ID

@router.get("/{asignacion_id}", response_model=AsignacionResponse)
def obtener_asignacion_por_id(
    asignacion_id: int,
    db: Session = Depends(get_db),
    usuario_actual=Depends(get_current_user)
):

    asignacion = db.query(Asignacion).filter(
        Asignacion.id == asignacion_id
    ).first()

    if not asignacion:
        raise HTTPException(
            status_code=404,
            detail="Asignación no encontrada"
        )

    return asignacion

# CREAR 

@router.post("/", response_model=AsignacionResponse)
def crear_asignacion(
    datos: AsignacionCreate,
    db: Session = Depends(get_db),
    usuario_actual=Depends(
        verificar_rol(["Admin", "Doctor", "Enfermero"])
    )
):

    # Comprobar que exista el paciente
    paciente = db.query(Paciente).filter(
        Paciente.id == datos.paciente_id
    ).first()

    if not paciente:
        raise HTTPException(
            status_code=404,
            detail="Paciente no encontrado"
        )

    # Comprobar que exista el personal
    personal = db.query(Personal).filter(
        Personal.id == datos.personal_id
    ).first()

    if not personal:
        raise HTTPException(
            status_code=404,
            detail="Personal no encontrado"
        )

    nueva_asignacion = Asignacion(
        paciente_id=datos.paciente_id,
        personal_id=datos.personal_id,
        fecha_asignacion=datos.fecha_asignacion,
        observaciones=datos.observaciones
    )

    db.add(nueva_asignacion)
    db.commit()
    db.refresh(nueva_asignacion)

    return nueva_asignacion

# MODIFICAR (ADMIN Y DOCTOR)

@router.put(
    "/{asignacion_id}",
    response_model=AsignacionResponse
)
def modificar_asignacion(
    asignacion_id: int,
    datos: AsignacionCreate,
    db: Session = Depends(get_db),
    usuario_actual=Depends(
        verificar_rol(["Admin", "Doctor"])
    )
):

    asignacion = db.query(Asignacion).filter(
        Asignacion.id == asignacion_id
    ).first()

    if not asignacion:
        raise HTTPException(
            status_code=404,
            detail="Asignación no encontrada"
        )

    # Comprobar que exista el paciente
    paciente = db.query(Paciente).filter(
        Paciente.id == datos.paciente_id
    ).first()

    if not paciente:
        raise HTTPException(
            status_code=404,
            detail="Paciente no encontrado"
        )

    # Comprobar que exista el personal
    personal = db.query(Personal).filter(
        Personal.id == datos.personal_id
    ).first()

    if not personal:
        raise HTTPException(
            status_code=404,
            detail="Personal no encontrado"
        )

    asignacion.paciente_id = datos.paciente_id
    asignacion.personal_id = datos.personal_id
    asignacion.fecha_asignacion = datos.fecha_asignacion
    asignacion.observaciones = datos.observaciones

    db.commit()
    db.refresh(asignacion)

    return asignacion


# ELIMINAR (SOLO ADMIN)

@router.delete("/{asignacion_id}")
def eliminar_asignacion(
    asignacion_id: int,
    db: Session = Depends(get_db),
    usuario_actual=Depends(
        verificar_rol(["Admin"])
    )
):

    asignacion = db.query(Asignacion).filter(
        Asignacion.id == asignacion_id
    ).first()

    if not asignacion:
        raise HTTPException(
            status_code=404,
            detail="Asignación no encontrada"
        )

    db.delete(asignacion)
    db.commit()

    return {
        "mensaje": "Asignación eliminada correctamente"
    }
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Personal
from schemas import PersonalCreate, PersonalResponse

from auth import get_current_user, verificar_rol


router = APIRouter(
    prefix="/personal",
    tags=["Personal"]
)


# ==========================================
# CONEXIÓN A LA BD
# ==========================================

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# ==========================================
# CONSULTAR TODOS
# ADMIN, DOCTOR Y ENFERMERO
# ==========================================

@router.get("/", response_model=list[PersonalResponse])
def obtener_personal(
    db: Session = Depends(get_db),
    usuario_actual=Depends(get_current_user)
):

    personal = db.query(Personal).all()

    return personal


# ==========================================
# CONSULTAR POR ID
# ADMIN, DOCTOR Y ENFERMERO
# ==========================================

@router.get("/{personal_id}", response_model=PersonalResponse)
def obtener_personal_por_id(
    personal_id: int,
    db: Session = Depends(get_db),
    usuario_actual=Depends(get_current_user)
):

    personal = db.query(Personal).filter(
        Personal.id == personal_id
    ).first()

    if not personal:
        raise HTTPException(
            status_code=404,
            detail="Personal no encontrado"
        )

    return personal


# ==========================================
# REGISTRAR
# SOLO ADMIN
# ==========================================

@router.post("/", response_model=PersonalResponse)
def crear_personal(
    datos: PersonalCreate,
    db: Session = Depends(get_db),
    usuario_actual=Depends(verificar_rol(["Admin"]))
):

    nuevo_personal = Personal(
        nombre=datos.nombre,
        apellido_paterno=datos.apellido_paterno,
        apellido_materno=datos.apellido_materno,
        fecha_nacimiento=datos.fecha_nacimiento,
        tipo=datos.tipo,
        especialidad=datos.especialidad,
        telefono=datos.telefono
    )

    db.add(nuevo_personal)
    db.commit()
    db.refresh(nuevo_personal)

    return nuevo_personal


# ==========================================
# MODIFICAR
# SOLO ADMIN
# ==========================================

@router.put("/{personal_id}", response_model=PersonalResponse)
def modificar_personal(
    personal_id: int,
    datos: PersonalCreate,
    db: Session = Depends(get_db),
    usuario_actual=Depends(verificar_rol(["Admin"]))
):

    personal = db.query(Personal).filter(
        Personal.id == personal_id
    ).first()

    if not personal:
        raise HTTPException(
            status_code=404,
            detail="Personal no encontrado"
        )

    personal.nombre = datos.nombre
    personal.apellido_paterno = datos.apellido_paterno
    personal.apellido_materno = datos.apellido_materno
    personal.fecha_nacimiento = datos.fecha_nacimiento
    personal.tipo = datos.tipo
    personal.especialidad = datos.especialidad
    personal.telefono = datos.telefono

    db.commit()
    db.refresh(personal)

    return personal


# ==========================================
# ELIMINAR
# SOLO ADMIN
# ==========================================

@router.delete("/{personal_id}")
def eliminar_personal(
    personal_id: int,
    db: Session = Depends(get_db),
    usuario_actual=Depends(verificar_rol(["Admin"]))
):

    personal = db.query(Personal).filter(
        Personal.id == personal_id
    ).first()

    if not personal:
        raise HTTPException(
            status_code=404,
            detail="Personal no encontrado"
        )

    db.delete(personal)
    db.commit()

    return {
        "mensaje": "Personal eliminado correctamente"
    }
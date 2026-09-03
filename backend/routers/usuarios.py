from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Usuario
from schemas import (
    UsuarioCreate,
    UsuarioResponse,
    LoginRequest
)

from pwdlib import PasswordHash
from security import crear_token
from auth import get_current_user, verificar_rol

# CONFIGURACIÓN DE CONTRASEÑAS

password_hash = PasswordHash.recommended()

# CONFIGURACIÓN DEL ROUTER

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

# CONEXIÓN A LA BD

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# CONSULTAR TODOS (SOLO ADMIN)

@router.get(
    "/",
    response_model=list[UsuarioResponse]
)
def obtener_usuarios(
    db: Session = Depends(get_db),
    usuario_actual=Depends(verificar_rol(["Admin"]))
):

    usuarios = db.query(Usuario).order_by(
        Usuario.id.asc()
    ).all()

    return usuarios

# LOGIN

@router.post("/login")
def login(
    datos: LoginRequest,
    db: Session = Depends(get_db)
):

    # Buscar usuario
    usuario = db.query(Usuario).filter(
        Usuario.usuario == datos.usuario
    ).first()

    # Comprobar que exista
    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrectos"
        )

    # Comprobar contraseña
    contraseña_correcta = password_hash.verify(
        datos.password,
        usuario.password
    )

    if not contraseña_correcta:
        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrectos"
        )

    # Crear token JWT
    token = crear_token({
        "usuario_id": usuario.id,
        "usuario": usuario.usuario,
        "rol": usuario.rol
    })

    return {
        "mensaje": "Login correcto",
        "access_token": token,
        "token_type": "bearer",
        "usuario_id": usuario.id,
        "usuario": usuario.usuario,
        "rol": usuario.rol,
        "personal_id": usuario.personal_id
    }

# CONSULTAR USUARIO (SOLO ADMIN)

@router.get(
    "/{usuario_id}",
    response_model=UsuarioResponse
)
def obtener_usuario_por_id(
    usuario_id: int,
    db: Session = Depends(get_db),
    usuario_actual=Depends(verificar_rol(["Admin"]))
):

    usuario = db.query(Usuario).filter(
        Usuario.id == usuario_id
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return usuario

# REGISTRAR / CREAR (SOLO ADMIN)

@router.post(
    "/",
    response_model=UsuarioResponse
)
def crear_usuario(
    datos: UsuarioCreate,
    db: Session = Depends(get_db),
    usuario_actual=Depends(verificar_rol(["Admin"]))
):

    # Comprobar si ya existe
    usuario_existente = db.query(Usuario).filter(
        Usuario.usuario == datos.usuario
    ).first()

    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="El nombre de usuario ya existe"
        )

    # Encriptar contraseña
    password_encriptada = password_hash.hash(
        datos.password
    )

    # Crear usuario
    nuevo_usuario = Usuario(
        usuario=datos.usuario,
        password=password_encriptada,
        rol=datos.rol,
        personal_id=datos.personal_id
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario

# MODIFICAR (SOLO ADMIN)

@router.put(
    "/{usuario_id}",
    response_model=UsuarioResponse
)
def modificar_usuario(
    usuario_id: int,
    datos: UsuarioCreate,
    db: Session = Depends(get_db),
    usuario_actual=Depends(verificar_rol(["Admin"]))
):

    # Buscar usuario
    usuario = db.query(Usuario).filter(
        Usuario.id == usuario_id
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    # Comprobar nombre de usuario duplicado
    usuario_existente = db.query(Usuario).filter(
        Usuario.usuario == datos.usuario,
        Usuario.id != usuario_id
    ).first()

    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="El nombre de usuario ya existe"
        )

    # Actualizar datos
    usuario.usuario = datos.usuario

    # Encriptar nueva contraseña
    usuario.password = password_hash.hash(
        datos.password
    )

    usuario.rol = datos.rol
    usuario.personal_id = datos.personal_id

    db.commit()
    db.refresh(usuario)

    return usuario

# ELIMINAR (SOLO ADMIN)

@router.delete("/{usuario_id}")
def eliminar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    usuario_actual=Depends(verificar_rol(["Admin"]))
):

    # Buscar usuario
    usuario = db.query(Usuario).filter(
        Usuario.id == usuario_id
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    # Eliminar
    db.delete(usuario)
    db.commit()

    return {
        "mensaje": "Usuario eliminado correctamente"
    }
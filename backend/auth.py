from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Usuario
from security import SECRET_KEY, ALGORITHM


# CONFIGURACIÓN DEL TOKEN
security = HTTPBearer()


# CONEXIÓN A LA BD

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# OBTENER USUARIO ACTUAL

def get_current_user(
    credenciales: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credenciales.credentials

    try:

        # Decodificar el token
        datos = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # Obtener ID del usuario
        usuario_id = datos.get("usuario_id")

        if usuario_id is None:
            raise HTTPException(
                status_code=401,
                detail="Token inválido"
            )

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Token inválido o expirado"
        )

    # Buscar usuario en la BD
    usuario = db.query(Usuario).filter(
        Usuario.id == usuario_id
    ).first()

    if not usuario:

        raise HTTPException(
            status_code=401,
            detail="Usuario no encontrado"
        )

    return usuario


# VERIFICAR ROL

def verificar_rol(roles_permitidos: list[str]):

    def verificar(usuario_actual=Depends(get_current_user)):

        if usuario_actual.rol not in roles_permitidos:
            raise HTTPException(
                status_code=403,
                detail="No tienes permisos para realizar esta acción"
            )

        return usuario_actual

    return verificar
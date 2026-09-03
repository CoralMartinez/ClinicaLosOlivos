from datetime import datetime, timedelta, timezone
from jose import jwt


# CONFIGURACIÓN DE JW

SECRET_KEY = "clinica_los_olivos_clave_secreta_2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# CREAR TOKEN

def crear_token(datos: dict):

    datos_token = datos.copy()

    fecha_expiracion = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    datos_token.update({
        "exp": fecha_expiracion
    })

    token = jwt.encode(
        datos_token,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token
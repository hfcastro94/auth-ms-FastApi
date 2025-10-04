from pydantic import BaseModel
from typing import Optional

class SystemUser(BaseModel):
    e_mail: str                  # PK en la tabla auth_ms_usuario
    hashed_password: str
    salt: Optional[str] = ""      # opcional, ya no lo usas
    type_user: str                # por defecto 'basic'
    state: bool = True            # por defecto activo
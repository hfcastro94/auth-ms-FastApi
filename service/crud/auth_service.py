import uuid
import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

from domain.models.system_user import SystemUser
from domain.models.jwt_token import Token
from repository.auth_repository import AuthRepository
from configuration.database import get_dynamo_client

# Configuración del token
SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    @staticmethod
    def register(e_mail: str, password: str, type_user: str = "basic"):
        """Registra un nuevo usuario y lo asocia a su tipo en auth_ms_type_user"""
        repo = AuthRepository(get_dynamo_client())

        # Verificar si ya existe el usuario
        existing_user = repo.get_user_by_email(e_mail)
        if existing_user:
            print("⚠️ El usuario ya existe")
            return None

        # Crear el usuario en auth_ms_usuario
        hashed = pwd_context.hash(password)
        user = SystemUser(
            e_mail=e_mail,
            hashed_password=hashed,
            salt='',
            type_user=type_user,
            state=True
        )
        repo.create_user(user)

        # Asociar el correo al tipo de usuario en auth_ms_type_user
        repo.add_email_to_type_user(type_user, e_mail)

        return user

    @staticmethod
    def login(e_mail: str, password: str) -> str | None:
        """Verifica credenciales y genera un token JWT"""
        repo = AuthRepository(get_dynamo_client())
        user = repo.get_user_by_email(e_mail)

        if not user or not user.state:
            return None

        if not pwd_context.verify(password, user.hashed_password):
            return None

        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {"sub": user.e_mail, "exp": expire, "type_user": user.type_user}

        # Crear JWT
        jwt_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        # Guardar token en DynamoDB
        repo.create_token(
            Token(
                token=jwt_token,
                e_mail=user.e_mail,
                created_at=datetime.utcnow()
            )
        )
        return jwt_token

    @staticmethod
    def verify_token(token: str) -> bool | None:
        """Valida un token JWT y retorna el email del usuario si es válido"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return True
        except jwt.ExpiredSignatureError:
            print("⛔ Token expirado")
            return False
        except jwt.InvalidTokenError:
            print("❌ Token inválido")
            return False

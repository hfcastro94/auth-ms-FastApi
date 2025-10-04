import boto3
from domain.models.system_user import SystemUser
from domain.models.jwt_token import Token
from boto3.dynamodb.conditions import Attr


class AuthRepository:
    def __init__(self, dynamo_client):
        self.dynamo = dynamo_client
        self.user_table = self.dynamo.Table("auth_ms_usuario")
        self.token_table = self.dynamo.Table("auth_ms_jwt")
        self.type_user_table = self.dynamo.Table("auth_ms_type_user")

    # ---------------- USERS ----------------
    def create_user(self, user: SystemUser) -> SystemUser:
        """Crea un nuevo usuario en la tabla auth_ms_usuario"""
        self.user_table.put_item(Item=user.dict())
        return user

    def get_user_by_email(self, e_mail: str) -> SystemUser | None:
        """Obtiene un usuario por su e_mail"""
        response = self.user_table.get_item(Key={"e_mail": e_mail})
        item = response.get("Item")
        return SystemUser(**item) if item else None

    # ---------------- TOKENS ----------------
    def create_token(self, token: Token) -> Token:
        """Guarda un token JWT"""
        self.token_table.put_item(Item={
            "token": token.token,
            "e_mail": token.e_mail,
            "created_at": token.created_at.isoformat()
        })
        return token

    def get_token(self, token_value: str) -> Token | None:
        """Obtiene un token por su valor"""
        response = self.token_table.get_item(Key={"token": token_value})
        item = response.get("Item")
        return Token(**item) if item else None

    # ---------------- TYPE USERS ----------------
    def get_type_user(self, type_user: str):
        """Obtiene un tipo de usuario por su clave primaria"""
        response = self.type_user_table.get_item(Key={"type_user": type_user})
        return response.get("Item")

    def create_type_user(self, type_user: str, e_mail: str):
        """Crea un nuevo tipo de usuario con su primer correo"""
        item = {
            "type_user": type_user,
            "emails": [e_mail]
        }
        self.type_user_table.put_item(Item=item)
        return item

    def add_email_to_type_user(self, type_user: str, e_mail: str):
        """Agrega un correo al tipo de usuario, o crea el tipo si no existe"""
        existing = self.get_type_user(type_user)

        if not existing:
            # Si el tipo no existe, se crea con este correo
            return self.create_type_user(type_user, e_mail)

        # Si existe, agregar el correo si no está
        emails = existing.get("emails", [])
        if e_mail not in emails:
            emails.append(e_mail)
            self.type_user_table.update_item(
                Key={"type_user": type_user},
                UpdateExpression="SET emails = :emails",
                ExpressionAttributeValues={":emails": emails}
            )
        return {"type_user": type_user, "emails": emails}

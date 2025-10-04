from pydantic import BaseModel

class TypeUser(BaseModel):
    type_user: str      # PK en Dynamo
    description: str

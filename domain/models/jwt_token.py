from pydantic import BaseModel
from datetime import datetime

class Token(BaseModel):
    token: str   # antes era jwt_token
    e_mail: str
    created_at: datetime

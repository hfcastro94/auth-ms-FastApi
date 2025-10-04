from pydantic import BaseModel, EmailStr, Field

class RegisterInput(BaseModel):
    e_mail: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., min_length=8, example="mysecurepassword")
    type_user: str = Field(..., example="admin")

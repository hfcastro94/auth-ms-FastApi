from fastapi import APIRouter, HTTPException
from domain.dtos.auth.register_input import RegisterInput
from domain.dtos.auth.login_input import LoginInput
from service.crud.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(data: RegisterInput):
    user = AuthService.register(data.e_mail, data.password, data.type_user)
    if not user:
        raise HTTPException(status_code=400, detail="User already exists")
    return {"message": "User registered", "e_mail": user.e_mail}


@router.post("/login")
def login(data: LoginInput):
    token = AuthService.login(data.e_mail, data.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"Access Granted":data.e_mail, "Access_token": token, "token_type": "bearer"}
    

@router.get("/validate-token")
def validatetoken(data:str):
    return AuthService.verify_token(data)

from fastapi import FastAPI
from controller import auth_controller


app = FastAPI(
    title="PROYECTO_TEAM_B - Authentication Microservice",
    description="Microservicio de autenticación con FastAPI y DynamoDB",
    version="1.0.0"
)
app.include_router(auth_controller.router)


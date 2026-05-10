from fastapi import APIRouter
from pydantic import BaseModel
from services.auth_service import login

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login_route(data: LoginRequest):
    token = login(data.username, data.password)
    if not token:
        return {"error": "Invalid"}

    return {"token": token}

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from jwt_manager import create_token
from schemas.auth import User

auth_router = APIRouter()

@auth_router.post("/login", tags=["auth"])
def login(user: User):
    if user.email == 'admin@gmail.com' and user.password == '123456':
        token = create_token(user.dict())
        return JSONResponse(content={"token": token}, status_code=200)
    return JSONResponse(content={"message": "Unauthorized"}, status_code=401)


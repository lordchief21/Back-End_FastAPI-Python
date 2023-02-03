from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

routes = APIRouter(prefix="/basicauth",
                   tags=["basicauth"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


users_db = {
    "Lordchief": {
        "username": "Lordchief",
        "full_name": "Cesar Villanueva",
        "email": "lordchief21@gmail.com",
        "disabled": False,
        "password": "123456"
    },
    "Lordchief21": {
        "username": "Lordchief21",
        "full_name": "Cesar A Villanueva",
        "email": "lordchief212@gmail.com",
        "disabled": True,
        "password": "654321"
    }
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username]) # Los dobles asteriscos #


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación inválidas",
            headers={"WWW-Authenticate": "Bearer"})

    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")

    return user


@routes.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")

    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")

    return {"access_token": user.username, "token_type": "bearer"}


@routes.get("/usersauth/me")
async def me(user: User = Depends(current_user)):
    return user

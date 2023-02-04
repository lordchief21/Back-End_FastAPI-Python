from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime,timedelta

ALGORITH = "HS256"
TIME_DURATION_TOKEN = 1
SECRET_KEY = "cab39380cd8adc80738111298b742004e4a339768abd3d84836e33e108a715ae"



routes = APIRouter(prefix="/jwtauth",
                   tags=["basicauthJwt"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
        "password": "$2a$12$B2Gq.Dps1WYf2t57eiIKjO4DXC3IUMUXISJF62bSRiFfqMdOI2Xa6"
    },
    "Lordchief21": {
        "username": "Lordchief21",
        "full_name": "Cesar A Villanueva",
        "email": "lordchief212@gmail.com",
        "disabled": False,
        "password": "$2a$12$SduE7dE.i3/ygwd0Kol8bOFvEABaoOOlC8JsCSr6wpwB4zl5STU4S"
    }
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username]) # Los dobles asteriscos permiten Aceptar y pasar múltiples parámetros con nombre en una función. Mas Info -> https://www.codigopiton.com/como-usar-asterisco-y-doble-asterisco-en-python/#6-asterisco-doble-en-python #

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


# Generamos la validación de nuestro token e inclusive nos lanza la excepction de acuerdo a la duración  #
async def auth_user(token: str = Depends(oauth2)):   
    exception = HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciales de autenticación inválidas ó expiradas",
                    headers={"WWW-Authenticate": "Bearer"})
    
    try:
        username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITH]).get("sub")
        if username is None:
            raise exception
    except JWTError:
         raise exception
     
    return search_user(username)

#Valida de acuerdo a nuestra dependencia <auth_user>#

async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")
    return user

#Realizamos una ruta de autenticación con JWT y que nos arroje nuestro access token Bearer para las siguientes rutas#

@routes.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")

    user = search_user_db(form.username)
    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
    access_token = {"sub": user.username, "exp": datetime.utcnow() + timedelta(minutes=TIME_DURATION_TOKEN)} #Generamos nuestro accessToken y le seteamos la expiración#
    
    return {"access_token": jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITH), "token_type": "bearer"}


#Ruta para validar el user que se autenticó#
@routes.get("/usersauth/me")
async def me(user: User = Depends(current_user)):
    return user
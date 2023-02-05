from fastapi import APIRouter,HTTPException,status
from pydantic import BaseModel
from db.models.userModel import User
from db.schemas.userSchema import user_schema
from db.client import client_db

#El prefix funciona para definir el prefijo de la ruta que se está trabajando y refactorizar el código. El tag sirve para clasificar la ruta en la documentación SwaggerUI#
routes = APIRouter(prefix= "/usersdb",
                   tags=["usersdb"])  



    
users_list = []


@routes.get("/")
async def usersForAPI():
    return users_list

@routes.get("/{name}") #Pasar parámetro por medio de una ruta #
async def user(name: str):
    usuario = filter(lambda user: user.name == name, users_list)
    try:
        return list(usuario)[0]
    except:
        return {"MessageError": "No se encontró el usuario"}


@routes.post("/",response_model=User, status_code=status.HTTP_200_OK)
async def user(user: User):
    
    user_dict = dict(user)
    del user_dict["id"]        
    id = client_db.local.users.insert_one(user_dict).inserted_id #Con esta línea agregamos usuarios a nuestros modelos y generamos un schema propio#  
    
    #Pasamos la función para generar el Schema#
    new_user = user_schema(client_db.local.users.find_one({"_id":id})) # El guión bajo es porque MongoDb lo genera en automático asi #  
    
    return User(**new_user) #Recordenmos que los <<**>> son los llamados **kwargs
    

@routes.put("/update")
async def changeInfoUser(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.name == user.name:
            users_list[index] = user
            found = True
            return {"Message": "Usuario actualizado con éxito"}    
    if not found:
        return {"Message": "No se ha actualizado el usuario"}
    

@routes.delete("/delete/{name}")
async def deleteUser(name: str):
    found = False
    for index, user_saved in enumerate(users_list):
        if user_saved.name == name:
            del users_list[index]
            found = True
            return {"Message": "Usuario eliminado con éxito"}
    if not found:
         return {"Message": "No se ha eliminado el usuario"}
    
            
    
def users_validate(name: str):
    usuario = filter(lambda user: user.name == name, users_list)
    try:
        return list(usuario)[0]
    except:
        return {"MessageError": "No se encontró el usuario"}
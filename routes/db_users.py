from fastapi import APIRouter,HTTPException,status
from pydantic import BaseModel
from db.models.userModel import User
from db.schemas.userSchema import user_schema,users_schema
from db.client import client_db
from bson import ObjectId




#El prefix funciona para definir el prefijo de la ruta que se está trabajando y refactorizar el código. El tag sirve para clasificar la ruta en la documentación SwaggerUI#
routes = APIRouter(prefix= "/usersdb",
                   tags=["usersdb"])  


@routes.get("/", response_model=list[User])
async def usersDb():
    return users_schema(client_db.users.find())


@routes.get("/{id}") #Pasar parámetro por medio de una ruta #
async def userID(id: str):
     return users_validate("_id", ObjectId(id))


@routes.post("/",response_model=User, status_code=status.HTTP_200_OK)
async def user(user: User):
    
    if(type(users_validate("email", user.email))) == User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario ya existe")
        
    user_dict = dict(user)
    del user_dict["id"]        
    id = client_db.users.insert_one(user_dict).inserted_id  #Con esta línea agregamos usuarios a nuestros modelos y generamos un schema propio#  
    
    #Pasamos la función para generar el Schema#
    new_user = user_schema(client_db.users.find_one({"_id":id}))  # El guión bajo es porque MongoDb lo genera en automático asi #  
    
    return User(**new_user)  #Recordenmos que los <<**>> son los llamados **kwargs
    

@routes.put("/", response_model= User)
async def changeInfoUser(user: User):
    
    user_dictionary = dict(user)
    del user_dictionary["id"]
    
    try:
        client_db.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dictionary)
    except:
        return {"Message": "No se ha actualizado el usuario"}
    
    return users_validate("_id", ObjectId(user.id))

    

@routes.delete("/{id}")
async def deleteUser(id: str, status_code= status.HTTP_204_NO_CONTENT):
    try:
        found = client_db.users.find_one_and_delete({"_id": ObjectId(id)})
        return {"Message": "Usuario eliminado con éxito"}
    except:
        return {"Message": "No se ha eliminado el usuario"}
    
            

 
#Utilizamos esta funcion para buscar por medio de el ObjectId o cualquier campo de MongoDb. Es mas genérico y ahorramos en código#
    
def users_validate(field: str, key):  #Dejamos el key genérico o sin el type_hint por si se envía un datatype distinto#
    try:
        findUser = user_schema(client_db.users.find_one({field: key}))
        return User(**findUser)
    except:
        return {"MessageError": "No se encontró el usuario"}
    
    
    
    


"""
Utilizamos esta funcion para buscar por medio del email contenido en MongoDb    

def users_validate(email: str):
    try:
        findEmail = user_schema(client_db.local.users.find_one({"email":email}))
        return User(**findEmail)
    except:
        return {"MessageError": "No se encontró el usuario"}
"""
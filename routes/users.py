from fastapi import APIRouter,HTTPException
from pydantic import BaseModel

#El prefix funciona para definir el prefijo de la ruta que se está trabajando y refactorizar el código. El tag sirve para clasificar la ruta en la documentación SwaggerUI#
routes = APIRouter(prefix= "/users",
                   tags=["products"])  


class User(BaseModel): #Esto es un BaseModel#
    name: str
    surname:str
    nickname:str
    
users_list = [
    User(name ="Cesar",surname="Villanueva",nickname="Lordchief"),
    User(name ="Tanjiro",surname="Kamado",nickname="FireDancer"),
    User(name ="Nezuko",surname="Kamado",nickname="GoodDemon"),
    User(name ="Zenitsu",surname="Agatsuma",nickname="BoostRain"),
    User(name ="Inosuke",surname="Hashibira",nickname="LordAnimal")
]


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


@routes.post("/", status_code=200)
async def user(user: User):
    
    if type(users_validate(user.name)) == User :
        raise HTTPException(409,{"Message": "El usuario ya existe"}) # Usamos el raise que para que suba la excepción al status code de la ruta#
    else:
        users_list.append(user)
        return {"Message": "El usuario se creó correctamente"}
    

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
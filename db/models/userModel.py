from pydantic import BaseModel

class User(BaseModel): #Esto es un BaseModel#
    id: str | None  #El <<None>> es para determinar que sea opcional que se pase#
    username: str
    email: str
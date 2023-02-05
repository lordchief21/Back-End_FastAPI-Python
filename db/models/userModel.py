from pydantic import BaseModel
from typing import Optional

class User(BaseModel): #Esto es un BaseModel#
    id: Optional[str]  #El <<None>> es para determinar que sea opcional que se pase y el Optional es porque Deta corre con python 3.9#
    username: str
    email: str

#Creamos un Schema para la base de datos#

def user_schema(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": str(user["username"]),
        "email": str(user["email"])
    }
    
def users_schema(users) -> list:
    return [user_schema(user) for user in users]
from fastapi import FastAPI
from routes import users,auth_basico,jwt_authentication, db_users



app = FastAPI()


#Generate autoroutes from routes files#
app.include_router(users.routes)
app.include_router(auth_basico.routes)
app.include_router(jwt_authentication.routes)
app.include_router(db_users.routes)

@app.get("/")
async def root():
    return {"Message":"Hello world"}

@app.get("/url")
async def root():
    return {"Nombre":"Curso FastAPI", "url": "https://www.youtube.com/watch?v=TbcEqkabAWU"}

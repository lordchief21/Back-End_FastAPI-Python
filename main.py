from fastapi import FastAPI
from routes import users,auth_basico



app = FastAPI()


#Generate autoroutes from routes files#
app.include_router(users.routes)
app.include_router(auth_basico.routes)

@app.get("/")
async def root():
    return {"Message":"Hello world"}

@app.get("/url")
async def root():
    return {"Nombre":"Curso FastAPI", "url": "https://www.youtube.com/watch?v=TbcEqkabAWU"}

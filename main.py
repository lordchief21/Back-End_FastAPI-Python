from fastapi import FastAPI



app = FastAPI()


@app.get("/")
async def root():
    return {"Message":"Hello world"}

@app.get("/url")
async def root():
    return {"Nombre":"Curso FastAPI", "url": "https://www.youtube.com/watch?v=TbcEqkabAWU"}

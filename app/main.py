from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"mensaje": "holi mundo"}

@app.get("/url")
async def url():
    return {"url": "url de nuestro repositorio de github: https://github.com/dominox45/FastApi-learning.git"}
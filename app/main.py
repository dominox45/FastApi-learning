from fastapi import FastAPI
from app.routers import products #importamos el router de products
from app.routers import users #importamos el router de users

app = FastAPI()

#routers 
app.include_router(products.router) #incluimos el router de products en nuestra app
app.include_router(users.router) #incluimos el router de users en nuestra app



@app.get("/")
async def root():
    return {"mensaje": "holi mundo"}

@app.get("/url")
async def url():
    return {"url": "url de nuestro repositorio de github: https://github.com/dominox45/FastApi-learning.git"}
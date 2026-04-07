from fastapi import FastAPI
from app.routers import products #importamos el router de products
from app.routers import users #importamos el router de users
from app.routers import basic_auth_users #importamos el router de basic_auth_users
from fastapi.staticfiles import StaticFiles #importamos StaticFiles para montar la carpeta de archivos estáticos (imagenes, css, js, etc)

app = FastAPI()
#uvicorn app.main:app --reload 
# comando de inicio del server, el --reload hace que se reinicie el server cada vez que se hace un cambio en el codigo, 
# lo cual es muy util durante el desarrollo. El app.main:app hace referencia al archivo main.py y a la instancia de 
# FastAPI llamada app.

#routers 
app.include_router(products.router) #incluimos el router de products en nuestra app
app.include_router(users.router) #incluimos el router de users en nuestra app
app.include_router(basic_auth_users.app) #incluimos el router de basic_auth_users en nuestra app    

# Montar carpeta de archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
async def root():
    return {"mensaje": "holi mundo"}

@app.get("/url")
async def url():
    return {"url": "url de nuestro repositorio de github: https://github.com/dominox45/FastApi-learning.git"}
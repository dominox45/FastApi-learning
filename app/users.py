from fastapi import FastAPI 
from pydantic import BaseModel 

app = FastAPI()
 #inicio del server uvicorn app.users:app --reload 

 #entidad user 
class User(BaseModel): 
    name: str
    surname: str
    url: str
    age: int

users_list = [User(name="facu", surname="garcia", url="https://example.com", age=30)]

#ejemplo de carga a mano de json
@app.get("/usersjson")
async def usersjson():
    return {"name": "facu", "surname": "garcia", "url": "https://example.com", "age": 30}

#ejemplo de carga a mano de json con pydantic
@app.get("/users")
async def users():
    return users_list
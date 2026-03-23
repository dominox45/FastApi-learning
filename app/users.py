from fastapi import FastAPI 
from pydantic import BaseModel 

app = FastAPI()
 #inicio del server uvicorn app.users:app --reload 

 #entidad user 
class User(BaseModel): 
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id=1, name="facu", surname="garcia", url="https://example1.com", age=30),
              User(id=2, name="asa", surname="perez", url="https://example2.com", age=30),
              User(id=3, name="denji", surname="lopez", url="https://example3.com", age=28)]

#ejemplo de carga a mano de json|
@app.get("/usersjson")
async def usersjson():
    return [{"name": "facu", "surname": "garcia", "url": "https://example1.com", "age": 30},
            {"name": "asa", "surname": "perez", "url": "https://example2.com", "age": 25},
            {"name": "denji", "surname": "lopez", "url": "https://example3.com", "age": 28}]

#ejemplo de carga a mano de json con pydantic
@app.get("/users")
async def users():
    return users_list


#---------Path encuentra uno, query filtra muchos.------------- 


#implementacion de variables de path
@app.get("/user/{id}")
async def user(id: int):
   user = next((u for u in users_list if u.id ==id),None)
   if user:
       return user
   return {"error": "User not found :( "}

#implementacion de variables de query
@app.get("/users")
async def users(name: str = None, age: int = None):
    results = users_list
    if name is not None:
         results = [u for u in results if u.name.lower() == name.lower()]
    if age is not None:
         results = [u for u in results if u.age == age]

    if len(results) == 0:
        return {"error": "User not found :( "}
    return results
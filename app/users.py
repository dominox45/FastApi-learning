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

class UserCreate(BaseModel):
    name: str
    surname: str
    url: str
    age: int


users_list = [User(id=1, name="facu", surname="garcia", url="https://example1.com", age=30),
              User(id=2, name="asa", surname="perez", url="https://example2.com", age=30),
              User(id=3, name="denji", surname="lopez", url="https://example3.com", age=28)]

#ejemplo de carga a mano de json|

# @app.get("/users")
# async def usersjson():
#     return [{"name": "facu", "surname": "garcia", "url": "https://example1.com", "age": 30},
#             {"name": "asa", "surname": "perez", "url": "https://example2.com", "age": 25},
#             {"name": "denji", "surname": "lopez", "url": "https://example3.com", "age": 28}]

#ejemplo de carga a mano de json con pydantic

#@app.get("/users")
#async def users():
#    return users_list

#---------Path encuentra uno, query filtra muchos.------------- 


#implementacion de get con variables por path
@app.get("/users/{id}")
async def user(id: int):
   user = next((u for u in users_list if u.id ==id),None)
   if user:
       return user
   return {"error": "User not found "}

#implementacion de get con variables por query
@app.get("/users")
async def users(name: str = None, age: int = None):
    results = users_list
    if name is not None:
         results = [u for u in results if u.name.lower() == name.lower()]
    if age is not None:
         results = [u for u in results if u.age == age]

    if len(results) == 0:
        return {"error": "User not found"}
    return results

#implementacion de post para agregar un nuevo usuario (corregir validacion))
@app.post("/users")
async def create_user(userData: UserCreate): 
    new_id = max([u.id for u in users_list]) + 1 if users_list else 1
    Error = validar(userData)
    if Error is not True:
        return Error
    newUser = User(id=new_id, name=userData.name, surname=userData.surname, url=userData.url, age=userData.age)
    users_list.append(newUser)
    return newUser

#implemetacion de put para actualizar un usuario existente (version basica sin validacion)
@app.put("/users/")  
async def update_user(user: User):
    flag = False
    for i, usuari in enumerate(users_list):
        if usuari.id == user.id:
            users_list[i] = user
            flag = True
            break
    if flag:
        return user
    return {"error": "User not found"}

#implementacion de delete para eliminar un usuario
@app.delete("/users/{id}")
async def delete_user(id: int):
    for i, user in enumerate(users_list):
        if user.id == id:
            auxuser = users_list[i]
            del users_list[i]
            return {"message": f"User: {auxuser.name} has been deleted"}
    return {"error": "User not found"}


#(posterior eliminar validaciones innecesarias)
def validar_name(name: str):
    if not name.isalpha() or (len(name) < 2 or len(name) > 50):
        return False
        
    return True

def validar_age(age: int):
    if age < 0 or age > 120:
        return False 
    return True

def validar_url(url: str):
    if not url.startswith("http://") and not url.startswith("https://"):
        return False
    return True

def validar(user: UserCreate):
    if not validar_name(user.name):
        return {"error": "Name must be between 2 and 50 characters"}
    if not validar_age(user.age):
        return {"error": "Age must be between 0 and 120"}
    if not validar_url(user.url):
        return {"error": "Invalid URL"}
    return True
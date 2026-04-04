from fastapi import FastAPI, HTTPException

from pydantic import BaseModel, Field, HttpUrl, EmailStr

app = FastAPI()
 #inicio del server uvicorn app.users:app --reload 

 #entidad user 
class User(BaseModel): 
    id: int
    name: str = Field(min_length=2, max_length=50)
    surname: str = Field(min_length=2, max_length=50)
    url: HttpUrl
    age: int = Field(ge=0, le=120)
    email: EmailStr

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    surname: str = Field(min_length=2, max_length=50)
    url: HttpUrl
    age: int = Field(ge=0, le=120)
    email: EmailStr


users_list = [User(id=1, name="facu", surname="garcia", url="https://example1.com", age=30, email="facu@example.com"),
              User(id=2, name="asa", surname="perez", url="https://example2.com", age=30, email="asa@example.com"),
              User(id=3, name="denji", surname="lopez", url="https://example3.com", age=28, email="denji@example.com")]

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
@app.get("/users/{id}",response_model=User, status_code=200) #La solicitud tuvo éxito, El recurso ha sido recuperado y transmitido en el cuerpo del mensaje.
async def user(id: int):
   user = next((u for u in users_list if u.id ==id),None)
   if user:
       return user
   raise HTTPException(status_code=404, detail="User not found")

#implementacion de get con variables por query
@app.get("/users", response_model=list[User], status_code=200) #La solicitud tuvo éxito, El recurso ha sido recuperado y transmitido en el cuerpo del mensaje.
async def users(name: str = None, age: int = None):
    results = users_list 
    if name is not None:
         results = [u for u in results if u.name.lower() == name.lower()]
    if age is not None:
         results = [u for u in results if u.age == age]

    if len(results) == 0:
        raise HTTPException(status_code=404, detail="No users found with the specified criteria")
    return results

#implementacion de post para agregar un nuevo usuario 

@app.post("/users", response_model=User, status_code=201) #201 resultado de creacion exitosa
async def create_user(userData: UserCreate):  
    if any(u.email == userData.email for u in users_list):
        raise HTTPException(status_code=409, detail="User with the same email already exists") #409 conflicto por email repetido
    
    new_id = max([u.id for u in users_list]) + 1 if users_list else 1
    newUser = User(id=new_id, name=userData.name, surname=userData.surname, url=userData.url, age=userData.age, email=userData.email)
    users_list.append(newUser)
    return newUser

#implemetacion de put para actualizar un usuario existente (version basica sin validacion)

@app.put("/users",response_model=User, status_code=200) #200 resultado exitoso, el recurso ha sido actualizado
async def update_user(user: User):
    for i, useraux in enumerate(users_list):
        if useraux.id == user.id:
            if any(u.email == user.email and u.id != user.id for u in users_list):
                raise HTTPException(status_code=409, detail="User with the same email already exists") #409 conflicto por email repetido
            users_list[i] = user
            return user   
    raise HTTPException(status_code=404, detail="User not found")

#implementacion de delete para eliminar un usuario
@app.delete("/users/{id}",response_model=User, status_code=200) #200 resultado exitoso, el recurso ha sido eliminado
async def delete_user(id: int):
    for i, user in enumerate(users_list):
        if user.id == id:
            auxuser = users_list[i]
            del users_list[i]
            return auxuser
    raise HTTPException(status_code=404, detail="User not found")

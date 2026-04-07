from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field, HttpUrl, EmailStr
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm


oauth2 = OAuth2PasswordBearer(tokenUrl="login") #creamos una instancia de OAuth2PasswordBearer,
#el tokenUrl es la ruta donde se va a hacer el login para obtener el token de acceso. 
# En este caso, la ruta es /login


#      uvicorn app.routers.basic_auth_users:app --reload

app = APIRouter( prefix="/auth",
                 responses={404: {"description": "User not found"}}, 
                    tags=["Auth"]) #prefijo para todas las rutas de este router y tag para documentacion    }



class User(BaseModel): 
    username: str = Field(min_length=2, max_length=50)
    full_name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    disabled: bool

class UserDB(User):
    password: str = Field(min_length=8, max_length=128)

users_db = {
    "facutolaba": {
        "username": "facutolaba",
        "full_name": "Facu Labadie",
        "email": "facundo.tolaba@example.com",
        "disabled": False,
        "password": "12345678"
        },
    "asa": {
        "username": "asa",
        "full_name": "Asa Perez",
        "email": "asa.perez@example.com",
        "disabled": False,
        "password": "87654321"
    },
    "denji": {
        "username": "denji",
        "full_name": "Denji Himura",
        "email": "denji.himura@example.com",
        "disabled": False,
        "password": "87654321"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    return None


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    return None

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    #depends dice Oye, no esperes que el cliente me mande un JSON { "username": "..." }. 
    # Espera un formulario estándar de los de toda la vida (como los de HTML)"..
    #El formateo: Depends() toma los datos que llegan "sueltos" en la petición HTTP, verifica que tengan los nombres
    #  correctos (username y password) y construye el objeto form para que tú puedas hacer form.username dentro de la función.

    user_db=users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username")
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    return {"access_token": user.username, "token_type": "bearer"}


async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials", headers={"WWW-Authenticate": "Bearer"})
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return user




@app.get("/me")
async def me(user: User = Depends(current_user)):
    return user



#el header: En el mundo de la autenticación HTTP, existe un estándar. Cuando una API le dice a un cliente (como un navegador o una app móvil) 
# que no tiene permiso para entrar, no basta con mandarle un error 401. El estándar RFC 6750 dice que la API debe "explicar" qué tipo de autenticación espera.
# Esto se hace a través de un header llamado "WWW-Authenticate". En el caso de OAuth2, el valor de este header es "Bearer".
#entonces el header sirve para  explicar los accesos denegados cuando no se tienen permiso de acceso

#El Token no viaja en el Path: Viaja en los Headers (por seguridad y orden).

#oauth2 es el extractor: Su trabajo es ser el "aspirador" que saca el token del Header.

#Depends es el conector: Es el cable que une ese token extraído con tu función de Python.
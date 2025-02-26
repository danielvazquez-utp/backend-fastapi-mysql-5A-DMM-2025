from typing import Union
from fastapi import FastAPI
import mysql.connector

from models import User

app = FastAPI()

db = mysql.connector.connect(
    host = "localhost",
    user = 'root',
    password = '',
    database = 'backend_fastapi_mysql_db',
    consume_results = True
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# Endpoint que recupera la colección de usuarios
@app.get("/users")
def getUsers():
    usuarios = []
    query = "SELECT * FROM usuarios"
    cursor = db.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    no_regs = cursor.rowcount
    if no_regs>0:
        for record in records:
            usuario = {
                "id": record[0],
                "name": record[1],
                "lastname": record[2],
                "nickname": record[3],
                "password": record[4],
                "profile": record[5],
                "status": record[6]
            }
            usuarios.append(usuario)
        return {"status":"ok", "message": "Usuarios recuperados", "data": usuarios}
    else:
        return {"status":"ok", "message": "No hay usuarios"}

# Endpoint que recupera un usuario
@app.get("/users/{id}")
def getUserById( id ):
    query = "SELECT * FROM usuarios WHERE id = {}".format(id)
    cursor = db.cursor()
    cursor.execute(query)
    record = cursor.fetchone()
    no_regs = cursor.rowcount
    if no_regs>0:
        usuario = {
            "id": record[0],
            "name": record[1],
            "lastname": record[2],
            "nickname": record[3],
            "password": record[4],
            "profile": record[5],
            "status": record[6]
        }
        return {"status":"ok", "message": "Usuario recuperado", "data": usuario}
    else:
        return {"status":"error", "message": "Usuario no enocntrado"}

# Crear un endpoint que retorne un usuario verificando su usuario y contraseña

# Endpoint que crea un usuario
@app.post("/users")
def createUser( user:User ):
    query = "INSERT INTO usuarios (`name`, `lastname`, `nickname`, `password`, `profile`, `status`) VALUES ('{}', '{}', '{}', '{}', '{}', {})".format( user.name, user.lastname, user.nickname, user.password, user.profile, user.status )
    print(query)
    try :
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()
        return {
            "status": "ok",
            "message": "Usuario agregado con éxito",
        }
    except:
        return {"status":"error", "message": "Usuario no fue agregado"}

# Endoint para modifir un usuario
@app.put("/users")
def updateUser( user:User ):
    query = "UPDATE usuarios SET `name`='{}', `lastname`='{}', `nickname`='{}', `password`='{}', `profile`={}, `status`={} WHERE `id`={} ".format(  user.name, user.lastname, user.nickname, user.password, user.profile, user.status, user.id)
    print(query)
    try:
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()
        return {
            "status": "ok",
            "message": "Usuario modificado con éxito",
        }
    except:
        return {"status":"error", "message": "Usuario no fue modificado"}

# Endpoint para eliminar un usuario
@app.delete("/users/{id}")
def delUser( id ):
    query = "DELETE FROM usuarios WHERE `id`={}".format( id )
    print( query )
    try:
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()
        return {
            "status": "ok",
            "message": "Usuario eliminado con éxito",
        }
    except:
        return {"status":"error", "message": "Usuario no fue eliminado"}
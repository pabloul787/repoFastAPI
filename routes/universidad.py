from fastapi import APIRouter, HTTPException
import sqlite3
from pydantic import BaseModel
from typing import Optional
router_uni = APIRouter(prefix = "/universidad", tags=["Universidad"])

class Registro(BaseModel):
    curso: str
    sigla: str
    user: int
    año: int
    semestre: int
    nota: float

class UpRegistro(BaseModel):
    curso: Optional[str] = None
    sigla: Optional[str] = None
    user: Optional[int] = None
    year: Optional[int] = None
    semestre: Optional[int] = None
    nota: Optional[float] = None

def crear_db():
    #Primero creare la base de datos si es que no existe
    with sqlite3.connect('reg_u1.db') as conexion:
        cursor1 = conexion.cursor() #me permite acceder a la base de datos y hacer queries en ella.

        #Aqui creo la tabla de cursos aprobados
        crear_tabla = '''
        CREATE TABLE IF NOT EXISTS registros_academicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            curso TEXT NOT NULL,
            sigla TEXT DEFAULT "NA",
            user INTEGER NOT NULL,
            year INTEGER NOT NULL,
            semestre INTEGER NOT NULL,
            nota FLOAT NOT NULL
        );
        '''
        #aqui ejecuto la creación de la tabla
        cursor1.execute(crear_tabla)

        #Hago un commit de la tabla recien hecha (si recien la estoy creando)
        conexion.commit()


@router_uni.get("/resumen/{user_id}")
def resumen(user_id:int):
    with sqlite3.connect('reg_u1.db') as conexion:
        cursor2 = conexion.cursor() #me permite acceder a la base de datos y hacer queries en ella.
        query = "SELECT * FROM registros_academicos WHERE user = ?;"

        #Ejecuto el query de arriba
        cursor2.execute(query, (user_id,))

        #Me devuelve todos los registros como una lista de tuplas con todos las columnas creadas
        registros = cursor2.fetchall()

        if not registros:
            raise HTTPException(404, "No hay registros asociados a este user id")

        #devuelve los registros
        #return(registros)
        output = []
        for item in registros:
            if item[3] == "0":
                output.append(f"ID: {item[0]} | Curso: {item[1]} | Sigla: {item[2]} | Estudiante: Pablo Uribe | Nota: {item[6]}")
            if item[3] == "1":
                output.append(f"Curso: {item[1]} Sigla: {item[2]} Estudiante: Joaquin Troncoso | Nota: {item[6]}")
        return(output)

@router_uni.post("/nuevo_registro") 
async def crear_nuevo_registro(registro: Registro):
    with sqlite3.connect('reg_u1.db') as conexion:
        cursor3 = conexion.cursor() #me permite acceder a la base de datos y hacer queries en ella.

        #creo el registro
        insertar_registro = '''
        INSERT INTO registros_academicos (curso, sigla, user, year, semestre, nota) 
        VALUES (?, ?, ?, ?, ?, ?);
        '''
        datos_tupla = (registro.curso, registro.sigla, registro.user, registro.año, registro.semestre, registro.nota)

        #registro_input = (curso, sigla, int(user), int(year), int(semestre), float(nota))

        cursor3.execute(insertar_registro, datos_tupla) #antes datos tupla era registro_input

        conexion.commit()
        return("Exitoso")
    
@router_uni.patch("/actualizar_registro/{registro_id}")
async def actualizar_registro(registro_id: int, registro_data: UpRegistro):
    with sqlite3.connect("reg_u1.db") as conexion:
        cursor = conexion.cursor()
        update_data = registro_data.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(status_code=400, detail="No ingresó ningún campo para actualizar")

        variables_to_change = [f"{key} = ?" for key in update_data.keys()]
        condicion = ", ".join(variables_to_change)

        valores = list(update_data.values())
        valores.append(registro_id)

        actualizar_registro = f"""
            UPDATE registros_academicos
            SET {condicion}
            WHERE id = ?;"""

        cursor.execute(actualizar_registro, tuple(valores))
        return {
            "Mensaje": f"Registro con ID {registro_id} actualizado exitosamente.",
            "Campos actualizados": update_data,
        }

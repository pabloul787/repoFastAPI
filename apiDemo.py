from fastapi import FastAPI
import pandas as pd

app = FastAPI()

db = pd.read_csv("demoDDBB.csv", sep=";")

@app.get("/")
async def root():
    return "Bienvenido, estos son los ID para consultar información sobre los estudiantes Pablo Uribe --> ID:0\nJoaquin Troncoso --> ID: 1"
    

@app.get("/universidad/{user_id}")
def general_des(user_id:int):
    lista_users = list(dict.fromkeys(db["Alumno"].tolist()))
    s_user = db[db["Alumno"]==lista_users[user_id]]
    cursos = s_user["curso"].tolist()
    max_prom = max(s_user["promedio"].tolist())
    oldest_registry = min(s_user["año"].tolist())
    profesores_ramo = {}
    for i in cursos:
        profesores_ramo[i] = s_user[db["curso"]==i]["profesor"]
    return "La siguiente información académica fue encontrada sobre el alumno:", {
        "Nombre": lista_users[user_id],
        "Cursos estudiados": ",".join(cursos),
        "Promedio maximo encontrado": max_prom,
        "Año del ramo más antiguo encontrado": oldest_registry
    }, "¿Quieres saber más del ramo?", "Profesor por ramo", profesores_ramo
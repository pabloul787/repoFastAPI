#Este codigo me permite dar información general del alumno relacionado a asu historial academico------------------------------
import pandas as pd

db = pd.read_csv("demoDDBB.csv", sep=";") #importo el archivo csv

def general_des(user_id:int):
    lista_users = list(dict.fromkeys(db["Alumno"].tolist())) #obtenga una lista con los valores unicos de alumnos del csv
    s_user = db[db["Alumno"]==lista_users[user_id]] #elijo al alumno de la lista de arriba que tenga el mismo indice enviado en la url
    cursos = s_user["curso"].tolist() #obtenga todos sus cursos como una lista
    max_prom = max(s_user["promedio"].tolist()) #maxima nota
    oldest_registry = min(s_user["año"].tolist()) #año menor
    profesores_ramo = {} #creo una diccionario vacio con los profesores
    for i in cursos:
        profesores_ramo[i] = s_user[db["curso"]==i]["profesor"].values[0] #agrego un key:value de la forma "Nombre del ramo" :"Profesor"
    return "La siguiente información académica fue encontrada sobre el alumno:", {
        "Nombre": lista_users[user_id],
        "Cursos estudiados": ",".join(cursos),
        "Promedio maximo encontrado": max_prom,
        "Año del ramo más antiguo encontrado": oldest_registry
    }, "¿Quieres saber más del ramo?", "Profesor por ramo", profesores_ramo
#----------------------------------------------------------------------------------------------------------------------------
#Esta función me da más información sobre el profesor

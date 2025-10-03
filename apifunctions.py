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


#FUNCION DE DE CREDITOS
class Credito():
    def __init__(self, monto_credito, tasa_mes, meses):
        self.monto_inicial_credito = monto_credito
        self.tasa_mes = tasa_mes
        self.meses = meses
        self.deuda_actual = monto_credito
        self.tasa_anual = self.anualiza_tasa()
        self.cuota_mes = self.calcula_cuota()
    
    def anualiza_tasa(self):
        return (1+self.tasa_mes)**12 - 1
    
    def calcula_cuota(self):
        return (self.monto_inicial_credito * self.tasa_mes) / (1-(1/(1+self.tasa_mes)**self.meses))
    
    def pago(self):
        if self.deuda_actual <= 0:
            return (0.0, 0.0) 
        pago = self.cuota_mes
        intereses = self.tasa_mes * self.deuda_actual
        amortizado = pago - intereses

        if amortizado > self.deuda_actual:
            amortizado = self.deuda_actual
        pago = intereses + amortizado  
        self.deuda_actual = self.deuda_actual - amortizado
        tupla = (amortizado, intereses)
        return tupla
    
    def __repr__(self):  # o __str__
        return "Monto actual: " + str(self.deuda_actual) + \
           " | Tasa anual: " + str(self.tasa_anual) + \
           " | Plazo: " + str(self.meses) + \
           " | Cuota mensual: " + str(self.cuota_mes)


def cargar_creditos(ruta_csv: str):
    resultado = []
    with open(ruta_csv, "r", encoding="utf-8") as f:
        # saltar encabezado
        encabezado = f.readline()
        for linea in f:
            partes = linea.strip().split(";")  # separa por ';'
            nombre = partes[0]
            monto = float(partes[1])
            tasa_mes = float(partes[2])
            plazo_meses = int(partes[3])
            resultado.append((nombre, monto, tasa_mes, plazo_meses))
    return resultado

lista_creditos = cargar_creditos("creditos.csv")
#print(lista_creditos)


objetos = {}
def crear_credito(listacreditos):
    for i in range(len(listacreditos)):
        nombre = listacreditos[i][0]
        monto = listacreditos[i][1]
        tasa_mes = listacreditos[i][2]
        plazo_meses = listacreditos[i][3]
        objetos[nombre] = Credito(monto, tasa_mes, plazo_meses)       

from fastapi import FastAPI, HTTPException

app = FastAPI(title="API Créditos (simple)")

# Cargamos en memoria los objetos al iniciar la app
@app.on_event("startup")
def _init_data():
    # Usa la lista ya cargada y tu función existente
    crear_credito(lista_creditos)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/creditos")
def listar_creditos():
    #Devuelve en el formato que pediste originalmente: [(nombre, monto_total, tasa_anual, plazo_meses), ...] tomando los datos desde 'objetos' ya construidos.
    salida = []
    for nombre, c in objetos.items():
        salida.append((nombre, float(c.monto_inicial_credito), float(c.tasa_anual), int(c.meses)))
    return salida

@app.get("/creditos/{nombre}") #Detalle de un credito por nombre
def detalle_credito(nombre: str):
    if nombre not in objetos:
        raise HTTPException(status_code=404, detail="Crédito no encontrado")
    c = objetos[nombre]
    return {
        "nombre": nombre,
        "monto_inicial": c.monto_inicial_credito,
        "tasa_mes": round(c.tasa_mes, 4),
        "tasa_anual": round(c.tasa_anual, 2),
        "meses": c.meses,
        "deuda_actual": c.deuda_actual,
        "cuota_mensual": c.cuota_mes,
    }

@app.post("/creditos/{nombre}/pago")
def aplicar_pago(nombre: str): #Aplica un pago usando método Credito.pago(). Retorna amortización, intereses y nuevo saldo.
    if nombre not in objetos:
        raise HTTPException(status_code=404, detail="Crédito no encontrado")
    c = objetos[nombre]
    amortizado, intereses = c.pago()
    return {
        "nombre": nombre,
        "amortizado": round(amortizado, 2),
        "intereses": round(intereses, 2),
        "deuda_actual": round(c.deuda_actual, 2),
        "cuota_mensual": round(c.cuota_mes, 2),
    }


@app.get("/creditos/{nombre}/pago")
def aplicar_pago_get(nombre: str):
    if nombre not in objetos:
        raise HTTPException(status_code=404, detail="Crédito no encontrado")
    c = objetos[nombre]
    amortizado, intereses = c.pago()
    return {
        "nombre": nombre,
        "amortizado": round(amortizado, 2),
        "intereses": round(intereses, 2),
        "deuda_actual": round(c.deuda_actual, 2),
        "cuota_mensual": round(c.cuota_mes, 2),
    }

#uvicorn prueba:app --reload
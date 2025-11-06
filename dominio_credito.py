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


#uvicorn apifunctions:app --reload
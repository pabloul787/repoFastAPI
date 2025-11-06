import requests
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta  # pip install python-dateutil

USER = ""
PASS = ""

def tpm_mensual_por_fecha(fecha_yyyy_mm_dd, user, password):
 
    serie = "F022.TPM.TIN.D001.NO.Z.M"
    base = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx"
    url = (
        f"{base}?user={user}&pass={password}"
        f"&firstdate={fecha_yyyy_mm_dd}&lastdate={fecha_yyyy_mm_dd}"
        f"&timeseries={serie}&function=GetSeries"
    )

    r = requests.get(url)
    r.raise_for_status()
    data = r.json()

    obs = data["Series"]["Obs"]
    if not obs:
        return None  
    fila = obs[0]
    return {
        "fecha": fila["indexDateString"],      # 'dd-mm-YYYY'
        "tpm": float(fila["value"])            # porcentaje
    }

# {'fecha': '01-11-2025', 'tpm': 5.0}   <-- ejemplo 



def _yyyy_mm_01(fecha_yyyy_mm_dd: str) -> str:
    """Normaliza cualquier fecha a 'YYYY-MM-01'."""
    d = datetime.strptime(fecha_yyyy_mm_dd, "%Y-%m-%d").replace(day=1)
    return d.strftime("%Y-%m-%d")

def _buscar_tpm_mas_reciente_hasta(fecha_yyyy_mm_dd, user, password, max_retro_mes=12):
 
    d = datetime.strptime(_yyyy_mm_01(fecha_yyyy_mm_dd), "%Y-%m-%d")
    for _ in range(max_retro_mes + 1):
        resp = tpm_mensual_por_fecha(d.strftime("%Y-%m-%d"), user, password)
        if resp is not None:
            return resp
        d = d - relativedelta(months=1)  # retrocede un mes y reintenta
    return None

def tpm_mensual_y_variacion(fecha_yyyy_mm_dd, user, password):

    actual = _buscar_tpm_mas_reciente_hasta(fecha_yyyy_mm_dd, user, password)
    if actual is None:
        return None 

    # Fecha "actual" encontrada (formato dd-mm-YYYY from API -> la convertimos a YYYY-MM)
    dt_act = datetime.strptime(actual["fecha"], "%d-%m-%Y")
    ym_act = dt_act.strftime("%Y-%m")
    tpm_act = float(actual["tpm"])

    # 2) Buscar TPM del mes anterior al "actual" encontrado (o la más cercana anterior)
    d_prev = (dt_act.replace(day=1) - relativedelta(months=1)).strftime("%Y-%m-%d")
    anterior = _buscar_tpm_mas_reciente_hasta(d_prev, user, password)
    tpm_prev = None
    ym_prev = None
    if anterior is not None:
        dt_prev = datetime.strptime(anterior["fecha"], "%d-%m-%Y")
        ym_prev = dt_prev.strftime("%Y-%m")
        tpm_prev = float(anterior["tpm"])

    variacion = None if tpm_prev is None else (tpm_act - tpm_prev)

    return {
        "fecha": ym_act,
        "tpm": tpm_act,
        "fecha_anterior": ym_prev,
        "tpm_anterior": tpm_prev,
        "variacion": variacion
    }

def dolar_por_fecha(fecha_yyyy_mm_dd, user, password):
 
    serie = "F073.TCO.PRE.Z.D"
    base = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx"
    url = (
        f"{base}?user={user}&pass={password}"
        f"&firstdate={fecha_yyyy_mm_dd}&lastdate={fecha_yyyy_mm_dd}"
        f"&timeseries={serie}&function=GetSeries"
    )

    r = requests.get(url)
    r.raise_for_status()
    data = r.json()

    obs = data["Series"]["Obs"]
    if not obs:
        return None  # no hay dato EXACTO para esa fecha

    fila = obs[0]  # única observación del día
    return {
        "fecha": fila["indexDateString"],      
        "usdclp": float(fila["value"])         
    }

def _usd_ultimo_disponible(fecha_yyyy_mm_dd, user, password, max_retro=7):
 
    d = datetime.strptime(fecha_yyyy_mm_dd, "%Y-%m-%d")
    for _ in range(max_retro + 1):
        dato = dolar_por_fecha(d.strftime("%Y-%m-%d"), user, password)
        if dato is not None:
            return dato
        d -= timedelta(days=1)  # retrocede un día y reintenta
    return None

def dolar_con_30_dias(fecha_yyyy_mm_dd, user, password):
 
    actual = _usd_ultimo_disponible(fecha_yyyy_mm_dd, user, password, max_retro=7)
    if actual is None:
        return None

    # 2) Dólar 30 días antes (o último disponible anterior)
    d_30 = (datetime.strptime(fecha_yyyy_mm_dd, "%Y-%m-%d") - timedelta(days=30)).strftime("%Y-%m-%d")
    antes_30 = _usd_ultimo_disponible(d_30, user, password, max_retro=7)
    if antes_30 is None:
        return None

    return {
        "fecha_actual": actual["fecha"],
        "usd_actual": actual["usdclp"],
        "fecha_30d": antes_30["fecha"],
        "usd_30d": antes_30["usdclp"],
    }

def uip_basicos(fecha_yyyy_mm_dd, user, password):

    tpm_data = tpm_mensual_y_variacion(fecha_yyyy_mm_dd, user, password)
    if not tpm_data or tpm_data.get("tpm") is None or tpm_data.get("tpm_anterior") is None:
        return {"error": "No hay datos suficientes de TPM para esa fecha o el mes anterior."}

    tpm_actual = tpm_data["tpm"]
    tpm_anterior = tpm_data["tpm_anterior"]
    fecha_tpm_actual = tpm_data["fecha"]
    fecha_tpm_anterior = tpm_data["fecha_anterior"]

    # Dólar (diario, 30 días antes) 
    usd_data = dolar_con_30_dias(fecha_yyyy_mm_dd, user, password)
    if not usd_data or usd_data.get("usd_actual") is None or usd_data.get("usd_30d") is None:
        return {"error": "No hay datos suficientes de tipo de cambio para esa fecha o 30 días antes."}

    usd_actual = usd_data["usd_actual"]
    usd_anterior = usd_data["usd_30d"]
    fecha_usd_actual = usd_data["fecha_actual"]
    fecha_usd_anterior = usd_data["fecha_30d"]

    #Etiquetas de cambio con tolerancia (para evitar “ruido” mínimo)
    def etiqueta_cambio(actual, anterior, tol=1e-6):
        delta = actual - anterior
        if delta > tol:   return "positivo"
        if delta < -tol:  return "negativo"
        return "nulo"

    # Tolerancias: TPM en puntos porcentuales; USD en pesos 
    cambio_tpm = etiqueta_cambio(tpm_actual, tpm_anterior, tol=0.005)  # 0.005 pp ~ 0.005%
    cambio_usd = etiqueta_cambio(usd_actual, usd_anterior, tol=1.0)    # $1 CLP

    if cambio_tpm == "positivo" and cambio_usd == "negativo":
        comentario = "Se cumple la paridad: subió la TPM y el peso se apreció (USD bajó)."
    elif cambio_tpm == "negativo" and cambio_usd == "positivo":
        comentario = "Se cumple la paridad: bajó la TPM y el peso se depreció (USD subió)."
    elif cambio_tpm == "negativo" and cambio_usd == "negativo":
        comentario = "No se cumple: con TPM a la baja, se esperaba depreciación del peso (USD al alza) y cayó."
    elif cambio_tpm == "positivo" and cambio_usd == "positivo":
        comentario = "No se cumple: con TPM al alza, se esperaba apreciación del peso (USD a la baja) y subió."
    elif cambio_tpm == "nulo" and cambio_usd == "positivo":
        comentario = "No podemos probar la paridad: el USD subió pero la TPM se mantuvo."
    elif cambio_tpm == "nulo" and cambio_usd == "negativo":
        comentario = "No podemos probar la paridad: el USD bajó pero la TPM se mantuvo."
    elif cambio_tpm == "positivo" and cambio_usd == "nulo":
        comentario = "No se cumple: subió la TPM y el tipo de cambio no reaccionó."
    elif cambio_tpm == "negativo" and cambio_usd == "nulo":
        comentario = "No se cumple: bajó la TPM y el tipo de cambio no reaccionó."
    elif cambio_tpm == "nulo" and cambio_usd == "nulo":
        comentario = "Sin conclusiones: ninguna de las variables se movió."
    else:
        comentario = "Caso no contemplado."

    return {
        "tpm_actual": tpm_actual,
        "tpm_anterior": tpm_anterior,
        "usd_actual": usd_actual,
        "usd_anterior": usd_anterior,
        "fecha_tpm_actual": fecha_tpm_actual,
        "fecha_tpm_anterior": fecha_tpm_anterior,
        "fecha_usd_actual": fecha_usd_actual,
        "fecha_usd_anterior": fecha_usd_anterior,
        "cambio de la tpm": cambio_tpm,
        "cambio del usd": cambio_usd,
        "comentario": comentario
    }


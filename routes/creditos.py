from fastapi import APIRouter, HTTPException
from dominio_creditos import objetos, crear_credito, lista_creditos

router = APIRouter(prefix="/creditos", tags=["creditos"])

if not objetos:
    crear_credito(lista_creditos)

@router.get("")
def listar_creditos():
    salida = []
    for nombre, c in objetos.items():
        salida.append((nombre, float(c.monto_inicial_credito), float(c.tasa_anual), int(c.meses)))
    return salida

@router.get("/{nombre}")
def detalle_credito(nombre: str):
    if nombre not in objetos:
        raise HTTPException(status_code=404, detail="Crédito no encontrado")
    c = objetos[nombre]
    return {
        "nombre": nombre,
        "monto_inicial": round(c.monto_inicial_credito, 2),
        "tasa_mes": round(c.tasa_mes, 4),     
        "tasa_anual": round(c.tasa_anual, 2),  
        "meses": c.meses,
        "deuda_actual": round(c.deuda_actual, 2),
        "cuota_mensual": round(c.cuota_mes, 2),
    }

@router.post("/{nombre}/pago")
def aplicar_pago(nombre: str):
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


@router.get("/{nombre}/pago")
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
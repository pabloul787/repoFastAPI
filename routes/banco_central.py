from fastapi import APIRouter, HTTPException, Query
from dominio_banco_central import (
    tpm_mensual_por_fecha,
    tpm_mensual_y_variacion,
    dolar_por_fecha,
    dolar_con_30_dias,
    uip,
    USER,
    PASS
)

router = APIRouter(prefix="/bc", tags=["banco_central"])

@router.get("/tpm")
def get_tpm(fecha: str = Query(..., description="YYYY-MM-DD (usar 01 del mes para TPM mensual)")):
    dato = tpm_mensual_por_fecha(fecha, USER, PASS)
    if not dato:
        raise HTTPException(404, "Sin dato para esa fecha (TPM mensual). Prueba con YYYY-MM-01.")
    return dato

@router.get("/tpm/variacion")
def get_tpm_variacion(fecha: str = Query(..., description="YYYY-MM-DD (tomará el mes de la fecha)")):
    dato = tpm_mensual_y_variacion(fecha, USER, PASS)
    if not dato:
        raise HTTPException(404, "Sin datos suficientes de TPM en ese rango/mes.")
    return dato

@router.get("/usd")
def get_usd(fecha: str = Query(..., description="YYYY-MM-DD (día exacto; si es feriado puede no haber dato)")):
    dato = dolar_por_fecha(fecha, USER, PASS)
    if not dato:
        raise HTTPException(404, "Sin dato exacto de USD para ese día (puede ser fin de semana/feriado).")
    return dato

@router.get("/usd/30d")
def get_usd_30d(fecha: str = Query(..., description="YYYY-MM-DD (trae día y 30 días antes, con fallback a último hábil)")):
    dato = dolar_con_30_dias(fecha, USER, PASS)
    if not dato:
        raise HTTPException(404, "Sin datos suficientes de USD en el rango.")
    return dato

@router.get("/uip")
def get_uip(fecha: str = Query(..., description="YYYY-MM-DD")):
    dato = uip(fecha, USER, PASS)
    if not dato or "error" in dato:
        raise HTTPException(404, dato.get("error", "No fue posible obtener los datos base de UIP."))
    return dato
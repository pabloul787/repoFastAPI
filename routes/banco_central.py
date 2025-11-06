from fastapi import APIRouter, HTTPException, Query
from dominio_banco_central import (
    tpm_mensual_por_fecha,
    tpm_mensual_y_variacion,
    dolar_por_fecha,
    dolar_con_30_dias,
    uip_basicos,
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
#   Documentación de la API Banco Central de Chile

##   Resumen de Endpoints 

| # | Endpoint | Método | Parámetros | Descripción | Ejemplo de uso |
|---|---------|--------|------------|-------------|----------------|
| 1 | `/bc/tpm` | GET | `?fecha=YYYY-MM-DD` | TPM del mes indicado (usar el **día 01** del mes) | `/bc/tpm?fecha=2024-09-01` |
| 2 | `/bc/tpm/variacion` | GET | `?fecha=YYYY-MM-DD` | TPM del mes y del mes previo + variación | `/bc/tpm/variacion?fecha=2024-09-15` |
| 3 | `/bc/usd` | GET | `?fecha=YYYY-MM-DD` | Dólar observado del día indicado | `/bc/usd?fecha=2024-09-15` |
| 4 | `/bc/usd/30d` | GET | `?fecha=YYYY-MM-DD` | Dólar del día y de ~30 días antes + variación | `/bc/usd/30d?fecha=2024-09-15` |
| 5 | `/bc/uip` | GET | `?fecha=YYYY-MM-DD` | Evalúa UIP (TPM vs. USD) con sup. de tasa externa constante | `/bc/uip?fecha=2024-09-15` |

---

# Banco Central API — Documentación

## Descripción General

La **API del Banco Central** es un servicio web construido con FastAPI que se conecta a la API pública del Banco Central de Chile para obtener indicadores macroeconómicos clave como la **Tasa de Política Monetaria (TPM)** y el **Tipo de Cambio (USD/CLP)**.  
Además, implementa una validación teórica de la **Paridad de Tasas de Interés No Cubierta (UIP)**, asumiendo una tasa externa constante.

Esta API demuestra la integración entre **Python**, **servicios web externos** y **análisis económico aplicado** para fines de Ciencia de Datos.

**URL base:** `http://localhost:8000`

**Tecnologías:**  
- **Framework:** FastAPI  
- **API Externa:** Banco Central de Chile — SIETE REST API  
- **Librerías:** `requests`, `pandas`, `datetime`, `python-dateutil`  
- **Versión de Python:** 3.10+

---

## Tabla de Contenidos

- [Inicio Rápido](#inicio-rápido)  
- [Descripción Funcional](#descripción-funcional)  
- [Endpoints de la API](#endpoints-de-la-api)  
- [Ejemplos de Uso](#ejemplos-de-uso)  
- [Contexto Económico](#contexto-económico)  
- [Buenas Prácticas para Estudiantes](#buenas-prácticas-para-estudiantes)  
- [Estructura del Proyecto](#estructura-del-proyecto)  
- [Solución de Problemas](#solución-de-problemas)

---

## Inicio Rápido

### Instalación

```bash
# Instalar dependencias requeridas
pip install fastapi uvicorn requests python-dateutil pandas

# Ejecutar la aplicación
uvicorn apiDemo:app --reload
```

### Acceso

- **Home:** `http://localhost:8000/`  
- **Docs (Swagger):** `http://localhost:8000/docs`  
- **Docs (ReDoc):** `http://localhost:8000/redoc`

> **Importante sobre fechas:** Para **todos los endpoints**, debes pasar la fecha con `?fecha=YYYY-MM-DD` (por ejemplo, `?fecha=2024-09-15`).  
> En el caso de **TPM mensual**, usa **el día 01 del mes** (p. ej., `?fecha=2024-09-01`).

---

## Descripción Funcional

Este proyecto consulta el servicio **SIETE REST** del Banco Central de Chile utilizando las siguientes series temporales:

| Serie | Código | Descripción | Frecuencia |
|------|--------|-------------|------------|
| **TPM (Tasa de Política Monetaria)** | `F022.TPM.TIN.D001.NO.Z.M` | Tasa de interés mensual (%) | Mensual |
| **Tipo de cambio USD/CLP** | `F073.TCO.PRE.Z.D` | Dólar observado ($CLP por USD) | Diaria |

Estas series permiten:  
- Obtener tasas de política monetaria (TPM)  
- Obtener tipo de cambio observado (USD/CLP)  
- Evaluar la **UIP**, que relaciona diferenciales de tasas con depreciación esperada de la moneda

---

## Endpoints de la API

### 1) Obtener TPM mensual

**Endpoint:** `GET /bc/tpm`

**Descripción:** Devuelve la **TPM** del mes de la fecha indicada (usar el **día 01** del mes).  
**Parámetro:** `?fecha=YYYY-MM-DD`

**Ejemplo:**  
```
/bc/tpm?fecha=2024-09-01
```

**Respuesta (ejemplo):**
```json
{
  "fecha": "01-09-2024",
  "tpm": 11.25
}
```

**Códigos de estado:**  
- `200 OK` — Consulta exitosa  
- `404 Not Found` — No hay datos para esa fecha

---

### 2) Obtener TPM actual y del mes anterior

**Endpoint:** `GET /bc/tpm/variacion`

**Descripción:** Devuelve la **TPM** del mes indicado, la **TPM** del **mes anterior** y la **variación**.  
**Parámetro:** `?fecha=YYYY-MM-DD` (cualquier día del mes de interés)

**Ejemplo:**  
```
/bc/tpm/variacion?fecha=2024-09-15
```

**Respuesta (ejemplo):**
```json
{
  "fecha": "2024-09",
  "tpm": 11.25,
  "fecha_anterior": "2024-08",
  "tpm_anterior": 11.50,
  "variacion": -0.25
}
```

---

### 3) Obtener tipo de cambio USD/CLP

**Endpoint:** `GET /bc/usd`

**Descripción:** Devuelve el **dólar observado** (USD/CLP) del día indicado.  
**Parámetro:** `?fecha=YYYY-MM-DD`

**Ejemplo:**  
```
/bc/usd?fecha=2024-09-15
```

**Respuesta (ejemplo):**
```json
{
  "fecha": "15-09-2024",
  "usdclp": 918.24
}
```

> **Nota:** Fines de semana y feriados pueden no tener publicación.

---

### 4) Tipo de cambio con 30 días de diferencia

**Endpoint:** `GET /bc/usd/30d`

**Descripción:** Devuelve el **dólar del día** indicado y el de **~30 días antes**, además de la **variación**.  
**Parámetro:** `?fecha=YYYY-MM-DD`

**Ejemplo:**  
```
/bc/usd/30d?fecha=2024-09-15
```

**Respuesta (ejemplo):**
```json
{
  "fecha_actual": "15-09-2024",
  "usd_actual": 918.24,
  "fecha_30d": "16-08-2024",
  "usd_30d": 895.43,
  "variacion": 22.81,
}
```

---

### 5) Evaluación de Paridad de Tasas de Interés (UIP)

**Endpoint:** `GET /bc/uip`

**Descripción:** Evalúa si se cumple la **UIP** comparando movimientos de **TPM** y **USD**, asumiendo tasa externa constante.  
**Parámetro:** `?fecha=YYYY-MM-DD`

**Ejemplo:**  
```
/bc/uip?fecha=2024-09-15
```

**Respuesta (ejemplo):**
```json
{
  "tpm_actual": 11.25,
  "tpm_anterior": 11.50,
  "usd_actual": 918.24,
  "usd_anterior": 895.43,
  "fecha_tpm_actual": "2024-09",
  "fecha_tpm_anterior": "2024-08",
  "fecha_usd_actual": "15-09-2024",
  "fecha_usd_anterior": "16-08-2024",
  "cambio de la tpm": "negativo",
  "cambio del usd": "positivo",
  "comentario": "Se cumple la paridad: bajó la TPM y el peso se depreció (USD subió)."
}
```

---

## Ejemplos de Uso

**Ejemplo 1 — TPM mensual**
```bash
curl -X GET "http://localhost:8000/bc/tpm?fecha=2024-10-01"
```

**Ejemplo 2 — Variación mensual de TPM**
```bash
curl -X GET "http://localhost:8000/bc/tpm/variacion?fecha=2024-09-15"
```

**Ejemplo 3 — Dólar observado**
```bash
curl -X GET "http://localhost:8000/bc/usd?fecha=2024-09-15"
```

**Ejemplo 4 — Dólar y valor 30 días antes**
```bash
curl -X GET "http://localhost:8000/bc/usd/30d?fecha=2024-09-15"
```

**Ejemplo 5 — Evaluación UIP**
```bash
curl -X GET "http://localhost:8000/bc/uip?fecha=2024-09-15"
```

## Contexto Económico

La **UIP (Uncovered Interest Parity)** sugiere que:
> *Un aumento de la tasa de interés doméstica tiende a apreciar la moneda local (baja el USD/CLP), mientras que una baja en la tasa tiende a depreciarla.*

La API automatiza esta comprobación con datos reales del **BCCh** para apoyar análisis empírico.

---

## Buenas Prácticas para Estudiantes

- Usa siempre el formato de fecha: `?fecha=YYYY-MM-DD`  
- Para **TPM**, usa el **día 01** del mes (p. ej., `?fecha=2024-09-01`)  
- Considera feriados y fines de semana para el **USD**  
- Interpreta la salida combinando **variaciones** y **comentario** (UIP)  
- Convierte respuestas JSON a **pandas** para análisis/visualización

---

## Estructura del Proyecto

```
repoFastAPI/
├── apiDemo.py                 # App principal FastAPI
├── dominio_banco_central.py   # Funciones de conexión/transformación (BCCh)
├── routes/
│   ├── creditos.py            # Endpoints de créditos
│   └── banco_central.py       # Endpoints de TPM, USD y UIP
└── API_DOCUMENTACION.md       # Este archivo
```

---

## Solución de Problemas

**“Error de credenciales”**  
- Define `USER` y `PASS` en `dominio_banco_central.py` con tus credenciales del BCCh.


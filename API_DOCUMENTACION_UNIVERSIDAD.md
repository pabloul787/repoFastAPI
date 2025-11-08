#   Documentación del endpoint universidad

##   Resumen de Endpoints 

| # | Endpoint | Método | Parámetros | Descripción | Ejemplo de uso |
|---|---------|--------|------------|-------------|----------------|
| 1 | `/universidad/resumen` | GET | `{USER_ID}` | Entrega información sobre los registros academicos creados por el usuario | `/universidad/resumen/0` |
| 2 | `/universidad/nuevo_registro` | POST | Request Body que contenga: curso, sigla, usuario, año, semestre, nota | Crea registro academico nuevo | `/universidad/nuevo_registro/` |
| 3 | `/universidad/actualizar_registro` | PATCH | `{REGISTRO_ID}` y Request Body que contenga: curso, sigla, usuario, año, semestre, nota | Actualiza un registro academico ya creado | `/universidad/actualizar_registro/1` |

---

# Universidad — Documentación

## Descripción General

El endpoint **Universidad** permite conocer información sobre los estudiantes mediante el registro de sus cursos aprobados en una base de datos SQLite. Aqui los usuarios podran crear, conocer información y editar la información de sus cursos aprobados en la medida que lo necesiten.

Esta API demuestra la integración entre **Python**, **base de datos SQLite** y **uso cotidiano** para fines de Ciencia de Datos.

**URL base:** `http://localhost:8000`

**Tecnologías:**  
- **Framework:** FastAPI  
- **Librerías:** `typing`, `pandas`, `pydantic`
- **Versión de Python:** 3.10+

---

## Tabla de Contenidos

- [Inicio Rápido](#inicio-rápido)  
- [Descripción Funcional](#descripción-funcional)  
- [Endpoints de la API](#endpoints-de-la-api)   
- [Buenas Prácticas para Estudiantes](#buenas-prácticas-para-estudiantes)  
- [Estructura del Proyecto](#estructura-del-proyecto)  
- [Solución de Problemas](#solución-de-problemas)

---

## Inicio Rápido

### Instalación

```bash
# Instalar dependencias requeridas
pip install fastapi uvicorn pydantic typing

# Ejecutar la aplicación
uvicorn apiDemo:app --reload
```

### Acceso

- **Home:** `http://localhost:8000/`  
- **Docs (Swagger):** `http://localhost:8000/docs`  
- **Docs (ReDoc):** `http://localhost:8000/redoc`

---

## Descripción Funcional

Los endpoints disponibles para universidad permiten:  
- Conocer el resumen de los cursos aprobados por algún estudiante 
- Crear nuevos cursos aprobados en la base de datos para integrarlos a algún analisis mediantes queries.  
- Editar los registros para hacer simulaciones en caso que desee hacerlo.

---

## Endpoints de la API

### 1) Obtener un resumen del estudiante

**Endpoint:** `GET /universidad/resumen`

**Descripción:** Devuelve la información principal de los cursos aprobados por el estduainte  
**Parámetro:** `/{user_id}

**Ejemplo:**  
```
/universidad/resumen?/0
```

**Respuesta (ejemplo):**
```lista
[ 
  "ID: 1 | Curso: string | Sigla: string | Estudiante: Pablo Uribe | Nota: 3.0",
  "ID: 2 | Curso: Programacion | Sigla: EAA1220 | Estudiante: Pablo Uribe | Nota: 1.0",
  "ID: 3 | Curso: Microeconomia | Sigla: EAE1110 | Estudiante: Pablo Uribe | Nota: 6.1"
]
```

**Códigos de estado:**  

- `404 Not Found` — No hay registros para ese user id

---

### 2) Crear un nuevo registro academico

**Endpoint:** `POST /universidad/nuevo_registro`

**Descripción:** Permite registrar un nuevo curso aprobado incorporando su id, nombre, sigla, user_id, año, semestre y nota de aprobación a la base de datos SQLite.
**Request body:** se ingresan los valores del registro que queremos crear. Se debe editar el valor asociada al nombre de cada columna de la base de datos:
                    {
                    "curso": "string",
                    "sigla": "string",
                    "user": 0,
                    "año": 0,
                    "semestre": 0,
                    "nota": 0
                    }

**Ejemplo:**  
```
/universidad/nuevo_registro

request body:{
            "curso": "Ciencia de datos",
            "sigla": "EAE2520",
            "user": 0,
            "año": 2025,
            "semestre": 2,
            "nota": 6
            }
```

**Respuesta (ejemplo):**
```lista
[
  "Registro exitosamente creado:",
  [
    "Ciencia de datos",
    "EAA2520",
    0,
    2025,
    2,
    6
  ]
]
```

---

### 3) Actualizar un registro academico de la base de datos.

**Endpoint:** `PATCH /universidad/actualizar_registro`

**Descripción:** Permite editar algun registro academico creado anteriormente.
**Parámetro:** {id del registro}
**Request body:** Aquí debe ingresar la información a editar del registro deseado.
                    {
                    "curso": "string",
                    "sigla": "string",
                    "user": 0,
                    "año": 0,
                    "semestre": 0,
                    "nota": 0
                    }

**Ejemplo:**  
```
/universidad/actualizar_registro/1
```
Request Body: Quiero cambiar la nota de 6 a 7
                    {
                    "nota": 7
                    }
**Respuesta (ejemplo):**
```json
{
  "Mensaje": "Registro con ID 1 actualizado exitosamente.",
  "Campos actualizados": {
    "nota": 7
  }
}
```
## Buenas Prácticas para Estudiantes

- Siempre crea un registro antes de ver el resumen, de lo contrario, no habrá información para resumir.   
- Considera valores razonables para las variables, ej: en la notas de un curso, considerando el contetxo local, no se pueden ingresar letras.

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


## Solución de Problemas

**“Resumen vacio”**  
- Crea un registro antes y verifica luego utilizando el resumen que este bien creado.

**“ID no coincide”**  
- Asegurate de que al buscar el resumen o editar un registro, el ID exista en la base de datos.

from fastapi import FastAPI
import pandas as pd
from apifunctions import router_uni as universidad_router
from routes.universidad import router_uni as universidad_router
from routes.creditos import router as creditos_router
from routes.banco_central import router as bc_router
from contextlib import asynccontextmanager


from routes.universidad import crear_db

# --- 3. ADD THE LIFESPAN FUNCTION ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_db()
    yield
app = FastAPI(lifespan=lifespan)
app.include_router(universidad_router)
app.include_router(creditos_router)
app.include_router(bc_router)   


@app.get("/")
async def root():
    return "Bienvenido a nuestra API, aqui puedes registrar información academica tuya o tambien consultar información del banco central"
    

#@app.get("/universidad/{user_id}")
#def main_info(user_id:int):
   #return apifunctions.general_des(user_id)
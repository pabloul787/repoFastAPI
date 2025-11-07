from fastapi import FastAPI
import pandas as pd
from apifunctions import router_uni as universidad_router
from routes.universidad import router_uni as universidad_router
from routes.creditos import router as creditos_router
from routes.banco_central import router as bc_router
from contextlib import asynccontextmanager


from routes.universidad import crear_db # <-- 2. ADD THIS IMPORT

# --- 3. ADD THE LIFESPAN FUNCTION ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run ONCE on server startup
    print("Server is starting up...")
    crear_db()
    yield
app = FastAPI(lifespan=lifespan)
app.include_router(universidad_router)
app.include_router(creditos_router)
app.include_router(bc_router)   


@app.get("/")
async def root():
    return "Bienvenido, estos son los ID para consultar información sobre los estudiantes Pablo Uribe --> ID:0\nJoaquin Troncoso --> ID: 1"
    

#@app.get("/universidad/{user_id}")
#def main_info(user_id:int):
   #return apifunctions.general_des(user_id)
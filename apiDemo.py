from fastapi import FastAPI
import pandas as pd
from apifunctions import router_uni as universidad_router
from routes.creditos import router as creditos_router
app = FastAPI()

app.include_router(universidad_router)
app.include_router(creditos_router)

@app.get("/")
async def root():
    return "Bienvenido, estos son los ID para consultar información sobre los estudiantes Pablo Uribe --> ID:0\nJoaquin Troncoso --> ID: 1"
    

#@app.get("/universidad/{user_id}")
#def main_info(user_id:int):
   #return apifunctions.general_des(user_id)
from fastapi import FastAPI
import pandas as pd
import apifunctions

app = FastAPI()

db = pd.read_csv("demoDDBB.csv", sep=";")

@app.get("/")
async def root():
    return "Bienvenido, estos son los ID para consultar información sobre los estudiantes Pablo Uribe --> ID:0\nJoaquin Troncoso --> ID: 1"
    

@app.get("/universidad/{user_id}")
def main_info(user_id:int):
    return apifunctions.general_des(user_id)
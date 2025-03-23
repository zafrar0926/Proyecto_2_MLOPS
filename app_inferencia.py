from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import os
import pandas as pd

app = FastAPI()

# Ruta del pipeline entrenado
MODELO_PATH = "/app/modelos/modelo_rf.pkl"
pipeline = joblib.load(MODELO_PATH)

# Definir estructura de entrada (solo los campos originales sin codificar)
class DatosEntrada(BaseModel):
    Elevation: float
    Aspect: float
    Slope: float
    Horizontal_Distance_To_Hydrology: float
    Vertical_Distance_To_Hydrology: float
    Horizontal_Distance_To_Roadways: float
    Hillshade_9am: float
    Hillshade_Noon: float
    Hillshade_3pm: float
    Horizontal_Distance_To_Fire_Points: float
    Wilderness_Area: int
    Soil_Type: int

@app.get("/")
def home():
    return {"mensaje": "API de Inferencia - Modelo de cobertura forestal"}

@app.post("/predecir")
def predecir(data: DatosEntrada):
    entrada_df = pd.DataFrame([data.dict()])
    
    # Aplicar get_dummies como en el DAG
    entrada_df = pd.get_dummies(entrada_df, columns=["Wilderness_Area", "Soil_Type"])

    # Asegurar que tenga las mismas columnas que en el entrenamiento
    columnas_entrenamiento = pipeline.feature_names_in_
    for col in columnas_entrenamiento:
        if col not in entrada_df.columns:
            entrada_df[col] = 0  # si no existe, la agrega en 0

    entrada_df = entrada_df[columnas_entrenamiento]  # mismo orden de columnas

    pred = pipeline.predict(entrada_df)[0]
    return {"cover_type_predicho": int(pred)}



from fastapi import FastAPI
import mlflow.pyfunc

app = FastAPI()

# Cargar el modelo registrado en MLflow (ajustamos esto luego)
# model = mlflow.pyfunc.load_model("models:/mi_modelo_produccion/Production")

@app.get("/")
def home():
    return {"mensaje": "API de inferencia lista"}

@app.post("/predict")
def predict(input_data: dict):
    import pandas as pd
    df = pd.DataFrame([input_data])
    prediction = model.predict(df)
    return {"prediccion": prediction.tolist()}

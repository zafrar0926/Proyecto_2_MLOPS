from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import json
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import mlflow
import mlflow.sklearn
import joblib

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

def entrenar():
    # Leer todos los archivos JSON
    ruta_datos = '/opt/airflow/datos_raw'
    datos = []
    for archivo in os.listdir(ruta_datos):
        if archivo.endswith('.json'):
            with open(os.path.join(ruta_datos, archivo)) as f:
                lote = json.load(f)
                datos.extend(lote["data"])

    # Convertir a DataFrame
    columnas = ["Elevation", "Aspect", "Slope", "Horizontal_Distance_To_Hydrology",
                "Vertical_Distance_To_Hydrology", "Horizontal_Distance_To_Roadways",
                "Hillshade_9am", "Hillshade_Noon", "Hillshade_3pm",
                "Horizontal_Distance_To_Fire_Points", "Wilderness_Area",
                "Soil_Type", "Cover_Type"]
    df = pd.DataFrame(datos, columns=columnas)
    df = pd.get_dummies(df, columns=["Wilderness_Area", "Soil_Type"])

    # Preprocesamiento simple
    df = df.dropna()
    X = df.drop("Cover_Type", axis=1)
    y = df["Cover_Type"]

    # Entrenamiento
    modelo = RandomForestClassifier(n_estimators=100)
    modelo.fit(X, y)
    preds = modelo.predict(X)
    acc = accuracy_score(y, preds)

    # Registrar en MLflow
    mlflow.set_tracking_uri("http://mlflow:5000")
    mlflow.set_experiment("modelo_cobertura_bosque")

    with mlflow.start_run():
        mlflow.log_param("modelo", "RandomForest")
        mlflow.log_metric("accuracy", acc)
        mlflow.sklearn.log_model(modelo, "modelo_entrenado")

        # Guardar localmente por si se quiere servir en API
        joblib.dump(modelo, "/opt/airflow/modelos/modelo_rf.pkl")

    print(f"Entrenamiento finalizado con accuracy: {acc}")

with DAG(
    dag_id='entrenar_modelo',
    default_args=default_args,
    description='Entrena modelo a partir de los lotes',
    schedule_interval='@daily',
    catchup=False
) as dag:

    tarea_entrenar = PythonOperator(
        task_id='entrenar_modelo_rf',
        python_callable=entrenar
    )

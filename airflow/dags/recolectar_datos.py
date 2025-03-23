from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
import json
import os

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

def recolectar_lote():
    url = "http://172.17.0.1/data?group_number=1"
    response = requests.get(url)
    datos = response.json()
    
    os.makedirs("/opt/airflow/datos_raw", exist_ok=True)
    ruta = f"/opt/airflow/datos_raw/lote_{datos['batch_number']}.json"
    
    with open(ruta, "w") as f:
        json.dump(datos, f)

    print(f"Lote {datos['batch_number']} guardado en {ruta}")

# <<< ESTA ES LA CLAVE >>>
with DAG(
    dag_id='recolectar_datos_api',
    default_args=default_args,
    description='Recolección de datos por lotes desde API del profe',
    schedule_interval='@hourly',
    catchup=False
) as dag:

    tarea_recolectar = PythonOperator(
        task_id='extraer_datos',
        python_callable=recolectar_lote
    )



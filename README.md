# Proyecto MLOps - Clasificación de Cobertura Forestal 🌲

Este proyecto implementa un flujo completo de MLOps utilizando **Airflow**, **MLflow**, **MinIO**, y un servicio de inferencia con **FastAPI**, para entrenar y servir un modelo de clasificación de cobertura forestal.

---

## 📁 Estructura del Proyecto
```
mlops_proyecto2/
├── airflow/
│   ├── dags/                # DAGs de Airflow
│   ├── logs/                # Logs de Airflow
│   └── plugins/             # Plugins si se requieren
├── modelos/                 # Modelos entrenados (montado en los servicios)
├── datos_raw/               # Datos en JSON (montado en los servicios)
├── mlflow/                  # Carpeta para almacenar artefactos de MLflow
├── app_inferencia.py        # API FastAPI para servir el modelo
├── Dockerfile               # Dockerfile para FastAPI
├── app_streamlit.py        # API streamlit para servir la UI
├── Dockerfile.streamlit    # Dockerfile para streamlit
└── docker-compose.yml       # Orquestación de servicios
```

---

## ⚙️ Servicios que se levantan

Con `docker-compose up -d` se crean los siguientes servicios:

- **Airflow (webserver, scheduler, worker)**
- **MLflow + MySQL (backend store)**
- **MinIO (artifact store para MLflow)**
- **FastAPI (API para inferencia del modelo)**
- **Streamlit (Interfaz para API )**

---

## 🚀 Flujo de trabajo

### 1. 🧪 Preparar los datos

Guardar archivos `.json` en la carpeta `datos_raw/`. Cada archivo debe tener una estructura similar:
```json
{
  "data": [
    {
      "Elevation": 2800,
      "Aspect": 45,
      "Slope": 10,
      ...,
      "Wilderness_Area": 2,
      "Soil_Type": 3,
      "Cover_Type": 1
    },
    ...
  ]
}
```

---

### 2. ⚙️ Entrenar el modelo con Airflow

- DAG: `entrenar_modelo`
- Ejecuta `PythonOperator` que:
  - Lee todos los archivos JSON
  - Hace one-hot encoding de `Wilderness_Area` y `Soil_Type`
  - Entrena un `RandomForestClassifier`
  - Loguea el modelo en MLflow
  - Guarda el modelo como `modelos/modelo_rf.pkl`

✅ El modelo resultante espera **features one-hot encoded**.

---

### 3. 🔮 Servir el modelo con FastAPI

#### app_inferencia.py
- Carga el modelo `modelos/modelo_rf.pkl`
- Preprocesa la entrada haciendo one-hot encoding **dinámico**
- Rellena con ceros las columnas faltantes
- Devuelve la predicción

### Ejemplo de request:
```bash
curl -X POST http://localhost:8000/predecir \
  -H "Content-Type: application/json" \
  -d '{
    "Elevation": 3000,
    "Aspect": 45,
    "Slope": 10,
    "Horizontal_Distance_To_Hydrology": 100,
    "Vertical_Distance_To_Hydrology": 50,
    "Horizontal_Distance_To_Roadways": 200,
    "Hillshade_9am": 200,
    "Hillshade_Noon": 220,
    "Hillshade_3pm": 180,
    "Horizontal_Distance_To_Fire_Points": 150,
    "Wilderness_Area": 1,
    "Soil_Type": 2
  }'
```

Respuesta esperada:
```json
{
  "cover_type_predicho": 1
}
```

---

## 🐳 Comandos útiles

- **Levantar todos los servicios**:
  ```bash
  sudo docker compose up --build -d
  ```

- **Ver logs del API de inferencia**:
  ```bash
  sudo docker logs -f api-inferencia
  ```

- **Reconstruir solo FastAPI**:
  ```bash
  sudo docker compose up --build -d api-inferencia
  ```
## 🛠️ Solución de problemas

- **❗ Error de permisos en logs de Airflow**

Si ves errores tipo Operation not permitted en los logs:
```bash
chmod -R 777 ./airflow/logs
```

Esto otorga permisos de escritura al contenedor de Airflow sobre la carpeta de logs montada desde tu sistema.
---

## 📌 Notas adicionales

- Se requiere `pandas` y `scikit-learn` en el contenedor de FastAPI
- Se debe montar el modelo entrenado en la ruta `/app/modelos/modelo_rf.pkl`
- La predicción fallará si no se hace preprocessing compatible con el entrenamiento

---

## ✅ Checklist final

- [x] Datos preparados en `datos_raw/`
- [x] DAG `entrenar_modelo` ejecutado con éxito
- [x] Modelo almacenado localmente y en MLflow
- [x] API FastAPI sirviendo correctamente
- [x] Inferencia funcionando con entrada cruda (preprocesada dentro del API)

---

Hecho por Edwin A. Caro, Andres F. Matallana, Santiago Zafra R

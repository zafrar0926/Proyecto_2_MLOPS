# Proyecto 2 - MLOps con Airflow, MLflow, MinIO y Docker Compose

Este proyecto implementa una arquitectura de MLOps que permite:
- Recolectar datos desde una API simulada.
- Almacenar datos crudos en volúmenes compartidos.
- Entrenar modelos desde Airflow.
- Registrar experimentos en MLflow.
- Almacenar artefactos en MinIO.

## Requisitos previos

- Docker
- Docker Compose

## Estructura de carpetas

```
├── airflow/
│   ├── dags/                # DAGs de Airflow
│   ├── logs/                # Logs de ejecución
│   └── plugins/             # Plugins personalizados (opcional)
├── datos_raw/               # Carpeta montada para datos crudos
├── modelos/                 # Carpeta montada para modelos entrenados
├── mlflow/                  # Carpeta para la metadata de MLflow
├── docker-compose.yml       # Orquestación de servicios
```

## Servicios utilizados

- **Airflow (webserver, scheduler, worker, init)**
- **PostgreSQL** como backend de Airflow
- **Redis** como broker de Celery
- **MinIO** para artefactos
- **MySQL** como backend de MLflow
- **MLflow** para gestión de experimentos

## Pasos para ejecutar

### 1. Crear carpetas necesarias y otorgar permisos
```bash
mkdir -p airflow/dags airflow/logs airflow/plugins datos_raw modelos mlflow
chmod 777 datos_raw modelos mlflow
```

### 2. Lanzar servicios
```bash
sudo docker-compose up -d --build
```

### 3. Verificar estado
Accede a:
- Airflow: [http://localhost:8080](http://localhost:8080) (user: `airflow`, pass: `airflow`)
- MLflow: [http://localhost:5000](http://localhost:5000)
- MinIO: [http://localhost:9001](http://localhost:9001) (user: `minioadmin`, pass: `minioadmin`)

### 4. DAGs disponibles

- `recolectar_datos_api`: extrae datos desde API simulada y los guarda en `datos_raw`.
- `entrenar_modelo`: entrena un modelo de RandomForest con los datos crudos y lo registra en MLflow.

### 5. Solución de errores comunes

- **PermissionError** al guardar modelo: otorgar permisos a carpeta `modelos`.
- **NoSuchBucket (S3)**: Crear bucket `mlflow` en la consola de MinIO.
- **mlflow.exceptions.MissingConfigException**: asegurarse que las variables de entorno estén bien en `docker-compose.yml`.

### 6. Crear bucket "mlflow" en MinIO (una sola vez)

Ingresar a `http://localhost:9001`, autenticarse y crear un bucket llamado `mlflow`.

---

Listo. El entorno está completamente funcional.



# Proyecto_2_MLOPS

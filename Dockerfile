# Dockerfile para servicio de inferencia
FROM python:3.9

WORKDIR /app

# Copiar archivos necesarios
COPY app_inferencia.py .
COPY modelos ./modelos
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto donde correrá FastAPI
EXPOSE 8000

# Comando para iniciar FastAPI
CMD ["uvicorn", "app_inferencia:app", "--host", "0.0.0.0", "--port", "8000"]


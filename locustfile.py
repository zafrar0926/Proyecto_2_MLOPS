from locust import HttpUser, task, between

class UsuarioDeCarga(HttpUser):
    wait_time = between(1, 2.5)  # Tiempo entre requests por usuario

    @task
    def hacer_inferencia(self):
        payload = {
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
        }

        response = self.client.post("/predecir", json=payload)

        if response.status_code != 200:
            print("❌ Error en la inferencia:", response.text)

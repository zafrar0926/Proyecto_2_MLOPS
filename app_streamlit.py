import streamlit as st
import requests

st.set_page_config(page_title="Clasificación de Cobertura Forestal", layout="centered")

st.title("🌲 Predicción de Tipo de Cobertura Forestal")
st.markdown("Esta aplicación permite ingresar datos y obtener predicciones usando el modelo entrenado.")

with st.form("form_prediccion"):
    st.subheader("📝 Ingrese los datos de entrada")
    elevation = st.number_input("Elevación", value=2800)
    aspect = st.number_input("Aspecto", value=45)
    slope = st.number_input("Pendiente", value=10)
    dist_hydrology_h = st.number_input("Distancia Horizontal a Hidrología", value=100)
    dist_hydrology_v = st.number_input("Distancia Vertical a Hidrología", value=50)
    dist_roadways = st.number_input("Distancia a Caminos", value=200)
    hillshade_9am = st.slider("Hillshade 9am", 0, 255, 200)
    hillshade_noon = st.slider("Hillshade mediodía", 0, 255, 220)
    hillshade_3pm = st.slider("Hillshade 3pm", 0, 255, 180)
    dist_fire_points = st.number_input("Distancia a puntos de fuego", value=150)
    wilderness_area = st.selectbox("Área silvestre", [0, 1, 2, 3])
    soil_type = st.selectbox("Tipo de suelo", list(range(0, 40)))

    submitted = st.form_submit_button("🔮 Predecir")

if submitted:
    entrada = {
        "Elevation": elevation,
        "Aspect": aspect,
        "Slope": slope,
        "Horizontal_Distance_To_Hydrology": dist_hydrology_h,
        "Vertical_Distance_To_Hydrology": dist_hydrology_v,
        "Horizontal_Distance_To_Roadways": dist_roadways,
        "Hillshade_9am": hillshade_9am,
        "Hillshade_Noon": hillshade_noon,
        "Hillshade_3pm": hillshade_3pm,
        "Horizontal_Distance_To_Fire_Points": dist_fire_points,
        "Wilderness_Area": wilderness_area,
        "Soil_Type": soil_type
    }

    try:
        response = requests.post("http://api-inferencia:8000/predecir", json=entrada)
        if response.status_code == 200:
            pred = response.json()["cover_type_predicho"]
            st.success(f"✅ Tipo de cobertura forestal predicho: **{pred}**")
        else:
            st.error("❌ Error en la respuesta del servidor FastAPI.")
    except Exception as e:
        st.error(f"⚠️ No se pudo conectar con FastAPI: {e}")

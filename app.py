import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

st.title("Control de Ambientes de Relajación")
st.write("Versión de Python:", platform.python_version())

broker="157.230.214.127"
port=1883

def publicar(topico, mensaje):
    client = paho.Client("StreamlitApp")
    client.connect(broker, port)
    client.publish(topico, json.dumps(mensaje))
    client.disconnect()

# Selección de ambiente
ambiente = st.radio(
    "Selecciona un ambiente:",
    ("Selva", "Desierto", "Personalizado")
)

# ---------- AMBIENTE SELVA ----------
if ambiente == "Selva":
    st.subheader("🌿 Ambiente Selva (Predeterminado)")
    st.write("""
    - Luz: Verde suave  
    - Sonido: Lluvia + Pájaros  
    - Temperatura: 22°C  
    - Humidificador: Alto  
    """)

    if st.button("Activar Selva"):
        publicar("cmqtt_env", {
            "ambiente": "selva",
            "luz": "verde",
            "sonido": "lluvia aves",
            "temperatura": 22,
            "humidificador": "alto"
        })
        st.success("Ambiente Selva Activado")


# ---------- AMBIENTE DESIERTO ----------
elif ambiente == "Desierto":
    st.subheader("🏜️ Ambiente Desierto (Predeterminado)")
    st.write("""
    - Luz: Ámbar cálido  
    - Sonido: Viento suave  
    - Temperatura: 28°C  
    - Humidificador: Bajo  
    """)

    if st.button("Activar Desierto"):
        publicar("cmqtt_env", {
            "ambiente": "desierto",
            "luz": "ambar",
            "sonido": "viento",
            "temperatura": 28,
            "humidificador": "bajo"
        })
        st.success("Ambiente Desierto Activado")


# ---------- AMBIENTE PERSONALIZADO ----------
elif ambiente == "Personalizado":
    st.subheader("🎨 Ambiente Personalizable")

    luz = st.selectbox("Color de Luz:", ["Rojo", "Azul", "Verde", "Ámbar", "Blanco"])
    sonido = st.selectbox("Tipo de Sonido:", ["Lluvia", "Viento suave", "Instrumental", "Silencio"])
    temperatura = st.slider("Temperatura (°C):", 16, 32, 24)
    humidificador = st.select_slider("Nivel Humidificador:", options=["Apagado", "Bajo", "Medio", "Alto"])

    if st.button("Activar Personalizado"):
        publicar("cmqtt_env", {
            "ambiente": "personalizado",
            "luz": luz.lower(),
            "sonido": sonido.lower(),
            "temperatura": temperatura,
            "humidificador": humidificador.lower()
        })
        st.success("Ambiente Personalizado Activado")

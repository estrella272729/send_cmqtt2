import streamlit as st
from streamlit_player import st_player
import paho.mqtt.client as paho
import json

# ========== CONFIG MQTT ==========
broker = "broker.mqttdashboard.com"
port = 1883
topic = "spa_relax/control"
client_name = "cliente_spa_relax"

client = paho.Client(client_name)

def enviar_mqtt(data):
    client.connect(broker, port)
    mensaje = json.dumps(data)
    client.publish(topic, mensaje)
    st.success("✅ Comando enviado a la maqueta")

# ========== CONFIG APP ==========
st.set_page_config(page_title="Spa Multimodal", page_icon="🌿", layout="wide")
st.title("🌿 ESPACIO DE RELAJACIÓN MULTIMODAL")


# ---- DEFINICIÓN DE AMBIENTES ----
ambientes = {
    "🌴 Selva (Automático)": {
        "bg": "https://images.unsplash.com/photo-1501785888041-af3ef285b470",
        "musica": "https://www.youtube.com/watch?v=OdIJ2x3nxzQ",
        "config": {"color":"#00AA55","temp":20,"hum":"Alto"},
        "editable": False
    },
    "🏜️ Desierto (Automático)": {
        "bg": "https://images.unsplash.com/photo-1508264165352-258a6f039317",
        "musica": "https://www.youtube.com/watch?v=2OEL4P1Rz04",
        "config": {"color":"#D29944","temp":30,"hum":"Bajo"},
        "editable": False
    },
    "🕯️ Zen Personalizable": {
        "bg": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e",
        "musica": "https://www.youtube.com/watch?v=lFcSrYw-ARY",
        "editable": True
    }
}

ambiente = st.selectbox("Seleccione un ambiente:", ambientes.keys())
data = ambientes[ambiente]

# Fondo dinámico
st.markdown(f"""
<style>
.stApp {{
    background-image: url("{data['bg']}");
    background-size: cover;
    background-attachment: fixed;
}}
</style>
""", unsafe_allow_html=True)

# Música ambiente
st_player(data["musica"])

# ---- MODO AUTOMÁTICO ----
if not data["editable"]:
    st.subheader("🌱 Ambiente Automático")
    st.write(f"**Color de luz:** {data['config']['color']}")
    st.write(f"**Temperatura:** {data['config']['temp']} °C")
    st.write(f"**Humidificador:** {data['config']['hum']}")

    if st.button("✨ Activar Ambiente"):
        enviar_mqtt(data["config"])


# ---- MODO PERSONALIZADO ----
else:
    st.subheader("🎨 Personalizar Ambiente Zen")

    color = st.color_picker("Color de la luz", "#FFFFFF")
    temp = st.slider("Temperatura (°C)", 18, 35, 24)
    hum = st.selectbox("Humidificador (LED):", ["Apagado", "Alto"])

    if st.button("💾 Enviar a la Maqueta"):
        config = {"color":color, "temp":temp, "hum":hum}
        enviar_mqtt(config)

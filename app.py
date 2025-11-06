import streamlit as st
from streamlit_player import st_player
import paho.mqtt.client as paho
import json
import platform

# ==========================
# CONFIG MQTT
# ==========================
broker = "broker.mqttdashboard.com"
port = 1883
client_name = "spa_relax_room"

client = paho.Client(client_name)

def publish(topic, payload):
    client.connect(broker, port)
    client.publish(topic, payload)

# ==========================
# STREAMLIT UI CONFIG
# ==========================
st.set_page_config(page_title="Spa Multimodal IoT", page_icon="🌿", layout="wide")

# ==========================
# CSS SPA ZEN
# ==========================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #d9f2e6, #ffffff);
    background-attachment: fixed;
}
.card {
    background: rgba(255,255,255,0.6);
    padding: 25px;
    border-radius: 18px;
    backdrop-filter: blur(6px);
    box-shadow: 0px 6px 25px rgba(0,0,0,0.18);
    margin-top: 20px;
    animation: fadein 0.8s ease;
}
@keyframes fadein {
  from { opacity:0; transform: translateY(8px); }
  to { opacity:1; transform: translateY(0); }
}
.stButton>button {
    background: #7fc7a9 !important;
    color: white !important;
    border-radius: 14px !important;
    padding: 10px 20px !important;
    border: none !important;
    transition: 0.3s;
    font-size: 18px;
}
.stButton>button:hover {
    transform: scale(1.05);
    background: #6dbb97 !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================
# TITLE
# ==========================
st.markdown("<h1 style='text-align:center;'>🌿 SPA DE RELAJACIÓN MULTIMODAL IoT</h1>", unsafe_allow_html=True)
st.caption("Ambientes conectados a tu maqueta real vía MQTT (Wokwi / Arduino)")

# ==========================
# AMBIENTES
# ==========================
ambientes = {
    "🌴 Selva (Automático)": {
        "color": "#00AA55",
        "temperatura": 20,
        "humidificador": "ON",
        "musica": "https://www.youtube.com/watch?v=OdIJ2x3nxzQ"
    },
    "🏜️ Desierto (Automático)": {
        "color": "#D29944",
        "temperatura": 30,
        "humidificador": "OFF",
        "musica": "https://www.youtube.com/watch?v=2OEL4P1Rz04"
    },
    "🕯️ Zen Personalizable": {
        "musica": "https://www.youtube.com/watch?v=lFcSrYw-ARY"
    }
}

st.subheader("✨ Selecciona el ambiente de relajación")
seleccion = st.selectbox("", ambientes.keys())
data = ambientes[seleccion]

# Música del ambiente
st_player(data["musica"])

# ==========================
# AUTOMÁTICOS
# ==========================
if seleccion != "🕯️ Zen Personalizable":
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.write(f"**Luz:** {data['color']}")
    st.write(f"**Temperatura:** {data['temperatura']} °C")
    st.write(f"**Humidificador:** {data['humidificador']}")

    if st.button("✨ Activar este ambiente"):
        payload = json.dumps({
            "color": data["color"],
            "temp": data["temperatura"],
            "humidificador": data["humidificador"]
        })
        publish("spa_iot_control", payload)
        st.success("✅ Ambiente enviado a la maqueta")

    st.markdown("</div>", unsafe_allow_html=True)

# ==========================
# PERSONALIZABLE
# ==========================
else:
    st.markdown("<h3>🎨 Personaliza tu ambiente</h3>")

    luz = st.color_picker("Color de iluminación", "#ffffff")
    temp = st.slider("Temperatura (°C)", 18, 35, 25)
    hum = st.selectbox("Humidificador (LED)", ["OFF", "ON"])

    user_music = st.text_input("🎧 Opcional: Pega enlace de YouTube para música personalizada:")

    if user_music:
        st_player(user_music)

    if st.button("💾 Enviar configuración personalizada"):
        payload = json.dumps({
            "color": luz,
            "temp": temp,
            "humidificador": hum
        })
        publish("spa_iot_control", payload)
        st.success("✅ Configuración enviada a la maqueta")


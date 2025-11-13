import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# Muestra la versión de Python
st.write("Versión de Python:", platform.python_version())

act1 = "OFF"
message_received = ""

# --- Callbacks MQTT ---
def on_publish(client, userdata, result):
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write("Mensaje recibido:", message_received)

# Datos del broker
broker = "157.230.214.127"
port = 1883

client1 = paho.Client("GIT-HUB")
client1.on_message = on_message

st.title("MQTT Control")

# ==============================
#      AMBIENTES PREDEFINIDOS
# ==============================

st.header("Ambientes predeterminados")

# Valores predefinidos (puedes cambiarlos)
AMBIENTE_1_TEMP = 22.0
AMBIENTE_2_TEMP = 28.0

col_a1, col_a2 = st.columns(2)

with col_a1:
    st.subheader("Ambiente 1")
    st.write("Temperatura: ", AMBIENTE_1_TEMP, "°C")
    if st.button("Encender ambiente 1"):
        client = paho.Client("GIT-HUB")
        client.on_publish = on_publish
        client.connect(broker, port)

        # Enciende humificador
        msg_hum = json.dumps({"Act1": "ON"})
        client.publish("cmqtt_s", msg_hum)

        # Envía temperatura predeterminada
        msg_temp = json.dumps({"Temperatura": AMBIENTE_1_TEMP})
        client.publish("cmqtt_a", msg_temp)

with col_a2:
    st.subheader("Ambiente 2")
    st.write("Temperatura: ", AMBIENTE_2_TEMP, "°C")
    if st.button("Encender ambiente 2"):
        client = paho.Client("GIT-HUB")
        client.on_publish = on_publish
        client.connect(broker, port)

        # Enciende humificador
        msg_hum = json.dumps({"Act1": "ON"})
        client.publish("cmqtt_s", msg_hum)

        # Envía temperatura predeterminada
        msg_temp = json.dumps({"Temperatura": AMBIENTE_2_TEMP})
        client.publish("cmqtt_a", msg_temp)

# ==============================
#   AMBIENTE 3 PERSONALIZABLE
# ==============================
st.header("Ambiente 3 (personalizable)")

# --------- CONTROL HUMIFICADOR (ON / OFF) ----------
st.subheader("Humificador")

col1, col2 = st.columns(2)

with col1:
    if st.button('Encender humificador (Ambiente 3)'):
        act1 = "ON"
        client = paho.Client("GIT-HUB")
        client.on_publish = on_publish
        client.connect(broker, port)
        message = json.dumps({"Act1": act1})
        client.publish("cmqtt_s", message)

with col2:
    if st.button('Apagar humificador (Ambiente 3)'):
        act1 = "OFF"
        client = paho.Client("GIT-HUB")
        client.on_publish = on_publish
        client.connect(broker, port)
        message = json.dumps({"Act1": act1})
        client.publish("cmqtt_s", message)

# --------- CONTROL DE TEMPERATURA (PERSONALIZABLE) ----------
st.subheader("Control de temperatura (Ambiente 3)")

temperatura = st.slider(
    'Selecciona la temperatura (°C)',
    10.0,   # mínimo
    40.0,   # máximo
    25.0    # valor inicial
)
st.write('Temperatura seleccionada:', temperatura, "°C")

if st.button('Enviar temperatura (Ambiente 3)'):
    client = paho.Client("GIT-HUB")
    client.on_publish = on_publish
    client.connect(broker, port)
    message = json.dumps({"Temperatura": float(temperatura)})
    client.publish("cmqtt_a", message)

# ==============================
#   REPRODUCCIÓN DE AUDIOS
# ==============================
st.header("Reproducción de audios")

audios = {
    "Sonido de pajaros": "bird.mp3",
    "Sonido de lluvia": "rain.mp3",
    "Sonido instrumental": "instrumental.mp3",
}

opcion_audio = st.selectbox("Elige un audio para reproducir", list(audios.keys()))

st.audio(audios[opcion_audio], format="audio/mp3")


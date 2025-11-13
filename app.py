import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# Muestra la versión de Python
st.write("Versión de Python:", platform.python_version())

values = 0.0
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

client1 = paho.Client("GIT-ANGIE")
client1.on_message = on_message

st.title("MQTT Control")

# --------- CONTROL HUMIFICADOR (ON / OFF) ----------
st.subheader("Humificador")

col1, col2 = st.columns(2)

with col1:
    if st.button('Encender humificador'):
        act1 = "ON"
        client1 = paho.Client("GIT-ANGIE")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        ret = client1.publish("cmqtt_spa", message)
    else:
        st.write('')

with col2:
    if st.button('Apagar humificador'):
        act1 = "OFF"
        client1 = paho.Client("GIT-ANGIE")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        ret = client1.publish("cmqtt_spa", message)
    else:
        st.write('')

# --------- CONTROL DE LUZ (ON / OFF) ----------
st.subheader("Luz")

col3, col4 = st.columns(2)

with col3:
    if st.button('Encender luz'):
        client1 = paho.Client("GIT-ANGIE")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Luz": "ON"})
        ret = client1.publish("cmqtt_spa3", message)
    else:
        st.write('')

with col4:
    if st.button('Apagar luz'):
        client1 = paho.Client("GIT-ANGIE")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Luz": "OFF"})
        ret = client1.publish("cmqtt_spa3", message)
    else:
        st.write('')

# --------- CONTROL DE TEMPERATURA ----------
st.subheader("Control de temperatura")

temperatura = st.slider(
    'Selecciona la temperatura (°C)',
    10.0,   # mínimo
    40.0,   # máximo
    25.0    # valor inicial
)
st.write('Temperatura seleccionada:', temperatura, "°C")

if st.button('Enviar temperatura'):
    client1 = paho.Client("GIT-ANGIE")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    # Enviamos la temperatura como JSON
    message = json.dumps({"Temperatura": float(temperatura)})
    ret = client1.publish("cmqtt_spa2", message)
else:
    st.write('')

# --------- REPRODUCCIÓN DE AUDIOS DESDE GITHUB ----------
st.header("Reproducción de audios")

audios = {
    "Sonido de pajaros": "bird.mp3",
    "Sonido de lluvia": "rain.mp3",
    "Sonido instrumental": "instrumental.mp3",
}

opcion_audio = st.selectbox("Elige un audio para reproducir", list(audios.keys()))

st.audio(audios[opcion_audio], format="audio/mp3")


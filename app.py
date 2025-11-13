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

client1 = paho.Client("GIT-HUB")
client1.on_message = on_message

st.title("MQTT Control")

# --------- CONTROL ON / OFF DIGITAL ----------
if st.button('ON'):
    act1 = "ON"
    client1 = paho.Client("GIT-HUB")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Act1": act1})
    ret = client1.publish("cmqtt_s", message)
else:
    st.write('')

if st.button('OFF'):
    act1 = "OFF"
    client1 = paho.Client("GIT-HUB")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Act1": act1})
    ret = client1.publish("cmqtt_s", message)
else:
    st.write('')

# --------- ENVÍO DE VALOR ANALÓGICO ----------
values = st.slider('Selecciona el rango de valores', 0.0, 100.0)
st.write('Values:', values)

if st.button('Enviar valor analógico'):
    client1 = paho.Client("GIT-HUB")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Analog": float(values)})
    ret = client1.publish("cmqtt_a", message)
else:
    st.write('')

# --------- REPRODUCCIÓN DE AUDIOS DESDE GITHUB ----------
st.header("Reproducción de audios")

# Diccionario de audios: NOMBRE VISIBLE -> URL RAW DEL ARCHIVO EN GITHUB
audios = {
    "Audio 1": "bird.mp3",
    "Audio 2": "rain.mp3",
    # Añade más audios aquí...
}

opcion_audio = st.selectbox("Elige un audio para reproducir", list(audios.keys()))

# Muestra el reproductor de audio
st.audio(audios[opcion_audio], format="audio/mp3")

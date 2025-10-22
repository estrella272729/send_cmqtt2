import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# ==========================
# CONFIGURACIÓN GENERAL
# ==========================
broker = "broker.mqttdashboard.com"
port = 1883
client_name = "angie_farm"

# ==========================
# CALLBACKS
# ==========================
def on_publish(client, userdata, result):
    print("✅ Dato publicado correctamente\n")

def on_message(client, userdata, message):
    global message_received
    message_received = str(message.payload.decode("utf-8"))
    st.info(f"📩 Mensaje desde la granja: {message_received}")

# ==========================
# CLIENTE MQTT
# ==========================
client1 = paho.Client(client_name)
client1.on_message = on_message
client1.on_publish = on_publish

# ==========================
# INTERFAZ
# ==========================
st.set_page_config(page_title="Granja Inteligente IoT", page_icon="🌾")
st.title("🌾 Panel IoT - Granja Inteligente")
st.caption("Controla tu granja desde el navegador usando MQTT + Wokwi 🐄🐖🐓")
st.write("Versión de Python:", platform.python_version())

# ==========================
# SECCIÓN: CONTROL DE SISTEMAS
# ==========================
st.header("💡 Control de sistemas automáticos")

col1, col2 = st.columns(2)

with col1:
    if st.button("☀️ Encender luces del establo"):
        act1 = "ON"
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        client1.publish("cmqtt_angies", message)
        st.success("Las luces del establo fueron encendidas 🌞")

with col2:
    if st.button("🌙 Apagar luces del establo"):
        act1 = "OFF"
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        client1.publish("cmqtt_angies", message)
        st.warning("Las luces del establo se apagaron 🌙")

# ==========================
# SECCIÓN: CONTROL ANALÓGICO
# ==========================
st.header("💧 Control del riego automático")

values = st.slider("Selecciona el nivel de riego 💦", 0.0, 100.0, 50.0)
st.write(f"Nivel actual de riego: **{values:.1f}%**")

if st.button("🚜 Enviar nivel de riego"):
    client1.connect(broker, port)
    message = json.dumps({"Analog": float(values)})
    client1.publish("cmqtt_angiel", message)
    st.info(f"💧 Nivel de riego actualizado a {values:.1f}%")

# ==========================
# INFORMACIÓN EXTRA
# ==========================
st.divider()
st.subheader("📡 Estado del sistema")
st.write("Broker:", broker)
st.write("Puerto:", port)
st.caption("Desarrollado por Angie 💻 | Proyecto de Comunicación IoT con MQTT y Wokwi 🌍")




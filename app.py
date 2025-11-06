import paho.mqtt.client as paho
import streamlit as st
import json
import platform

st.set_page_config(page_title="Ambientes de Relajación", page_icon="🌿", layout="centered")
st.write("Versión de Python:", platform.python_version())

broker = "157.230.214.127"
port = 1883

def publicar(topico, mensaje):
    client = paho.Client("StreamlitApp")
    client.connect(broker, port)
    client.publish(topico, json.dumps(mensaje))
    client.disconnect()

st.title("🌿 Espacio de Relajación Multimodal")

ambiente = st.radio("Selecciona un ambiente:", ["Selva", "Desierto", "Personalizado"])

if ambiente == "Selva":
    st.subheader("🌿 Ambiente Selva")
    st.write("Luz verde suave, sonidos de aves, temperatura 22°C, humidificador ON")
    # reproducir sonido de pájaros
    audio_file = "birds.mp3"
    st.audio(audio_file, format='audio/mp3')
    if st.button("Activar Selva"):
        publicar("cmqtt_env", {
            "ambiente": "selva",
            "luz": "verde",
            "sonido": "aves",
            "temperatura": 22,
            "humidificador": "on"
        })
        st.success("✅ Selva activada")

elif ambiente == "Desierto":
    st.subheader("🏜️ Ambiente Desierto")
    st.write("Luz ámbar cálida, sonido de viento, temperatura 28°C, humidificador OFF")
    # reproducir sonido de viento
    audio_file = "wind.mp3"
    st.audio(audio_file, format='audio/mp3')
    if st.button("Activar Desierto"):
        publicar("cmqtt_env", {
            "ambiente": "desierto",
            "luz": "ambar",
            "sonido": "viento",
            "temperatura": 28,
            "humidificador": "off"
        })
        st.success("✅ Desierto activado")

else:  # Personalizado
    st.subheader("🎨 Ambiente Personalizado")
    luz = st.color_picker("Selecciona color de luz:", "#ffffff")
    sonido_select = st.selectbox("Sonido:", ["Lluvia", "Viento", "Instrumental", "Silencio"])
    temperatura = st.slider("Temperatura (°C):", 16, 32, 24)
    humidificador = st.radio("Humidificador:", ["ON", "OFF"])

    # reproducir el sonido elegido
    if sonido_select != "Silencio":
        audio_file = f"{sonido_select.lower()}.mp3"
        st.audio(audio_file, format='audio/mp3')
    else:
        st.write("🔇 Silencio seleccionado")

    if st.button("Activar Personalizado"):
        publicar({
            "ambiente": "personalizado",
            "luz": luz,
            "sonido": sonido_select.lower(),
            "temperatura": temperatura,
            "humidificador": humidificador.lower()
        })
        st.success("✅ Ambiente personalizado activado")


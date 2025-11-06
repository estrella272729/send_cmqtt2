import paho.mqtt.client as paho
import streamlit as st
import json
import base64
from streamlit_lottie import st_lottie
import requests

st.set_page_config(page_title="Ambientes de Relajación", page_icon="🌿", layout="centered")

# -------- ESTILOS --------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #D6E8D2 0%, #FFFFFF 100%);
}
.card {
    padding: 25px;
    border-radius: 18px;
    background: rgba(255,255,255,0.55);
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255,255,255,0.4);
    margin: 18px 0;
}
h1, h2, h3, label, p {
    font-family: 'Segoe UI', sans-serif;
}
</style>
""", unsafe_allow_html=True)

# -------- MQTT --------
broker = "157.230.214.127"
port = 1883

def publicar(topico, mensaje):
    client = paho.Client("SPA_APP")
    client.connect(broker, port)
    client.publish(topico, json.dumps(mensaje))
    client.disconnect()

# -------- LOTTIE ANIMACIONES --------
def load_lottie(url):
    r = requests.get(url)
    return r.json()

lottie_selva = load_lottie("https://lottie.host/0a0cd1a5-0be2-4a67-b3bf-f50e0826ea09/nNJOxvUq9e.json")
lottie_desierto = load_lottie("https://lottie.host/a33a8cf7-1421-49ca-929b-1ecf26fb3ce1/qEYO09tU6F.json")
lottie_custom = load_lottie("https://lottie.host/ae0bb41f-6eab-4f9a-ac04-734b4d542f72/3mvmWm8hRw.json")

# -------- UI --------
st.title("🌿 Espacio de Relajación Multimodal")

ambiente = st.radio("Selecciona un ambiente:", ["Selva", "Desierto", "Personalizado"])

# -------- SELVA --------
if ambiente == "Selva":
    st_lottie(lottie_selva, height=200)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🌿 Ambiente Selva")
    st.write("Sonido de pájaros, luz verde suave y aire fresco 🌱")
    st.audio("birds.mp3")
    if st.button("Activar Selva"):
        publicar("cmqtt_env", {"ambiente": "selva", "luz": "verde", "sonido": "pajaros", "temperatura": 22, "humidificador": "on"})
        st.success("✨ Selva activada")
    st.markdown('</div>', unsafe_allow_html=True)

# -------- DESIERTO --------
elif ambiente == "Desierto":
    st_lottie(lottie_desierto, height=200)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🏜️ Ambiente Desierto")
    st.write("Luz ámbar cálida, viento suave, atmósfera templada 🌬️")
    st.audio("wind.mp3")
    if st.button("Activar Desierto"):
        publicar("cmqtt_env", {"ambiente": "desierto", "luz": "ambar", "sonido": "viento", "temperatura": 28, "humidificador": "off"})
        st.success("🔥 Desierto activado")
    st.markdown('</div>', unsafe_allow_html=True)

# -------- PERSONALIZADO --------
else:
    st_lottie(lottie_custom, height=200)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎨 Ambiente Personalizado")

    luz = st.color_picker("Color de luz ambiental:", "#F5EEDC")
    sonido = st.selectbox("Sonido:", ["Lluvia", "Viento", "Instrumental", "Pájaros", "Silencio"])
    temperatura = st.slider("Temperatura:", 16, 32, 24)
    humidificador = st.radio("Humidificador:", ["ON", "OFF"])

    # Audio dinámico
    if sonido != "Silencio":
        st.audio(f"{sonido.lower()}.mp3")

    if st.button("Activar Ambiente Personalizado ✨"):
        publicar("cmqtt_env", {
            "ambiente": "personalizado",
            "luz": luz,
            "sonido": sonido.lower(),
            "temperatura": temperatura,
            "humidificador": humidificador.lower()
        })
        st.success("💖 Ambiente personalizado activado")

    st.markdown('</div>', unsafe_allow_html=True)

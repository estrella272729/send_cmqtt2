import paho.mqtt.client as paho
import streamlit as st
import json
import base64

st.set_page_config(page_title="Espacio de Relajación Multimodal", page_icon="🌿", layout="centered")

# ---------- OCULTAR BARRA DEL AUDIO ----------
st.markdown("""
<style>
audio { display: none; }
</style>
""", unsafe_allow_html=True)

# ---------- FUNCIÓN PARA CARGAR FONDOS EN BASE64 ----------
def fondo(nombre_archivo):
    with open(nombre_archivo, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    .card {{
        background: rgba(255,255,255,0.65);
        backdrop-filter: blur(20px);
        border-radius: 18px;
        padding: 22px;
        border: 1px solid rgba(255,255,255,0.45);
        margin-top: 14px;
    }}
    </style>
    """, unsafe_allow_html=True)

# ---------- MQTT CONFIG ----------
broker = "157.230.214.127"
port = 1883

def publicar(mensaje):
    client = paho.Client("voice_angie")  # Cliente MQTT
    client.connect(broker, port)
    client.publish("cmqtt_env", json.dumps(mensaje))
    client.disconnect()

# ---------- UI ----------
st.title("🌿 Espacio de Relajación Multimodal")

ambiente = st.radio("Selecciona un ambiente:", ["Selva (Bosque)", "Desierto Dorado", "Personalizado (Spa)"])

# ---------- SELVA ----------
if ambiente == "Selva (Bosque)":
    fondo("sel.jpg")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🌿 Ambiente Selva")
    st.write("Sonido de pájaros, luz verde suave, frescura natural 🌱")

    st.markdown('<audio src="birds.mp3" autoplay loop></audio>', unsafe_allow_html=True)

    if st.button("Activar Ambiente Selva"):
        publicar({
            "ambiente": "selva",
            "luz": "verde",
            "sonido": "pajaros",
            "temperatura": 22,
            "humidificador": "on"
        })
        st.success("✨ Selva activada")
    st.markdown('</div>', unsafe_allow_html=True)


# ---------- DESIERTO ----------
elif ambiente == "Desierto Dorado":
    fondo("desi.jpg")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🏜️ Ambiente Desierto Dorado")
    st.write("Luz ámbar cálida, viento suave, calma profunda 🌬️")

    st.markdown('<audio src="wind.mp3" autoplay loop></audio>', unsafe_allow_html=True)

    if st.button("Activar Ambiente Desierto"):
        publicar({
            "ambiente": "desierto",
            "luz": "ambar",
            "sonido": "viento",
            "temperatura": 28,
            "humidificador": "off"
        })
        st.success("🔥 Desierto activado")
    st.markdown('</div>', unsafe_allow_html=True)


# ---------- SPA PERSONALIZADO ----------
else:
    fondo("spa.jpg")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎨 Spa Personalizado")
    st.write("Un ambiente creado a tu medida ✨")

    luz = st.color_picker("Color de luz:", "#F5EEDC")
    sonido = st.selectbox("Sonido:", ["Lluvia", "Viento", "Instrumental", "Pájaros", "Silencio"])
    temperatura = st.slider("Temperatura (°C):", 16, 32, 24)
    humidificador = st.radio("Humidificador:", ["ON", "OFF"])

    if sonido != "Silencio":
        st.markdown(f'<audio src="{sonido.lower()}.mp3" autoplay loop></audio>', unsafe_allow_html=True)

    if st.button("Activar Ambiente Spa"):
        publicar({
            "ambiente": "personalizado",
            "luz": luz,
            "sonido": sonido.lower(),
            "temperatura": temperatura,
            "humidificador": humidificador.lower()
        })
        st.success("💖 Spa Personalizado Activado")

    st.markdown('</div>', unsafe_allow_html=True)

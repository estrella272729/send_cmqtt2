import paho.mqtt.client as paho
import streamlit as st
import json

st.set_page_config(page_title="Ambientes de Relajación", page_icon="🌿", layout="centered")

# -------- ESTILO VISUAL --------
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

def publicar(mensaje):
    client = paho.Client("SPA_APP")
    client.connect(broker, port)
    client.publish("cmqtt_env", json.dumps(mensaje))
    client.disconnect()

st.title("🌿 Espacio de Relajación Multimodal")

ambiente = st.radio("Selecciona un ambiente:", ["Selva", "Desierto", "Personalizado"])

# -------- SELVA --------
if ambiente == "Selva":
    st.image("https://i.imgur.com/NCRZa5b.gif", use_container_width=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🌿 Ambiente Selva")
    st.write("Sonido de aves, luz verde suave, humedad fresca.")
    st.audio("birds.mp3")
    if st.button("Activar Selva"):
        publicar({"ambiente":"selva","luz":"verde","sonido":"pajaros","temperatura":22,"humidificador":"on"})
        st.success("✨ Selva activada")
    st.markdown('</div>', unsafe_allow_html=True)

# -------- DESIERTO --------
elif ambiente == "Desierto":
    st.image("https://i.imgur.com/JsJg6lY.gif", use_container_width=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🏜️ Ambiente Desierto")
    st.write("Luz cálida, viento suave, ambiente templado.")
    st.audio("wind.mp3")
    if st.button("Activar Desierto"):
        publicar({"ambiente":"desierto","luz":"ambar","sonido":"viento","temperatura":28,"humidificador":"off"})
        st.success("🔥 Desierto activado")
    st.markdown('</div>', unsafe_allow_html=True)

# -------- PERSONALIZADO --------
else:
    st.image("https://i.imgur.com/fkTbQ0J.gif", use_container_width=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎨 Ambiente Personalizado")

    luz = st.color_picker("Color de luz:", "#F5EEDC")
    sonido = st.selectbox("Sonido:", ["Lluvia", "Viento", "Instrumental", "Pájaros", "Silencio"])
    temperatura = st.slider("Temperatura (°C):", 16, 32, 24)
    humidificador = st.radio("Humidificador:", ["ON", "OFF"])

    if sonido != "Silencio":
        st.audio(f"{sonido.lower()}.mp3")

    if st.button("Activar Ambiente Personalizado ✨"):
        publicar({
            "ambiente":"personalizado",
            "luz":luz,
            "sonido":sonido.lower(),
            "temperatura":temperatura,
            "humidificador":humidificador.lower()
        })
        st.success("💖 Ambiente Personalizado Activado")
    st.markdown('</div>', unsafe_allow_html=True)

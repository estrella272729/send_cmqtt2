import paho.mqtt.client as paho
import streamlit as st
import json
import base64

st.set_page_config(page_title="Relax Space", page_icon="🌿", layout="centered")

# ---------- OCULTAR BARRA GRIS DEL AUDIO ----------
st.markdown("""
<style>
audio { display: none; }
</style>
""", unsafe_allow_html=True)

# ---------- FUNCIÓN PARA FONDO CON BASE64 ----------
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

# ---------- FUNCIÓN DE AUDIO CON FADE + DESBLOQUEO ----------
def play_audio(file):
    st.markdown(f"""
    <audio id="audio" src="{file}" loop></audio>
    <script>
        let audio = document.getElementById("audio");
        document.addEventListener("click", () => {{
            audio.play();
            // Fade-in suave
            audio.volume = 0;
            let v = 0;
            let fade = setInterval(() => {{
                if(v < 1.0) {{
                    v += 0.02;
                    audio.volume = v;
                }} else {{
                    clearInterval(fade);
                }}
            }}, 120);
        }}, {{ once: true }});
    </script>
    """, unsafe_allow_html=True)

# ---------- MQTT ----------
broker = "157.230.214.127"
port = 1883

def publicar(mensaje):
    client = paho.Client("voice_angie")
    client.connect(broker, port)
    client.publish("cmqtt_env", json.dumps(mensaje))
    client.disconnect()

# ---------- UI ----------
st.title("🌿 Relaxation Multimodal Space")

ambiente = st.radio("Choose an environment:", ["Forest", "Desert", "Custom Spa"])

# ---------- FOREST ----------
if ambiente == "Forest":
    fondo("sel.jpg")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🌿 Forest Ambience")
    st.write("Birdsong, fresh air, soft green atmosphere.")

    play_audio("birds.mp3")  # sonido automático

    if st.button("Activate Forest"):
        publicar({
            "ambiente": "selva",
            "luz": "verde",
            "sonido": "birds",
            "temperatura": 22,
            "humidificador": "on"
        })
        st.success("✨ Forest Activated")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- DESERT ----------
elif ambiente == "Desert":
    fondo("desi.jpg")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🏜️ Desert Ambience")
    st.write("Golden light, soft silence, gentle warm wind.")

    play_audio("wind.mp3")  # sonido automático

    if st.button("Activate Desert"):
        publicar({
            "ambiente": "desierto",
            "luz": "ambar",
            "sonido": "wind",
            "temperatura": 28,
            "humidificador": "off"
        })
        st.success("🔥 Desert Activated")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- CUSTOM SPA ----------
else:
    fondo("spa.jpg")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎨 Custom Spa Ambience")
    st.write("Create your personal relaxation mood ✨")

    luz = st.color_picker("Light color:", "#F5EEDC")
    sonido = st.selectbox("Sound:", ["Rain", "Wind", "Instrumental", "Birds", "Silence"])
    temperatura = st.slider("Temperature (°C):", 16, 32, 24)
    humidificador = st.radio("Humidifier:", ["ON", "OFF"])

    # Sonido solo si el usuario lo elige
    if sonido != "Silence":
        play_audio(f"{sonido.lower()}.mp3")

    if st.button("Activate Custom Spa"):
        publicar({
            "ambiente": "personalizado",
            "luz": luz,
            "sonido": sonido.lower(),
            "temperatura": temperatura,
            "humidificador": humidificador.lower()
        })
        st.success("💖 Custom Spa Activated")

    st.markdown('</div>', unsafe_allow_html=True)


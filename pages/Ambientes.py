import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# ---- CONFIGURACIÓN DE PÁGINA ----
st.set_page_config(
    page_title="Spa Domótico",
    page_icon="💧",
    layout="centered"
)

# ---- ESTILOS TIPO SPA (CSS) ----
st.markdown(
    """
    <style>
    /* Fondo general en tonos suaves */
    .stApp {
        background:#60BCE0;
        font-family: "Segoe UI", sans-serif;
    }

    /* Títulos principales */
    h1, h2, h3 {
        color: black;
        font-weight: 600;
    }

    /* Caja general de cada sección */
    .spa-box {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 1.2rem 1.5rem;
        border-radius: 18px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.06);
        margin-bottom: 1.3rem;
        border: 1px solid rgba(220, 235, 235, 0.9);
    }

    /* Botones estilo spa */
    .stButton > button {
        border-radius: 999px;
        padding: 0.5rem 1.2rem;
        border: none;
        background: linear-gradient(135deg, #6ec6b3, #4f8fba);
        color: white;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        cursor: pointer;
        transition: all 0.2s ease-in-out;
    }

    .stButton > button:hover {
        transform: translateY(-1px) scale(1.02);
        box-shadow: 0 6px 16px rgba(0,0,0,0.2);
        background: linear-gradient(135deg, #7fd6c3, #5b9acc);
    }

    /* Slider */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #6ec6b3, #f7b267);
    }

    /* Texto pequeño de apoyo */
    .spa-caption {
        font-size: 0.9rem;
        color: #5f7b7b;
        margin-bottom: 0.3rem;
    }

    /* Selector de audio */
    .stSelectbox label {
        font-weight: 600;
        color: #345a63;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---- INFO DE VERSIÓN ----
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

# ---- TÍTULO PRINCIPAL ----
st.title("Spa Domótico")
st.markdown(
    '<p class="spa-caption">Controla el humificador, la luz ambiente y la temperatura, '
    'y acompáñalo con sonidos relajantes.</p>',
    unsafe_allow_html=True
)

# --------- AMBIENTE PREDETERMINADO ----------
st.markdown('<div class="spa-box">', unsafe_allow_html=True)
st.subheader("Ambiente predeterminado")

st.markdown(
    '<p class="spa-caption">Al activar este ambiente se configura automáticamente:</p>'
    '<ul class="spa-caption">'
    '<li>Temperatura: 20 °C</li>'
    '<li>Humificador: apagado</li>'
    '<li>Luz: encendida</li>'
    '</ul>',
    unsafe_allow_html=True
)

if st.button("Activar ambiente de relajación (20 °C)"):
    # Creamos un cliente MQTT y enviamos las tres órdenes
    client_preset = paho.Client("GIT-ANGIE")
    client_preset.on_publish = on_publish
    client_preset.connect(broker, port)

    # 1) Temperatura 20 °C
    msg_temp = json.dumps({"Temperatura": 20.0})
    client_preset.publish("cmqtt_spa2", msg_temp)

    # 2) Humificador OFF
    msg_hum = json.dumps({"Act1": "OFF"})
    client_preset.publish("cmqtt_spa", msg_hum)

    # 3) Luz ON
    msg_luz = json.dumps({"Luz": "ON"})
    client_preset.publish("cmqtt_spa3", msg_luz)

st.markdown('</div>', unsafe_allow_html=True)

# --------- CONTROL HUMIFICADOR (ON / OFF) ----------
st.markdown('<div class="spa-box">', unsafe_allow_html=True)
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

st.markdown('</div>', unsafe_allow_html=True)

# --------- CONTROL DE LUZ (ON / OFF) ----------
st.markdown('<div class="spa-box">', unsafe_allow_html=True)
st.subheader("🕯️ Luz ambiente")

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

st.markdown('</div>', unsafe_allow_html=True)

# --------- CONTROL DE TEMPERATURA ----------
st.markdown('<div class="spa-box">', unsafe_allow_html=True)
st.subheader("🌡️ Control de temperatura")

temperatura = st.slider(
    'Selecciona la temperatura (°C)',
    10.0,
    40.0,
    20.0  # valor inicial cambiado a 20 °C
)
st.write('Temperatura seleccionada:', temperatura, "°C")

if st.button('Enviar temperatura'):
    client1 = paho.Client("GIT-ANGIE")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Temperatura": float(temperatura)})
    ret = client1.publish("cmqtt_spa2", message)
else:
    st.write('')

st.markdown('</div>', unsafe_allow_html=True)

# --------- REPRODUCCIÓN DE AUDIOS DESDE GITHUB ----------
st.markdown('<div class="spa-box">', unsafe_allow_html=True)
st.subheader("🎧 Sonidos relajantes")

audios = {
    "Sonido de pájaros 🐦": "bird.mp3",
    "Sonido de lluvia 🌧️": "rain.mp3",
    "Música instrumental 🎼": "instrumental.mp3",
}

opcion_audio = st.selectbox("Elige un audio para acompañar tu sesión", list(audios.keys()))

st.audio(audios[opcion_audio], format="audio/mp3")

st.markdown('</div>', unsafe_allow_html=True)

st.audio(audios[opcion_audio], format="audio/mp3")

st.markdown('</div>', unsafe_allow_html=True)

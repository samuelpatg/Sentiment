from textblob import TextBlob
import pandas as pd
import streamlit as st
from PIL import Image
from googletrans import Translator
from streamlit_lottie import st_lottie
import json
import requests

st.title('Análisis de Sentimiento')
image = Image.open('emoticones.jpg')
st.image(image)
st.subheader("Por favor escribe en el campo de texto la frase que deseas analizar")

translator = Translator()

with st.sidebar:
    st.subheader("Polaridad y Subjetividad")
    st.write("""
    Polaridad: Indica si el sentimiento expresado en el texto es positivo, negativo o neutral. 
    Su valor oscila entre -1 (muy negativo) y 1 (muy positivo), con 0 representando un sentimiento neutral.
    
    Subjetividad: Mide cuánto del contenido es subjetivo (opiniones, emociones, creencias) frente a objetivo
    (hechos). Va de 0 a 1, donde 0 es completamente objetivo y 1 es completamente subjetivo.
    """)

# --- Funciones para cargar animaciones Lottie ---
def load_lottie_local(filepath: str):
    """Carga un archivo .json de Lottie guardado localmente."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def load_lottie_url(url: str):
    """Carga una animación Lottie desde una URL."""
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# --- Animaciones (elige LOCAL o URL según prefieras) ---
# Opción A: archivos locales en una carpeta "lottie/"
LOTTIE_POSITIVO = load_lottie_local("Happy.json")
LOTTIE_NEGATIVO = load_lottie_local("Sad.json")
LOTTIE_NEUTRAL  = load_lottie_local("Neutral.json")

# Opción B: desde una URL (descomenta y reemplaza local por url si prefieres esto)
# LOTTIE_POSITIVO = load_lottie_url("https://assets.lottiefiles.com/tu-url-happy.json")
# LOTTIE_NEGATIVO = load_lottie_url("https://assets.lottiefiles.com/tu-url-sad.json")
# LOTTIE_NEUTRAL  = load_lottie_url("https://assets.lottiefiles.com/tu-url-neutral.json")

with st.expander('Analizar texto'):
    text = st.text_input('Escribe por favor: ')
    if text:
        translation = translator.translate(text, src="es", dest="en")
        trans_text = translation.text
        blob = TextBlob(trans_text)

        polaridad = round(blob.sentiment.polarity, 2)
        subjetividad = round(blob.sentiment.subjectivity, 2)

        st.write('Polarity: ', polaridad)
        st.write('Subjectivity: ', subjetividad)

        x = polaridad

        if x > 0.1:
            st.write('Es un sentimiento Positivo 😊')
            st_lottie(LOTTIE_POSITIVO, height=250, key="happy")
        elif x < -0.1:
            st.write('Es un sentimiento Negativo 😔')
            st_lottie(LOTTIE_NEGATIVO, height=250, key="sad")
        else:
            st.write('Es un sentimiento Neutral 😐')
            st_lottie(LOTTIE_NEUTRAL, height=250, key="neutral")

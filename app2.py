import streamlit as st
import requests
import base64

# URLs de tus APIs
URL_AUDIO_A_TEXTO = "https://oqj2q7ygtb.execute-api.us-east-1.amazonaws.com/default/prueba3"
URL_TEXTO_A_AUDIO = "https://zz5vifuk78.execute-api.us-east-1.amazonaws.com/default/prueba4"

st.set_page_config(page_title="Transcribe & Polly App", layout="wide")

# Inicializar estados
if "texto_actual" not in st.session_state:
    st.session_state.texto_actual = ""
if "audio_creado" not in st.session_state:
    st.session_state.audio_creado = None



st.markdown("<h2 style='text-align:center;color:#ef1023;'>🎤 Convertidor Audio ⇄ Texto AWS</h2>", unsafe_allow_html=True)

# --- COLUMNAS ---
col1, col2 = st.columns(2)

# --- Columna 1: Audio a Texto ---
with col1:
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.subheader("🔊 Audio a Texto")
    archivo_audio = st.file_uploader("Selecciona un archivo de audio", type=["wav", "mp3", "ogg","m4a","aac"], key="audio1")
    
    if archivo_audio:
        st.audio(archivo_audio, format="audio/wav")

        if st.button("Convertir Audio a Texto", key="btn1", help="Click para transcribir", args=None):
            try:
                with st.spinner("Procesando audio..."):
                    audio_data = archivo_audio.read()
                    audio_base64 = base64.b64encode(audio_data).decode("utf-8")

                    response = requests.post(
                        URL_AUDIO_A_TEXTO,
                        json={"body": audio_base64},
                        headers={"Content-Type": "application/json"}
                    )

                    if response.ok:
                        resultado = response.json()
                        st.session_state.texto_actual = resultado.get("texto", "")
                        st.success("✅ Transcripción completada")
                    else:
                        st.error(f"Error en la API: {response.status_code}")

            except Exception as err:
                st.error(f"No se pudo conectar a la API: {err}")
    st.markdown('</div>', unsafe_allow_html=True)

# --- Columna 2: Texto a Audio ---
with col2:
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.subheader("📝 Texto a Audio")
    if st.session_state.texto_actual:
        st.session_state.texto_actual = st.text_area("Edita el texto:", value=st.session_state.texto_actual, height=200)

        if st.button("Generar Audio", key="btn2"):
            try:
                with st.spinner("Creando audio... 🎶"):
                    response = requests.post(
                        URL_TEXTO_A_AUDIO,
                        data=st.session_state.texto_actual,
                        headers={"Content-Type": "text/plain"}
                    )

                    if response.ok:
                        resultado_audio = response.json()
                        audio_b64 = resultado_audio.get("audio_base64", "")
                        if audio_b64:
                            st.session_state.audio_creado = base64.b64decode(audio_b64)
                            st.success("✅ Audio generado correctamente")
                        else:
                            st.warning("⚠ La API no devolvió audio")
                    else:
                        st.error(f"Error en la API: {response.status_code}")

            except Exception as err:
                st.error(f"No se pudo conectar a la API: {err}")

        if st.session_state.audio_creado:
            st.subheader("🎧 Reproducir Audio Generado")
            st.audio(st.session_state.audio_creado, format="audio/mp3")
    st.markdown('</div>', unsafe_allow_html=True)

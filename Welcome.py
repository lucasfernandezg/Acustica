import streamlit as st
from Funciones import *
import sounddevice as sd

st.set_page_config("RICO")
st.title('RICO')
st.markdown(
    """
    ### Hola!
    Bienvenido a RICO (Respuesta al Impulso de Cuarto Optimizado).
    Como ves son cuatro modulos:
    - Welcome: (este modulo) con datita de bienvenida
    - Generator: genera, reproduce y graba la IR.
    - Process: se especifican qué RIRs y los parametros a procesar
    - Analysis: el analisis de las RIRs procesadas
    
    De entrada y salida de audio utiliza lo que este seleccionado desde el sistema operativo.
    """)

import streamlit as st
from Funciones import *
import sounddevice as sd


st.markdown(
    """
    ### Hola Kpo
    Bienvenido a RICO (Respuesta al Impulso de Cuarto Optimizado).
    Vinimos a patearle el orto a los giles de Aurora.
    Como ves son cuatro modulos:
    - Welcome: (este modulo) con datita de bienvenida
    - Generator: genera, reproduce y graba la IR.
    - Process: se especifican qué RIRs y los parametros a procesar
    - Analysis: el analisis de las RIRs procesadas
    """)

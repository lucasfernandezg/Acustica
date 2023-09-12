import streamlit as st
from Funciones import *
import sounddevice as sd


def sweepPlay(length, f0, f1, fs):
    sw, inv = sweep(length, f0, f1, fs)
    r = sd.playrec(sw, fs, channels=1)
    st.session_state["rec_sweep"] = r


st.write("Sine Sweep Generator and Recorder")
f0 = st.number_input("Starting Frequency [Hz]", min_value=1, step=1)
f1 = st.number_input("Ending Frequency [Hz]", min_value=1, step=1)
length = st.number_input("Length [s]", min_value=0)
fs = st.number_input("Sampling Frequency", min_value=1, step=1)


st.button("Play&Rec Sweep", on_click=sweepPlay, args=[length, f0, f1, fs])

if st.button("Show Plot"):
    fig = plt.figure()
    plt.plot(st.session_state["rec_sweep"])
    st.pyplot(fig)

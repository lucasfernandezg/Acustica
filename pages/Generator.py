import sys
from Funciones import *
import streamlit as st

# sar session_states para guardar la data de cada pagina y que sea el valor por default del generador.

if "Generator" not in st.session_state:
    st.session_state.Generator = {"names":[], "data":[]}

if "page_save" not in st.session_state:
    st.session_state.page_save = {"name":"", "f0":100, "f1":500, "length":1, "fs":44100}
    
st.write(int(st.session_state.page_save["f0"]))

def sweepPlay(length, f0, f1, fs):
    sw, inv = sweep(length, f0, f1, fs)
    r = sd.playrec(sw, fs, channels=1)
    st.session_state.Generator["data"].append(r)
    st.session_state.Generator["names"].append(name)

def saveValue(key):
    st.session_state.page_save[key] = st.session_state[key]

st.write("Sine Sweep Generator and Recorder")
name = st.text_input("Name the RIR", key="name")
f0 = st.number_input("Starting Frequency [Hz]", key="f0", min_value=1, step=1, on_change=saveValue, args=("f0",), value = int(st.session_state.page_save["f0"]))
f1 = st.number_input("Ending Frequency [Hz]", key="f1", min_value=1, step=1)
length = st.number_input("Length [s]", key="length", min_value=0)
fs = st.number_input("Sampling Frequency", key="fs", min_value=1, step=1)


st.button("Play&Rec Sweep", on_click=sweepPlay, args=[length, f0, f1, fs])


if st.button("Show Plot"):
    fig = plt.figure()
    plt.plot(st.session_state.Generator["data"][-1], label=name)
    plt.legend()
    st.pyplot(fig)

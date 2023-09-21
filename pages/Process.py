import sys
from Funciones import *
import streamlit as st
import soundfile as sf
import io
import wave
from tempfile import NamedTemporaryFile

sys.path.append('..')
st.set_page_config("RICO")
st.title('PROCESS')

if "Process" not in st.session_state:
    st.session_state.Process = {}

if "band" not in st.session_state:
    st.session_state.band = "Octava"



col1, col2 = st.columns(2)

with col1:
    st.text("Rirs:")
    if "Generator" in st.session_state:
        for j in range(0,len(st.session_state.Generator["names"])):
            st.checkbox(st.session_state.Generator["names"][j] +" "+ str(st.session_state.Generator["fs"][j]), key=j)
        
def remove():
    for j in range(0,len(st.session_state.Generator["names"])):
        if st.session_state[j]:
            st.session_state.Generator["names"].pop(j)
            st.session_state.Generator["data"].pop(j)
            st.session_state.Generator["fs"].pop(j)
        
def process():
    #Check bandas:
    if st.session_state.band == "Tercio de Octava":
        tercio = True
    else:
        tercio = False
    #Que rirs fueron seleccionadas para procesar:
    for j in range(0,len(st.session_state.Generator["names"])):
        if st.session_state[j]:
            jName = st.session_state.Generator["names"][j]
            jData = st.session_state.Generator["data"][j]
            jFs = st.session_state.Generator["fs"][j]
            st.session_state.Process[jName] = {"bandasImp": {}, "bandasSch": {}, "IR": {}, "T20": [], "T30": [], "EDT": [], "C50":[], "C80": []}
            a, b = filtrar(jData, jFs, tercio = tercio)
            st.session_state.Process[jName]["bandasImp"] = a
            st.session_state.Process[jName]["bandas"] = b
            # print(a.keys())
            for i in a.keys():
                # print(i)
                sch, ir = schroeder(a[i], jFs, tail = 26)
                print(sch[-1], " ", i)
                st.session_state.Process[jName]["bandasSch"][i] = sch
                st.session_state.Process[jName]["IR"][i] = ir
                st.session_state.Process[jName]["T30"].append(T30(sch, jFs))
                st.session_state.Process[jName]["T20"].append(T20(sch, jFs))
                st.session_state.Process[jName]["EDT"].append(EDT(sch, jFs))
                st.session_state.Process[jName]["C50"].append(C50(ir, jFs))
                st.session_state.Process[jName]["C80"].append(C80(ir, jFs))
                
                

    
            
# def band_change(x):
#     print(x)
#     if x == "Tercio de Octava":
#         st.session_state.band = True
#     else:
#         st.session_state.band = False

# --- El verdadero Upload
def upload_togo():
    file = wav_bytes = io.BytesIO(st.session_state["file"].read())
    
    if file is not None:
        with wave.open(wav_bytes, 'rb') as wav_file:
            # Obtener los parámetros del archivo WAV
            params = wav_file.getparams()
            print(params.framerate)
            
            # Leer los datos del archivo WAV en un arreglo NumPy
            audio_data = np.frombuffer(wav_file.readframes(params.nframes), dtype=np.int16)
            st.session_state.Generator["names"].append(st.session_state["file"].name)
            st.session_state.Generator["fs"].append(params.framerate)
            st.session_state.Generator["data"].append(audio_data)
#             print(st.session_state["file"].name)
#             print(audio_data)

def upload():
    st.session_state.Generator["names"].append(st.session_state["file"].name)
    audioup, fsup = sf.read("AudioFiles/"+st.session_state["file"].name)
    st.session_state.Generator["fs"].append(fsup)
    st.session_state.Generator["data"].append(audioup)

st.button("Process", on_click=process)
st.button("Delete", on_click=remove)
file = st.file_uploader("Upload Wav File", type=[".wav",".wave"], key = "file", on_change=upload)





with col2:
    st.session_state.band = st.radio("Bandas:" ,["Octava", "Tercio de Octava"])
    #print(st.session_state.band)
    
    
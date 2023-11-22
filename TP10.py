#! D:\Programacion\Python\admin\Scripts\python.exe
import streamlit as st
from Funciones import *
import os
import pandas as pd

#from tempfile import NamedTemporaryFile




### Funciones ###
def without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}

def upload():
    # with NamedTemporaryFile(dir='.', suffix='.wav') as f:
    #     f.write(file.getbuffer())
    #     path = f.name.split("tmp")[0]
    #     print(path)
    if st.session_state["file"] is not None:
        st.session_state.rirs["name"] = st.session_state["file"].name
        audio, fs = sf.read("AudioFiles/"+st.session_state["file"].name)
        st.session_state.rirs["fs"] = fs
        st.session_state.rirs["data"] = audio
        #print(audio)

def process():
    clearVars()
    fs = st.session_state.rirs["fs"]
    schtot, irtot = schroeder(st.session_state.rirs["data"], fs, tail = 26)
    st.session_state.rirs["IR"] = irtot
    if st.session_state.rirs["band"] == "Octava":
        bandas, freqCentrales = filtrado(st.session_state.rirs["data"], st.session_state.rirs["fs"], False)
    else:
        bandas, freqCentrales = filtrado(st.session_state.rirs["data"], st.session_state.rirs["fs"], True)
    st.session_state.rirs["Freqs"] = freqCentrales
    #print(freqCentrales)
    for banda in bandas:
        sch, ir = schroeder(banda, fs, tail = 26)
        st.session_state.rirs["T20"].append(T20(sch, fs))
        st.session_state.rirs["EDT"].append(EDT(sch, fs))
        st.session_state.rirs["C50"].append(C50(ir, fs))
        st.session_state.rirs["C80"].append(C80(ir, fs))
    st.session_state.rirs["dataOK"] = True
    #print(st.session_state.rirs["T20"])

def clearVars():
    st.session_state.rirs["T20"] = []
    st.session_state.rirs["EDT"] = []
    st.session_state.rirs["C50"] = []
    st.session_state.rirs["C80"] = []


if "rirs" not in st.session_state:
    st.session_state.rirs = {"name":None, "IR": None, "data":None, "fs":None, "band":"Octava", "Freqs":[], "T20": [], "EDT": [], "C50":[], "C80": [], "dataOK":False}


st.set_page_config("RIRs", layout="wide")
st.title('RIRs')
st.markdown(
    """
    Software de Procesamiento de RIRs
    """)


file = st.file_uploader("Upload Wav File", type=[".wav",".wave"], key = "file", on_change=upload)



# Información de la RIR cargada
if st.session_state.rirs["name"] != None:
    st.text(f"File name: {st.session_state.rirs['name'].split('/')[-1][:-4]}; Sampling frequency: {st.session_state.rirs['fs']} Hz")


st.session_state.rirs["band"] = st.radio("Bandas:" ,["Octava", "Tercio de Octava"])


# Tabla con parametros
st.button("Process", on_click=process)
if st.session_state.rirs["dataOK"] == True:
    data = without_keys(st.session_state.rirs, ["name","IR","data","fs","band","dataOK"])
    df = pd.DataFrame(data)
    st.write(df.transpose())
    

# Gráficos
if st.session_state.rirs["data"] is not None:
    fig = plt.figure()
    plt.plot(st.session_state.rirs["data"])
    st.pyplot(fig)

def export():
    df.to_excel(f"{st.session_state.rirs['name'].split('/')[-1][:-4]} Parameters.xlsx")
# Export Excel

if st.session_state.rirs["dataOK"] == True:
    df = pd.DataFrame.from_dict(data)
    st.button("Export Data", on_click=export)

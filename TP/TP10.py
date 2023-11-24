#! D:\Programacion\Python\admin\Scripts\python.exe
import streamlit as st
from Funciones import *
import pandas as pd


### Funciones ###
def without_keys(d, keys):
    '''Quita los keys selecionados de un dictionary'''
    return {x: d[x] for x in d if x not in keys}

def upload():
    '''Lee la información del archivo seleccionado'''
    if st.session_state["file"] is not None:
        st.session_state.rirs["name"] = st.session_state["file"].name # se queda con el nombre para la siguiente linea
        audio, fs = sf.read("AudioFiles/"+st.session_state["file"].name) # Lee la información de audio del archivo con el nombre guardado
        st.session_state.rirs["fs"] = fs  # Frecuencia de sampleo del archivo importado
        st.session_state.rirs["data"] = audio  # La informacion de audio del archivo importado

def process():
    '''Procesa loa rir importada para obtener los parametros acusticos'''
    clearVars() # Reiniciar los parametros T20...
    fs = st.session_state.rirs["fs"] # Variable local para facilitar la escritura
    schtot, irtot = schroeder(st.session_state.rirs["data"], fs, tail = 26) # Schroeder y RIR recortada del impulso sin filtrar
    st.session_state.rirs["IR"] = irtot # Se guarda en una variable global para luego poder graficarla

    # If statement para saber si filtrar por octava o tercio
    if st.session_state.rirs["band"] == "Octava": 
        bandas, freqCentrales = filtrado(st.session_state.rirs["data"], st.session_state.rirs["fs"], False)
    else:
        bandas, freqCentrales = filtrado(st.session_state.rirs["data"], st.session_state.rirs["fs"], True)
    #
    st.session_state.rirs["Freqs"] = freqCentrales  # lista de frecuencias centrales de cada banda

    # Loop para hacer Schroeder y RIR recortada de cada banda
    for banda in bandas:
        sch, ir = schroeder(banda, fs, tail = 26)
        st.session_state.rirs["T20"].append(T20(sch, fs))
        st.session_state.rirs["EDT"].append(EDT(sch, fs))
        st.session_state.rirs["C50"].append(C50(ir, fs))
        st.session_state.rirs["C80"].append(C80(ir, fs))
    st.session_state.rirs["dataOK"] = True #Boolean para saber si se proceso la rir
    #print(st.session_state.rirs["T20"])

def clearVars():
    '''Reinicia los parametros'''
    st.session_state.rirs["T20"] = []
    st.session_state.rirs["EDT"] = []
    st.session_state.rirs["C50"] = []
    st.session_state.rirs["C80"] = []

def export():
    '''Exporta el dataframe en formato excel en la misma carpeta donde se encuentra el main file .py'''
    df.to_excel(f"{st.session_state.rirs['name'].split('/')[-1][:-4]} {st.session_state.rirs['band']} Parameters.xlsx")

# Los session_state son como las variables globales, tienen formato de diccionario.
# Esta es la forma de instanciar el dictionario rirs con sus key:values por default
if "rirs" not in st.session_state:
    st.session_state.rirs = {"name":None, "IR": None, "data":None, "fs":None, "band":"Octava", "Freqs":[], "T20": [], "EDT": [], "C50":[], "C80": [], "dataOK":False}

# Formato de la pagina
st.set_page_config("RIRs", layout="wide")
st.title('RIRs') # Titulo de la pagina
st.markdown(
    """
    Software de Procesamiento de RIRs
    """) # Lo que dice al inicio

# El boton e interfaz de importación
file = st.file_uploader("Upload Wav File", type=[".wav",".wave"], key = "file", on_change=upload)



# Información de la RIR cargada
if st.session_state.rirs["name"] != None:
    st.text(f"File name: {st.session_state.rirs['name'].split('/')[-1][:-4]}; Sampling frequency: {st.session_state.rirs['fs']} Hz")

# El input del usuario para seleccionar el tipo de filtrado
st.session_state.rirs["band"] = st.radio("Bandas:" ,["Octava", "Tercio de Octava"])


# Tabla con parametros
st.button("Process", on_click=process) # El boton que dispara la funcion process
if st.session_state.rirs["dataOK"] == True: # Si los parametrso se procesaron correctamente
    data = without_keys(st.session_state.rirs, ["name","IR","data","fs","band","dataOK"]) # El diccionario sin los keys que no son parametros
    df = pd.DataFrame(data) # Creamos el dataframe
    st.write(df.transpose()) # Tabla con el dataframe transpuesto (para que las frecuencias no queden en una columna, sino en una fila)
    

# Gráficos
if st.session_state.rirs["data"] is not None:  # Si el archivo se importo correctamente
    fig = plt.figure()
    plt.plot(st.session_state.rirs["data"]) # Plotea la RIR importada en el tiempo
    st.pyplot(fig)


# Export Excel
if st.session_state.rirs["dataOK"] == True:  #Si los parametros no son nulos
    df = pd.DataFrame.from_dict(data) # Hace un dataframe con los parametros
    st.button("Export Data", on_click=export) # boton que al clikearse exporta el dataframe en formato excel

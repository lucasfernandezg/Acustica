import sys
from Funciones import *
import streamlit as st
from time import sleep
sys.path.append('..')
st.set_page_config("RICO")
st.title('GENERATOR')
sd.default.reset()
#sd.default.device = (None,None)
# State de datos que se pasan entre páginas. Estos datos se guardan cuando se clickea Play/Rec del sweep.
if "Generator" not in st.session_state:
    st.session_state.Generator = {"names":[], "data":[], "fs":[]} # Los datos que se pasa entre
    
# State para guardar los valores introducidos y que no se borren cuando cambio entre páginas. Se guardan cuando se cambian los valores de las casillas
if "page_save" not in st.session_state:
    st.session_state.page_save = {"name":"", "f0":100, "f1":500, "length":1.0 , "fs":44100} # Default Values (__init__)

# if "inputIndex" not in st.session_state:
#     st.session_state["inputIndex"] = None
    
# if "outputIndex" not in st.session_state:
#     st.session_state["outputIndex"] = None


### --- Test Print --- ###
# for i in st.session_state.page_save.keys():
#     try:
#         st.write(int(st.session_state.page_save[i]))
#     except:
#         st.write(st.session_state.page_save[i])
### --- Test Print --- ###


def sweepPlay(length, f0, f1, fs):
    sw, inv = sweep(length, f0, f1, fs)
    sleep(int(st.session_state["waitTime"]))
    rec = sd.playrec(sw, fs, channels=1)
    imp = sig.fftconvolve(rec.reshape(-1),inv)
    st.session_state.Generator["data"].append(imp)
    #print(st.session_state.Generator["data"][-1])
    st.session_state.Generator["names"].append(name)
    st.session_state.Generator["fs"].append(fs)

def saveValue(key):
    st.session_state.page_save[key] = st.session_state[key]
    
# def inputChange():
#     st.session_state["inputIndex"] = inputIndex[inputList.index(st.session_state["input"])]
#     sd.default.device([st.session_state["inputIndex"],st.session_state["outputIndex"]])

# def outputChange():
#     st.session_state["outputIndex"] = outputIndex[outputList.index(st.session_state["output"])]
#     sd.default.device([st.session_state["inputIndex"],st.session_state["outputIndex"]])


sampfreqs = [44100, 48000, 88200, 96000]
st.write("Sine Sweep Generator and Recorder")
name = st.text_input("Name the RIR", key="name", on_change=saveValue, args=("name",), value = st.session_state.page_save["name"])
f0 = st.number_input("Starting Frequency [Hz]", key="f0", min_value=20, max_value=19999, step=1, on_change=saveValue, args=("f0",), value = int(st.session_state.page_save["f0"]))
f1 = st.number_input("Ending Frequency [Hz]", key="f1", min_value=21, max_value=20000, step=1, on_change=saveValue, args=("f1",), value = int(st.session_state.page_save["f1"]))
length = st.number_input("Length [s]", key="length", min_value=0.0, on_change=saveValue, args=("length",), value = float(st.session_state.page_save["length"]))
fs = st.selectbox("Sampling Frequency", options = sampfreqs, key="fs", on_change=saveValue, args=("fs",), index =  sampfreqs.index(st.session_state.page_save["fs"]))
wait = st.number_input("Wait Time [s]", key="waitTime", min_value=0)


st.button("Play&Rec Sweep", on_click=sweepPlay, args=[length, f0, f1, fs])

# inputList = []
# inputIndex = []
# outputList = []
# outputIndex = []
# Qinput = np.array(list(sd.query_devices()))
# for i in range(0, len(Qinput)):
#     if Qinput[i]["max_input_channels"]>0:
#         inputList.append(Qinput[i]["name"])
#         inputIndex.append(Qinput[i]["index"])
#     if Qinput[i]["max_output_channels"]>0:
#         outputList.append(Qinput[i]["name"])
#         outputIndex.append(Qinput[i]["index"])
    

        
# st.selectbox("Input Device:",inputList, key="input", on_change=inputChange)
# st.selectbox("Output Device:",outputList, key="output", on_change=outputChange)

if st.button("Show Plot"):
    fig = plt.figure()
    plt.plot(st.session_state.Generator["data"][-1], label=name)
    plt.legend()
    st.pyplot(fig)

if st.button("Export Impulse"):
    sf.write(st.session_state.Generator["names"][-1]+".wav", st.session_state.Generator["data"][-1], st.session_state.Generator["fs"][-1])

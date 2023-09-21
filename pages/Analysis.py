import sys
from Funciones import *
import streamlit as st
import pandas as pd
sys.path.append('..')
st.set_page_config("RICO")
st.title('ANALYSIS')

def without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}

dict = without_keys(st.session_state.Process[st.session_state.Generator["names"][-1]],["bandasSch", "bandasImp", "IR"])

print(dict)
data = without_keys(dict, ["bandasImp", "bandasSch", "IR"])
df = pd.DataFrame(data)
st.table(df)

fig = plt.figure()
plt.plot(st.session_state.Process[st.session_state.Generator["names"][-1]]["IR"]["1000"], label=st.session_state.Generator["names"][-1])
#plt.plot(st.session_state.Process[st.session_state.Generator["names"][-1]]["bandasSch"]["1000"], label=st.session_state.Generator["names"][-1])
plt.legend()

st.pyplot(fig)
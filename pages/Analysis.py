import sys
from Funciones import *
import streamlit as st
import pandas as pd
sys.path.append('..')

def without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}

dict = without_keys(st.session_state.Process[st.session_state.Generator["names"][0]],["bandasSch", "bandasImp", "IR"])

print(dict)
data = without_keys(dict, ["bandasImp", "bandasSch", "IR"])
df = pd.DataFrame(data)
st.table(df)
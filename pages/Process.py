import sys
from Funciones import *
import streamlit as st

col1, col2 = st.columns(2)

with col1:
    st.text("Rirs:")
    if "Generator" in st.session_state:
        for i in st.session_state.Generator["names"]:
            st.checkbox(i)
    
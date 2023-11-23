import streamlit as st
from Funciones import *
import pandas as pd
import numpy as np
from scipy.signal import butter, lfilter, fftconvolve
import matplotlib.pyplot as plt
import soundfile as sf

import subprocess

if __name__ == '__main__':
    subprocess.run("streamlit run TP10.py")
import numpy as np
from scipy import signal as sig
import soundfile as sf

def index_where(array, value):
	return np.abs(array - value).argmin()

def sweep(length, f0, f1, fs, met="logarithmic"):
    # Hann: Donde hann = 0dB por primera vez = f0. Entonces el chirp me queda más largo en realidad.
    #hann = np.hanning(len(sw))
    t = np.linspace(0,length,int(fs*length))
    sw = sig.chirp(t,f0=f0,t1=t[-1],f1=f1,method=met)
    factor = np.exp((t*np.log(f1/f0))/length)
    inv = np.flip(sw)/factor
    inv = inv/np.max(inv)
    sw = 0.5*sw
    hann = np.hanning(fs/5)
    mid = index_where(hann, 1)
    addm = len(sw)-fs/5
    hann_win = np.concatenate((hann[:mid],np.ones(int(addm)),hann[mid:]))
    sw = hann_win*sw
    return sw, inv

sw, inv = sweep(40,100,16000,48000)
sf.write("Sweep 40s 100-16k 48khz.wav", sw, 48000)
sf.write("FiltroInverso 40s 100-16k 48khz.wav", inv, 48000)

#! D:\Programacion\Python\admin\Scripts\python.exe

from scipy import signal as sig
import sounddevice as sd
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt

# FILTRO

def filtrar(señal, fs, tercio = False):
    ext = 2
    nyq = fs/2
    bandas = [31.25, 62.5, 125, 250, 500, 1000, 2000, 4000, 8000, 16000] #**(1/2) para extremos oct y (1/6) para ter
    fter = [24.803, 31.25, 39.373, 49.606, 62.5, 78.745, 99.213, 125, 157.49, 198.43, 250, 314.98, 396.85, 500, 629.96, 793.7, 1000, 1259.9, 1587.4, 2000, 2519.8, 3174.8, 4000, 5039.7, 6349.6, 8000, 10079, 12699, 16000, 20159]
    if tercio:
        ext = 6
        bandas = fter
    extremos = [(x*2**(-1/ext))/nyq for x in bandas]
    extremos.append((bandas[-1]*2**(1/ext))/nyq)
    if extremos[-1] >= 1:
        extremos[-1]=0.999999999
    print(extremos)
    soses = []
    señalfiltrada = {}
    for i in range(0,len(bandas)):
        soses.append(sig.butter(6, [extremos[i], extremos[i+1]], btype='band', analog = False, output='sos'))
        señalfiltrada[str(bandas[i])] = sig.sosfilt(soses[i],señal)
    return señalfiltrada, bandas, soses


# GENERADOR DE SWEEP Y FILTRO INVERSO
def sweep(length, f0, f1, met,fs):
    t = np.linspace(0,length,int(fs*length))
    sw = sig.chirp(t,f0=f0,t1=t[-1],f1=f1,method=met)
    factor = np.exp((t*np.log(f1/f0))/length)
    inv = np.flip(sw)/factor
    return sw, inv


# INTEGRAL INVERSA DE SCHROEDER
def schroeder(rir):
    all = np.sum(rir**2)
    a = np.array([])
    for i in range(0,len(rir)):
        np.append(a, np.sum(rir[i:]**2))
    return 10*np.log10(a/all)


# iNTEGRAL INVERSA DE SCHROEDER EN DB
def schroederDB(IR):
    # Schroeder integration
    sch = np.cumsum(IR[::-1]**2)[::-1]
    sch_dB = 10.0 * np.log10(sch / np.max(sch))
    return sch_dB


# VALOR MEDIO
def valorMedio(x): 
    '''
    Calcula el valor medio de una señal x[n] de una dimensión.
    x[n] se entrega como una list o un array de numpy.
    Libreria necesaria: Numpy as np
    '''
    u = np.sum(np.array(x))/len(x)  #len(x) en vez de x.shape[0] porque len funciona para lists y arrays
    return u


# FILTRO DE MEDIANA MOVIL
def mmf(x, M):
    '''
    Filtro de media movil. x es la señal a filtrar y M el ancho de la ventana movil.
    '''
    if M>len(x):
        raise ValueError('El largo de la ventana (M={}) no puede ser mayor a la longuitud de la señal x (len(x)={}).'.format(M,len(x)))
    else:
        xf = np.zeros(len(x)-M)
        for i in range(0,len(x)-M):
            xf[i] = valorMedio(x[i:i+M])
        if (M % 2 == 0):
            xf = np.hstack([np.zeros(M//2), xf, np.zeros(M//2)])
        else:
            xf = np.hstack([np.zeros(M//2), xf, np.zeros((M//2)+1)])
        return xf


# RMS DE UNA SEÑAL
def rms(x):
    '''
    Calcula el RMS de una señal x[n] de una dimensión.
    x[n] se entrega como una list o un array de numpy.
    Libreria necesaria: Numpy as np
    '''
    rmsv = (np.sum(np.array(x)**2)/len(x))**(1/2)
    return rmsv


# INDEX DEL VALOR DADO
def index_where(array, value):
	return np.abs(array - value).argmin()


### --- PARAMETROS ACUSTICOS --- ###

# CROSS CORRELATION
def autoCorrelation(a, b, t, fs):
# Autocorrelacion pero arrancando de 0 hasta t.
	muestras = int(t*fs)
	corr = sig.correlate(a, b)
	m_mid = int(len(corr)/2)
	corr = corr[m_mid:muestras]
	return corr


# RT20
def T20(schroeder, fs):
# De -5db a -25db
	db_25_index = index_where(schroeder, -25)
	db_5_index = index_where(schroeder, -5)
	return ((db_25_index - db_5_index)/fs)*3


#RT30
def T30(schroeder, fs):
# De -5db a -35db
	db_35_index = index_where(schroeder, -35)
	db_5_index = index_where(schroeder, -5)
	return ((db_35_index - db_5_index)/fs)*2

# EARLY DECAY TIME
def EDT(schroeder, fs):
# Primeros 10db de atenuacion extrapolado a t60
	db_10_index = index_where(schroeder, -10)
	db_0_index = np.nonzero(schroeder)[0][0]-1
	return ((db_10_index - db_0_index)/fs)*6
	

# INTER AURAL CROSS CORRELATION
def IACC_early(rirL, rirR, fs):
# |autocorrelación de los primeros 80ms entre L y R, dividido por el modulo| El Max de esto.
	max_abs = np.max(np.abs(autoCorrelation(rirL, rirR, 0.08, fs)))
	denom = np.sqrt(np.sum(rirL**2)*np.sum(rirR**2))
	return max_abs/denom


# CLARITY 50
def C50(rir, fs):
	ms50 = int(fs*0.05)
	a = rir[:ms50]
	b = rir[ms50+1:]
	a = np.sum(a**2)
	b = np.sum(b**2)
	return 10*np.log10(a/b)


# CLARITY 80
def C80(rir, fs):
	ms80 = int(fs*0.08)
	a = rir[:ms80]
	b = rir[ms80+1:]
	a = np.sum(a**2)
	b = np.sum(b**2)
	return 10*np.log10(a/b)


# TRANSITION TIME
def Tt():
# ITDG, transition time. no sabemos ni como calcularlo. Hay que separar el rir en estocastico y deterministico y analizar el traspaso de uno a otro en energia. Bidondo tiró: " cuando det=-3db de tot rir".
    return None


# EARLY DECAY TIME (t)
def EDTt(schroeder, t, fs):
    # Early Decay time segun los primeros t segundos
	db_0_index = np.nonzero(schroeder)[0][0]-1
	time_index = db_0_index + int(t*fs)
	db = schroeder[time_index]
	multiplier = -60/db
	return t*fs*multiplier


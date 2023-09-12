#! D:\Programacion\Python\admin\Scripts\python.exe
# git
from scipy import signal as sig
import sounddevice as sd
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt

# FILTRO
def downsamplingfactor(freq, fs):
    guard = 0.10
    factor = (np.floor((fs / (2+guard)) / np.array(freq)))
    for idx in range(len(factor)):
        # Factor between 1<factor<50
        factor[idx] = max(min(factor[idx], 50), 1)
    
    return factor

def filtrar(señal, fs, tercio = False, resamp = False):
    ext = 2
    nyq = int(fs/2)
    bandas = [31.25, 62.5, 125, 250, 500, 1000, 2000, 4000, 8000, 16000] #**(1/2) para extremos oct y (1/6) para ter
    fter = [24.803, 31.25, 39.373, 49.606, 62.5, 78.745, 99.213, 125, 157.49, 198.43, 250, 314.98, 396.85, 500, 629.96, 793.7, 1000, 1259.9, 1587.4, 2000, 2519.8, 3174.8, 4000, 5039.7, 6349.6, 8000, 10079, 12699, 16000, 20159]
    if tercio:
        ext = 6
        bandas = fter
    extremos = [(x*2**(-1/ext))/nyq for x in bandas]
    extremos.append((bandas[-1]*2**(1/ext))/nyq)
    extremos = np.array(extremos)
    if extremos[-1] >= 1:
        extremos[-1]=0.999999999
    # soslow = []
    # soshi = []
    soses = []
    señalfiltrada = {}
    if resamp:
        factor = downsamplingfactor(extremos*nyq, fs)
        for i in range(0,len(bandas)):
            soses.append(sig.butter(6, [extremos[i], extremos[i+1]], btype='band', analog = False, output='sos'))
            x = sig.resample(señal, round(len(señal) / factor[i]))
            y = sig.sosfilt(soses[i], x)
            señalfiltrada[str(bandas[i])] = sig.resample_poly(y,factor[i],1)
    else:
        # for i in range(0,3):
        #     soslow.append(sig.butter(6, extremos[i+1], btype='lowpass', analog = False, output='sos'))
        #     soshi.append(sig.butter(6, extremos[i], btype='highpass', analog = False, output='sos'))
        #     a = sig.sosfilt(soslow[i], señal)
        #     señalfiltrada[str(bandas[i])] = sig.sosfilt(soshi[i], a)
        for i in range(0,len(bandas)):
            soses.append(sig.butter(6, [extremos[i], extremos[i+1]], btype='band', analog = False, output='sos'))
            señalfiltrada[str(bandas[i])] = sig.sosfilt(soses[i], señal)
    return señalfiltrada, bandas, soses


# GENERADOR DE SWEEP Y FILTRO INVERSO
def sweep(length, f0, f1, fs, met="logarithmic"):
    # Hann: Donde hann = 0dB por primera vez = f0. Entonces el chirp me queda más largo en realidad.
    #hann = np.hanning(len(sw))
    t = np.linspace(0,length,int(fs*length))
    sw = sig.chirp(t,f0=f0,t1=t[-1],f1=f1,method=met)
    factor = np.exp((t*np.log(f1/f0))/length)
    inv = np.flip(sw)/factor
    hann = np.hanning(fs/5)
    mid = index_where(hann, 1)
    addm = len(sw)-fs/5
    hann_win = np.concatenate((hann[:mid],np.ones(int(addm)),hann[mid:]))
    sw = 0.5*sw
    sw = hann_win*sw
    return sw, inv


# INTEGRAL INVERSA DE SCHROEDER
# def schroeder(rir):
#     all = np.sum(rir**2)
#     a = np.array([])
#     for i in range(0,len(rir)):
#         np.append(a, np.sum(rir[i:]**2))
#     return 10*np.log10(a/all)


# iNTEGRAL INVERSA DE SCHROEDER EN DB
def schroeder(IR, fs, tail=45, dB=True):
    '''
    IR: impulse response to integrate.
    fs: sampling frequency
    tail: how many dB under the peak does the IR cut its tail? If T30, then minimum -35 dB (45 dB is recommended in this case)
    Returns the Schroeders curve (sch_dB) and the sliced IR (IR_cut).
    '''
    sch = np.cumsum(IR[::-1]**2)[::-1]
    sch_dB = np.round(10.0 * np.log10(sch / np.max(sch)),2)
    start_cut = np.where(sch_dB == 0)[0][-1]
    end_cut = np.where(sch_dB == -np.abs(tail))[0][0]
    sch_dB = sch_dB[start_cut-int(fs/1000):end_cut] # 1ms de changui al principio
    sch = sch[start_cut-int(fs/1000):end_cut]
    IR_cut = IR[start_cut-int(fs/1000):end_cut]
    if dB:
        return sch_dB, IR_cut
    else:
        return sch/np.max(sch), IR_cut


# VALOR MEDIO
def valorMedio(x):
    '''
    Calcula el valor medio de una señal x[n] de una dimensión.
    x[n] se entrega como una list o un array de numpy.
    Libreria necesaria: Numpy as np
    '''
    u = np.sum(np.array(x))/len(x)  #len(x) en vez de x.shape[0] porque len funciona para lists y arrays
    return u


    # if overlap>=win:
    #     raise ValueError("overlap tiene que ser menor a win")
    # if win>len(x):
    #     raise ValueError('El largo de la ventana (win={}) no puede ser mayor a la longuitud de la señal x (len(x)={}).'.format(win,len(x)))

# FILTRO DE MEDIANA MOVIL
def mmf_old(x, win, overlap=0):
    '''
    Filtro de media movil. x es la señal a filtrar, win el ancho de la ventana movil y overlap son las muestras que se solpanan las ventanas.
    '''
    out=np.zeros(len(x))
    indexes = np.arange(0,len(x)-win+1,win-overlap)
    for i in indexes:
        out[i] = np.sum(x[i:i+win])/len(x[i:i+win])
        if i!= 0:
            out[i-overlap+1:i] = np.linspace(out[i-overlap], out[i], overlap+1)[1:-1]
    return out

def mmf(x,win,overlap=0):
    out=[]
    for i in np.arange(0, len(x)-win+1, win-overlap):
        out.append(np.sum(x[i:i+win])/len(x[i:i+win]))
    out = np.interp(np.linspace(0,len(out),len(out)*(win-overlap)),np.arange(0,len(out)),out)
    return out

    
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
    #Filtro de media movil = deterministico. Total - deterministico = estocastico. Schroeder de ambos y Tt= 10dB dif.
    
    return None


# EARLY DECAY TIME (t)
def EDTt(schroeder, t, fs):
    # Early Decay time segun los primeros t segundos
	db_0_index = np.nonzero(schroeder)[0][0]-1
	time_index = db_0_index + int(t*fs)
	db = schroeder[time_index]
	multiplier = -60/db
	return t*fs*multiplier


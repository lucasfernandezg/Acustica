# Funciones para extraer de un Impulso distintos parametros acusticos.
import numpy as np
from Filterbank import Filterbank
import scipy.stats as st
from scipy import signal as sig

def schroederDB(IR):
    # Schroeder integration
    sch = np.cumsum(IR[::-1]**2)[::-1]
    sch_dB = 10.0 * np.log10(sch / np.max(sch))
    return sch_dB


def schroeder(IR):
    # Schroeder integration
    sch = np.cumsum(IR[::-1]**2)[::-1]
    sch = sch / np.max(sch)
    return sch


def filtrado(rir, fs, ter):
    params = {'fs': fs,
              'bands': [31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000],
              'bandsize': 2,
              'order': 4,
              'f_length': 16384,
              'power': True}
    if ter:
        params['bands'] = [25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630,
                           800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500, 16000]
        params['bandsize'] = 3
    filterbank = Filterbank(**params)
    bands, centros = filterbank.apply(rir)
    return bands, centros





def lundeby(signal, fs, alpha=0.1):
    S = np.cumsum(signal**2)
    S = S/np.max(S)

def rms(x):
    '''
    Calcula el RMS de una señal x[n] de una dimensión.
    x[n] se entrega como una list o un array de numpy.
    Libreria necesaria: Numpy as np
    '''
    rmsv = (np.sum(np.array(x)**2)/len(x))**(1/2)
    return rmsv
    

def recorteRIR(signal, fs, ti, RT_estimado):
    sig = signal[np.argmax(signal)-int(ti*fs):]
    noise = signal[:np.argmax(signal)-int(ti*fs)]
    n=0
    while rms(sig[n:])>=rms(noise):
        n=n+1000
    return sig[:n+int(RT_estimado*fs)]


def INR(signal, fs, T60):
    noise = signal[-1*fs:]
    N = rms(noise)**2
    L = 10*np.log10(np.max(signal)**2)
    return L-N


def index_where(array, value):
	return np.abs(array - value).argmin()


def autoCorrelation(a, b, t, fs):
# Autocorrelacion pero arrancando de 0 hasta t.
	muestras = int(t*fs)
	corr = sig.correlate(a, b)
	m_mid = int(len(corr)/2)
	corr = corr[m_mid:muestras]
	return corr
	

## Parameters: ##

def T20(schroeder,fs):
# De -5db a -25db
	db_25_index = index_where(schroeder, -25)
	db_5_index = index_where(schroeder, -5)
	return ((db_25_index - db_5_index)/fs)*3


def T30(schroeder,fs):
# De -5db a -35db
	db_35_index = index_where(schroeder, -35)
	db_5_index = index_where(schroeder, -5)
	return ((db_35_index - db_5_index)/fs)*2


def EDT(schroeder, fs):
# Primeros 10db de atenuacion extrapolado a t60
	db_10_index = index_where(schroeder, -10)
	db_0_index = np.nonzero(schroeder)[0][0]-1
	return ((db_10_index - db_0_index)/fs)*6
	

def IACC_early(rirL, rirR, fs):
# |autocorrelación de los primeros 80ms entre L y R, dividido por el modulo| El Max de esto.
	max_abs = np.max(np.abs(autoCorrelation(rirL, rirR, 0.08, fs)))
	denom = np.sqrt(np.sum(rirL**2)*np.sum(rirR**2))
	return max_abs/denom


def C50(rir, fs):
	ms50 = int(fs*0.05)
	a = rir[:ms50]
	b = rir[ms50+1:]
	a = np.sum(a**2)
	b = np.sum(b**2)
	return 10*np.log10(a/b)


def C80(rir, fs):
	ms80 = int(fs*0.08)
	a = rir[:ms80]
	b = rir[ms80+1:]
	a = np.sum(a**2)
	b = np.sum(b**2)
	return 10*np.log10(a/b)


def Tt():
# ITDG, transition time. no sabemos ni como calcularlo. Hay que separar el rir en estocastico y deterministico y analizar el traspaso de uno a otro en energia. Bidondo tiró: " cuando det=-3db de tot rir".
    return None


def EDTt(schroeder, t, fs):
    # Early Decay time segun los primeros t segundos
	db_0_index = np.nonzero(schroeder)[0][0]-1
	time_index = db_0_index + int(t*fs)
	db = schroeder[time_index]
	multiplier = -60/db
	return t*fs*multiplier


# =============================================================================
# # F debe ser una lista de las frecuencias entregadas por la FFT de menor a mayor
# # AMP debe ser una lista de las amplitudes en dB de la FFT
# # OCT debe ser la subdivisión de octava (ej. OCT=3 -> Suavizado por tercios de octava)
# # OCT=0 es un caso especial donde no se realiza el suavizado y se devuelve la curva intacta
# # La función devuelve una lista con la curva suavizada de amplitudes en dB.
# =============================================================================
    
def suavizado(F,AMP,OCT):
    ampsmooth=AMP
    if OCT!=0:
        for n in range(1,len(F)):
            fsup=F[n]*pow(2,1/(2*OCT))  #calcula el corte superior del promedio
            finf=F[n]*pow(2,1/(2*OCT))  #calcula el corte inferior del promedio

            if F[-1]<=fsup:
                idxsup=len(F)-n
            else:
                idxsup=np.argmin(abs(F[n:]-fsup))   #busca el índice de fsup
                
            if F[1]<=finf:
                idxinf=np.argmin(abs(F[0:n+1]-finf))    #busca el ínfice de finf
            else:
                idxinf=0
                
            if idxsup!=idxinf+n:
                temp=pow(10,AMP[idxinf:idxsup+n-1]*0.1)
                ampsmooth[n]=10*np.log10(sum(temp)/(idxsup+n-idxinf))
    return ampsmooth


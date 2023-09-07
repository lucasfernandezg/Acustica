import scipy.signal as sc
import sounddevice as sd
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
# Fourier Class
# Acoustic Parameters => Filterbank
# 

### Funciones: ###


# Generador de Sweep y Filtro Inverso: #

def sweep(length, f0, f1, met,fs):
    t = np.linspace(0,length,int(fs*length))
    sw = sc.chirp(t,f0=f0,t1=t[-1],f1=f1,method=met)
    factor = np.exp((t*np.log(f1/f0))/length)
    inv = np.flip(sw)/factor
    return sw, inv


# Integral de Schroeder: #

def schroeder(rir):
    all = np.sum(rir**2)
    a = np.array([])
    for i in range(0,len(rir)):
        np.append(a, np.sum(rir[i:]**2))
    return 10*np.log10(a/all)


# Filtro de Media Movil: #

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


# Suavizado: #

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




###---- TEST ----###
sw, inv = sweep(3,100,10000,"logarithmic",44100)
# plt.figure()
# plt.plot(sw)
# plt.show()
#sd.play(sw,44100)
#sf.write("D:\Programacion\Python\Acustica\Sweep.wav",sw,44100)
#sf.write("D:\Programacion\Python\Acustica\Inv_filter.wav",inv,44100)

plt.figure()
plt.plot(np.convolve(sw,inv))
#plt.plot(schroeder(np.convolve(sw,inv)))
#plt.plot(inv)
plt.show()


import numpy as np
from Funciones import rms
import bottleneck as bn
import matplotlib.pyplot as plt

def lundeby(signal, fs, window = 1000):
    'calculation of the crossover point where the decay ends and the response is noise using the steps' 
    'indicated in the study by Lundeby et. to the. (Uncertainties of Measurements in Room Acoustics)'
    
    signal = signal[np.argmax(signal):]
    
    #1  Average squared impulse response
    padded = np.pad(signal, (window//2,  0), mode='edge')
    promediada = bn.move_mean(padded**2, window) 
    plt.figure()
    plt.plot(signal)
    plt.plot(promediada)
    plt.show()
    #2 Estimate background noise level using the tail
    ruido = int(len(promediada)/10)
    ruido_rms = rms(promediada[-ruido:])
    ruido_dBrms = 10* np.log10(ruido_rms)
    if ruido_dBrms <= -91:                                             
        ruido_dBrms = -100 
    
    #3 Estimate slope of decay from 0 dB to noise level
    with np.errstate(divide='ignore'): 
        promediada_dB = 10* np.log10(promediada)
    punto = np.where(promediada_dB >= 20 + ruido_dBrms)[0]
    if len(punto) == 0:
        punto = np.where(promediada_dB >= 10 + ruido_dBrms)[0]
        if len(punto) == 0:
            return ''
        else:
            punto = punto[-1]
    else:
        punto = punto[-1]
    if ruido_dBrms <= -91:                                              
        promediada_dB = promediada_dB[:punto+ 7*fs]                     
        promediada = promediada[:punto+ 7*fs]  
    x = np.arange(punto)
    coeficientes = np.polyfit(x, promediada_dB[:punto], 1)
    
    #Reinforcement---------------------------------------------------------------

    if np.isnan(coeficientes[0]):
        promediada = np.convolve(padded**2, np.ones((window,))/window, mode='valid')
        
        #2 Estimate background noise level using the tail
        ruido = int(len(promediada)/70)
        ruido_rms = rms(promediada[-ruido:])
        ruido_dBrms = 10* np.log10(ruido_rms)
        if ruido_dBrms <= -91:                                            
            ruido_dBrms = -100                                            
        
        #3 Estimate slope of decay from 0 dB to noise level
        promediada_dB = 10* np.log10(promediada)
        punto = np.where(promediada_dB >= 20 + ruido_dBrms)[0][-1]
        if len(punto) == 0:
            punto = np.where(promediada_dB >= 10 + ruido_dBrms)[0]
            if len(punto) == 0:
                return ''
            else:
                punto = punto[-1]
        else:
            punto = punto[-1]
        if ruido_dBrms <= -91:                                              
            promediada_dB = promediada_dB[:punto+ 5*fs]                     
            promediada = promediada[:punto+ 5*fs]                          
        x = np.arange(punto)
        coeficientes = np.polyfit(x, promediada_dB[:punto], 1)
                                  
    #------------------------------------------------------------------------------
    
    x2 = np.arange(len(promediada))
    ajustada = np.polyval(coeficientes, x2)
    if ajustada[0] > ajustada[1]:
    
        #4 Find preliminary crosspoint
        crosspoint_pre = np.where(ajustada >= ruido_dBrms)[0]
        if len(crosspoint_pre)== 0:
            crosspoint_pre = ''
        else:
            crosspoint_pre = crosspoint_pre[-1] 
        
            #5 Find new local time interval length
            new_interval = (np.where(ajustada >= ajustada[0]-10)[0][-1])//10
            
            #6  Average squared impulse response in new local time intervals
            if ruido_dBrms <= -91:                                                          
                padded2 = np.pad(signal[:punto+ 7*fs], (new_interval//2,  0), mode='edge')  
            else:                                                                           
                padded2 = np.pad(signal, (new_interval//2,  0), mode='edge') 
            promediada2 = bn.move_mean(padded2**2, new_interval) 
            with np.errstate(divide='ignore'):                                     
               promediada2_dB = 10* np.log10(promediada2)
            
            #Reinforcement 2----------------------------------------------------------------------------------------------
            if np.isin(True, np.isinf(promediada2_dB), assume_unique = False) == True:    
                promediada2 = np.convolve(padded2**2, np.ones((new_interval,))/new_interval, mode='valid')
                promediada2_dB = 10* np.log10(promediada2)
            #---------------------------------------------------------------------------------------------------------
            
            #7,8,9 Find crosspoint
            i = 0
            while i<5:
                #7
                nivel_final_dB = ajustada[crosspoint_pre]-10
                nivel_final = 10**(nivel_final_dB/10)
                ruido_dBrms_final = 10* np.log10(rms(promediada2[np.where(promediada2 >= nivel_final)[0][-1]:]))
                
                #8
                valores_sobre_ruido = np.where(promediada2_dB >= 5 + ruido_dBrms_final)[0]
                if len(valores_sobre_ruido)== 0:
                    crosspoint_pre = ''
                    break
                else:
                    punto2 = valores_sobre_ruido[-1]
                    x = np.arange(punto2)
                    coeficientes2 = np.polyfit(x, promediada2_dB[:punto2], 1)
                    x2 = np.arange(len(ajustada))
                    ajustada2 = np.polyval(coeficientes2, x2)
                    
                    #9
                    crosspoint_pre = np.where(ajustada2 >= ruido_dBrms_final)[0]
                    if len(crosspoint_pre) ==0:
                        return ''
                    else:
                        crosspoint_pre = crosspoint_pre[-1]
                    i +=1
    else:
        crosspoint_pre = ''
    
    
    return crosspoint_pre
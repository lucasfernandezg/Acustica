#! D:\Programacion\Python\admin\Scripts\python.exe

from Funciones import *
from FourierClass import Fourier
from PyOctaveBand import *

imp, fs = sf.read("Impulse.wav")

plt.figure()
plt.plot(imp)


imp_sch = np.round(schroederDB(imp),2)
start_cut = np.where(imp_sch == 0)[0][-1]
end_cut = np.where(imp_sch == -45)[0][0]
imp_sch = imp_sch[start_cut:end_cut]
imp_filt = mmf(imp_sch,50)
imp_corte = imp[start_cut:end_cut]

plt.figure()
plt.plot(imp_corte)
plt.figure()
plt.plot(imp_sch)
plt.plot(imp_filt)

plt.show()

print(T30(imp_sch,fs))
print(T20(imp_sch,fs))
print(T30(imp_filt,fs))

filtros, bandas, soses = filtrar(imp_corte, fs, False)

for i in filtros:
    imp_sch = np.round(schroederDB(filtros[i]),2)
    #start_cut = np.where(imp_sch == 0)[0][-1]
    #end_cut = np.where(imp_sch == -45)[0][0]
    #imp_sch = imp_sch[start_cut:end_cut]    
    print(i, " hz, t30: ", T30(imp_sch,fs))


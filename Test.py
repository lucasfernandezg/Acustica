#! D:\Programacion\Python\admin\Scripts\python.exe

from Funciones import *
from FourierClass import Fourier
from PyOctaveBand import *

imp, fs = sf.read("Impulse.wav")


sch, imp = schroeder(imp, fs, 45, False)

M=500
overlap = int(M/2)
sch_mmf = mmf(sch,M,overlap)



plt.figure()
plt.plot(imp/np.max(imp), label="Imp")
plt.plot(sch, label="sch")
plt.plot(sch_mmf,label=f"sch mmf M:{M}, overlap: {overlap}")
plt.legend()
plt.grid()
plt.show()
# plt.show()

# print(T30(imp_sch,fs))
# print(T20(imp_sch,fs))
# print(T30(imp_filt,fs))

# filtros, bandas, soses = filtrar(imp_corte, fs, False)

# for i in filtros:
#     imp_sch = np.round(schroederDB(filtros[i]),2)
#     #start_cut = np.where(imp_sch == 0)[0][-1]
#     #end_cut = np.where(imp_sch == -45)[0][0]
#     #imp_sch = imp_sch[start_cut:end_cut]    
#     print(i, " hz, t30: ", T30(imp_sch,fs))


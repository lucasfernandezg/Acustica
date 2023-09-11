#! D:\Programacion\Python\admin\Scripts\python.exe

from Funciones import *
#from FourierClass import Fourier
from PyOctaveBand import *

imp, fs = sf.read("Impulse.wav")

plt.figure()
plt.plot(imp)

sch, imp = schroeder(imp, fs, 45, False)

sw, inv = sweep(10, 200, 16000, "logarithmic", 48000)
# hann = np.hanning(fs/100)
# mid = index_where(hann, 1)
# addm = len(sw)-fs/100
# hann_win = np.concatenate((hann[:mid],np.ones(int(addm)),hann[mid:]))
# sw = hann_win*sw

sf.write("sweep.wav", sw, 48000)
sf.write("Filt_inv.wav", inv, 48000)

# M=500
# overlap = int(M/2)
# sch_mmf = mmf(sch,M,overlap)




# plt.figure()
# plt.plot(imp/np.max(imp), label="Imp")
# plt.plot(sch, label="sch")
# plt.plot(sch_mmf,label=f"sch mmf M:{M}, overlap: {overlap}")
# plt.legend()
# plt.grid()
# plt.show()
# plt.show()

# print(T30(imp_sch,fs))
# print(T20(imp_sch,fs))
# print(T30(imp_filt,fs))

# filtros, bandas, soses = filtrar(imp, fs)
# plt.figure()
# for i in soses:
#    f, h = sig.sosfreqz(i, fs=fs)
#    plt.semilogx(f,np.abs(h))
# plt.show()

# for i in filtros:
#     imp_sch = np.round(schroederDB(filtros[i]),2)
#     #start_cut = np.where(imp_sch == 0)[0][-1]
#     #end_cut = np.where(imp_sch == -45)[0][0]
#     #imp_sch = imp_sch[start_cut:end_cut]    
#     print(i, " hz, t30: ", T30(imp_sch,fs))


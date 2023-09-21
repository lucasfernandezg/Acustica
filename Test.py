#! D:\Programacion\Python\admin\Scripts\python.exe

from Funciones import *
#from FourierClass import Fourier
from PyOctaveBand import *
import sounddevice as sd
import soundfile as sf

sw, fs = sf.read("SiturRIR.wav")
inv, fs1 = sf.read("Filt_inv.wav")
print(fs, fs1)


# met = "log"
# f0 = 100
# f1 = 1000
# length = 3
# fs = 2000
# t = np.linspace(0,length,int(fs*length))

# sw = sig.chirp(t,f0=f0,t1=t[-1],f1=f1,method=met)
# sw = 0.5*sw
# factor = np.exp((t*np.log(f1/f0))/length)
# inv = np.flip(sw)/factor

inv = inv/np.max(inv)
# fs = 48000
# sw, inv = sweep(5.5,31,20000,fs)
s = sig.fftconvolve(sw,inv)
plt.figure()
plt.plot(s)
plt.show()
sf.write("Impulse_RICO_test_fft.wav",s, fs)





# imp, fs = sf.read("Impulse.wav")



# imp_est = mmf(imp,500,10)
# #mp_det = imp - imp_est
# sch_est, imp_est = schroeder(imp_est, fs, 45, False)
# #sch_det, imp_det = schroeder(imp_det, fs, 45, False)


# plt.figure()
# plt.plot(imp, label="imp")
# plt.plot(imp_est,label="Est")
# #plt.plot(imp_det, label="det")
# plt.legend()
# plt.grid()
# plt.show()

# plt.figure()
# #plt.plot(sch_det, label="det")
# plt.plot(sch_est,label="Est")
# #plt.plot(imp_det, label="det")
# plt.legend()
# plt.grid()
# plt.show()

# sw, inv = sweep(10, 200, 16000, "logarithmic", 48000)
# hann = np.hanning(fs/100)
# mid = index_where(hann, 1)
# addm = len(sw)-fs/100
# hann_win = np.concatenate((hann[:mid],np.ones(int(addm)),hann[mid:]))
# sw = hann_win*sw

# sf.write("sweep.wav", sw, 48000)
# sf.write("Filt_inv.wav", inv, 48000)

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


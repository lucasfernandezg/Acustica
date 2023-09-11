#! D:\Programacion\Python\admin\Scripts\python.exe
import Neutron
import sounddevice as sd
import numpy as np
from scipy import signal as sig
from Funciones import *

# All the CSS and HTML in this example is based on https://bbbootstrap.com/snippets/todo-list-jquery-and-font-awesome-icons-77769811

win = Neutron.Window("Example", size=(800, 500), css="def.css")

tasks = [0, 1, 2]
rec = []

def onClick():
    f0 = int(win.getElementById("f0").value)
    f1 = int(win.getElementById("f1").value)
    length = float(win.getElementById("length").value)
    fs = int(win.getElementById("fs").value)
    sw, filt = sweep(length, f0, f1, fs)
    r = sd.playrec(sw, fs, channels=1)
    global rec
    rec = r 

def onClickRec():
    sd.play(rec,44100)


def plotFigure():
#     if key == "Enter":
#         taskName = win.getElementById("addTask").value
#         taskId = len(tasks)

#         tasks.append(taskId)
        plt.figure()
        plt.plot(rec)
        name = "figure.png"
        
        plt.savefig(name)
        fig = f'<figure><img src="{name}" alt="Trulli" style="width:100%"><figcaption>Fig.1 - Trulli, Puglia, Italy.</figcaption></figure>'
        win.getElementById("figure").append(fig)

# def RemoveTask(taskid):
#     win.getElementById(taskid).remove()
    


win.display(file="render.html", pyfunctions=[onClick, onClickRec])
win.getElementById("play").addEventListener("click", Neutron.event(onClick))
win.getElementById("playRec").addEventListener("click", Neutron.event(onClickRec))
win.getElementById("plot").addEventListener("click", Neutron.event(plotFigure))
win.show()
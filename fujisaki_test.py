#!/usr/bin/python3
try:
  # for python2
  from Tkinter import *
except ImportError:
  # for python3
  from tkinter import *
  from tkinter import filedialog

import numpy as np
from numpy import arange
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
import scipy
import scipy.io
import scipy.io.wavfile as wavfile
from toshokan import File, Frame, Tieng
from sekkei import Config
import os, time
alpha = 3.0
beta = 20
gama = 0.9
def Gp(t):
  if t >= 0:
    return alpha * alpha * t * math.exp(- alpha * t)
  else:
    return 0
def Ga(t):
  if t >= 0:
    return min([gama, 1 - (1 + beta * t) * math.exp(- beta * t)])
  else:
    return 0
def F0(Fb, Ap, Aa):
  result = []
  lnFb = math.log(Fb)
  for t in range(max([len(Ap), len(Aa)])):
    phrase_sum = 0
    for idx, i in enumerate(Ap):
      if i != 0:
        phrase_sum += i * Gp(t - idx)
    accent_sum = 0
    Aai = None
    onset = None
    offset = None
    for idx, i in enumerate(Aa):
      if i != Aai:        
        if onset != None and offset != None:
          accent_sum += Aai * (Ga(t - onset) - Ga(t - offset))
          #print(Aai, onset, offset, "\n")
        Aai = i
        onset = idx
        offset = idx
      else:
        offset = idx

    result.append(lnFb + phrase_sum + accent_sum)
    t += 1
  return result

Ap = []
Aa = []
Fb = 140
for i in range(1000):
  if i % 50 == 0:
    Ap.append(1)
  else:
    Ap.append(0)

for i in range(100):
  if 5 <= i and i <= 10:
    Aa.append(1)
  elif 20 <= i and i <= 30:
    Aa.append(2)
  else:
    Aa.append(0)
mainWindow=Tk()

fig, ax = plt.subplots(3, 1, num='Sound Diagram')
fig.suptitle('fujisaki model', fontsize=20)
ax[0].plot(Ap)
ax[1].plot(Aa)
ax[2].plot(F0(Fb, Ap, Aa))
fig.show()

mainWindow.geometry('100x100+10+10')
mainWindow.title("Xu li am thanh")
Button(mainWindow,text="Thoat",command=quit).grid(row=9,column=1)
mainWindow.mainloop()


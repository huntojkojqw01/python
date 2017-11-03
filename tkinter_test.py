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
import math
import scipy
import scipy.io
import scipy.io.wavfile as wavfile

mainWindow=Tk()
# image = PhotoImage(file="./smilingpython.gif")
# label=Label(mainWindow,image=image,text="Nguyen Dinh Hung")
# label.grid(row=0,column=1)

fig, ax = plt.subplots(2, 1, num='Sound Diagram')
fig.suptitle('wav file', fontsize=20)
FRAME_DURATION = 0.02
frame_length = None
time_array = None
filename = "./khoosoothunhus.wav"
data = None
fs = None

def show():  
  global data,fs,filename,ax,fig,time_array,frame_length
  
  filename =  filedialog.askopenfilename(initialdir = "./",title = "Choose your file",filetypes = (("wav files","*.wav"),("mp3 files","*.mp3"),("all files","*.*")))
  
  # print(filename)
  try:
    fs, data = wavfile.read(filename)
  except (TypeError, FileNotFoundError):
    print("Chua chon file hop le.")
    return None
  data = data / (2. ** 15)    
  time_array=arange(0,len(data))/fs
  
  time = (float)(len(data) / fs);
  print("Fs: ", fs)
  print("Data: ", data)    
  print("Length: ", len(data))
  print("Time: ", time)
  ax[0].plot(time_array, data)      
  ax[0].set_xlabel('Time(s)')
  ax[0].set_ylabel('Amplitude')
  fig.show()    
def xac_dinh_khoang_lang():
  global data,fs,filename,ax,fig,time_array,frame_length
  if fs == None:
    return None
  ax[0].clear()
  fig.show()  
  ax[0].plot(time_array, data)      
  ax[0].set_xlabel('Time(s)')
  ax[0].set_ylabel('Amplitude') 
  
  # Lay frame length tu tren giao dien:
  tmp = None
  try:
    tmp = (float)(entry.get())
    if tmp <= 0:
      return None
  except ValueError:
    print("Oops!  Hay nhap gia tri frame length hop le vao !")
    tmp = FRAME_DURATION    
  frame_length = (int)(tmp * fs)
  #-----------------------------

  number_of_frame = int(len(data) / frame_length)  
  print("Frame length: ", frame_length)
  print("Number frame: ", number_of_frame)
  energy_array = []
  for i in range(0, len(data) - 1, frame_length):
    energy_array.append(sum(np.power(data[i:(i + frame_length - 1)], 2)))
  # print(np.array(energy_array).size)

  flag = 0 # flag = 0 tuc la dang trong khoang lang, khong co tieng noi.

  # Lay gia tri nguong nang luong tu giao dien:
  tmp = None
  try:
    tmp = (float)(entry2.get())
    if tmp <= 0:
      return None    
  except ValueError:
    print("Oops!  Hay nhap gia tri muc nang luong hop le vao !")
    tmp = 0.5
  nguong = tmp
  #-----------

  for i in range(0, len(energy_array) - 1):
    if math.sqrt(energy_array[i] + energy_array[i + 1]) >= nguong:
      if flag == 0:          
        ax[0].axvline(x=time_array[i*frame_length], color='blue', linestyle='-')
        flag = 1                
    else:
      if flag == 1:
        ax[0].axvline(x=time_array[i*frame_length], color='red', linestyle='--')
        flag = 0
  if flag == 1:
    ax[0].axvline(x=time_array[i*frame_length], color='red', linestyle='--')
  fig.show()

def tinh_f0():
  pass

def quit():
  mainWindow.quit()

# DANH SACH CAC THANH PHAN CUA GIAO DIEN:

button=Button(mainWindow,text="Chon file wav",command=show).grid(row=1,column=1)

label=Label(mainWindow,text="Do dai frame").grid(row=2,column=0)

entry = Entry(mainWindow)
entry.grid(row=2,column=1)

label2=Label(mainWindow,text="Muc nang luong").grid(row=3,column=0)

entry2 = Entry(mainWindow)
entry2.grid(row=3,column=1)

button2=Button(mainWindow,text="Xac dinh khoang lang",command=xac_dinh_khoang_lang).grid(row=4,column=1)

button3=Button(mainWindow,text="Tinh tan so f0",command=tinh_f0).grid(row=5,column=1)

mainWindow.geometry('280x160+10+10')
mainWindow.title("Xu li am thanh")
Button(mainWindow,text="Thoat",command=quit).grid(row=6,column=1)
mainWindow.mainloop()
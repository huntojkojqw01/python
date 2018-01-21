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
mainWindow=Tk()

fig, ax = plt.subplots(2, 1, num='Sound Diagram')
fig.suptitle('wav file', fontsize=20)

config = Config()
toa_do_frame = 0
sem = None
def show():
  global fai  
  filename =  filedialog.askopenfilename(initialdir = "./",
    title = "Choose your file",
    filetypes = (("wav files","*.wav"),("mp3 files","*.mp3"),("all files","*.*")))  
  
  try:    
    if not os.path.isfile(filename):      
      filename = config.ten_file
    else:
      config.ten_file = filename
    fai = File(filename)
  except (TypeError, FileNotFoundError):
    print("Chua chon file hop le.")
    return None 
   
  time = fai.time()
  print("Fs: ", fai.sample_rate())
  print("Data: ", fai.data())    
  print("Length: ", fai.length())
  print("Time: ", time)
  ax[0].clear()
  fig.show()  
  fai.show(ax[0])  
  fig.show()    
def xac_dinh_khoang_lang():
  ax[0].clear()
  fig.show()
  fai.show(ax[0])
  
  frame_length = config.do_dai_frame
  print("Frame length: ", frame_length)
  
  frames = fai.frames(frame_length)
  print("Number of frames: ", np.array(frames).size)  
  
  dang_trong_khoang_lang = True # tuc la dang trong khoang lang, khong co tieng noi.  
  nguong_nang_luong = config.nguong_nang_luong
  fs = fai.sample_rate()
  diem_dau = diem_cuoi = 0
  for frame in frames:       
    if frame.nang_luong() >= nguong_nang_luong:      
      if dang_trong_khoang_lang:        
        diem_dau = frame.toa_do()
        dang_trong_khoang_lang = False                
    else:
      if not dang_trong_khoang_lang:        
        diem_cuoi = frame.toa_do()        
        ax[0].axvspan(diem_dau / fs, diem_cuoi / fs, facecolor='g', alpha=0.5)
        dang_trong_khoang_lang = True
  if not dang_trong_khoang_lang:   
    diem_cuoi = frame.toa_do()    
    ax[0].axvspan(diem_dau / fs, diem_cuoi / fs, facecolor='g', alpha=0.5)
  fig.show()

def tinh_f0():
  global data,fs,filename,ax,fig,time_array,frame_length,energy_array,energy_index
  if fs == None:
    return None
  ax[1].clear()
  fig.show()  
  
  # Lay frame length tu tren giao dien:  
  try:
    tmp = float(entry.get())
    if tmp <= 0:
      return None
    else:
      frame_length = int(tmp * fs)
  except ValueError:
    # print("Oops!  Hay nhap gia tri frame length hop le vao !")      
    frame_length = int(FRAME_DURATION * fs)
  #----------------------------------------  

  data_length = len(data)
  if data_length % frame_length == 0:
    number_of_frame = int(data_length / frame_length)
  else:
    number_of_frame = int(data_length / frame_length) + 1

  print("Frame length: ", frame_length)
  print("Number frame: ", number_of_frame)
  
  if energy_array == None or len(energy_array) == 0:
    return None 
  half_frame_length = (int)(frame_length/2)
  # Lay gia tri nguong nang luong tu giao dien:
  nguong_nang_luong = None
  try:
    nguong_nang_luong = (float)(entry2.get())
    if nguong_nang_luong <= 0:
      return None    
  except ValueError:
    # print("Oops!  Hay nhap gia tri muc nang luong hop le vao !")
    nguong_nang_luong = 2  
  #-----------  
  count = 0
  # danh_sach_tan_so = []
  for i in energy_index:
    chi_so = energy_index.index(i)
    if chi_so == len(energy_index) - 1:
      t = ham_tu_tuong_quan_R_k(frame_length, data[i:len(data)])
    else:
      t = ham_tu_tuong_quan_R_k(frame_length, data[i:i+frame_length])
    chu_ky = cuc_dai_tiep_theo_cua_R(t)
      # danh_sach_tan_so.append(1.0/chu_ky)         
  # axs[2].plot(danh_sach_tan_so)
  fig.show()
def ve_tuong_quan_ben_canh(huong):
  global toa_do_frame, sem  
  frame_length = config.do_dai_frame
  half_frame_length = frame_length  >> 1
  if not sem is None:
    sem.remove()
  ax[1].clear()
  fig.show()

  frames = fai.frames(frame_length)

  if huong == 0:
    if toa_do_frame > 0:
      toa_do_frame -= 1
  else:
    if toa_do_frame < len(frames) - 1:
      toa_do_frame += 1

  current_frame = frames[toa_do_frame]
  vi_tri_dang_xet = current_frame.toa_do()
  fs = fai.sample_rate()
  sem = ax[0].axvline(x=vi_tri_dang_xet / fs, color='black', linestyle='-')  
  ax[1].plot(current_frame.ham_ttq())        
  ax[1].axvline(x=current_frame.chu_ky(), color='orange', linestyle='-')        
  print("Tan so la", current_frame.tan_so_co_ban(fs))  
  fig.show()

def choi():  
  fai.play()

def thiet_lap():
  try:
    tmp = (int)(entry.get())
    if 0 < tmp and tmp < fai.length():
      config.do_dai_frame = tmp          
  except ValueError:
    pass
  try:
    tmp = (int)(entry2.get())
    if 0 < tmp:
      config.nguong_nang_luong = tmp
  except ValueError: 
    pass
def quit():
  mainWindow.quit()

def onclick(event):
  global toa_do_frame  
  if event.inaxes is ax[0] and 0 <= event.xdata and event.xdata <= fai.length() / fai.sample_rate():    
    frame_length = config.do_dai_frame
    index = int(event.xdata * fai.sample_rate())
    toa_do_frame = math.floor(index * 2 / frame_length )
    if not sem is None: # neu dang ve thi ve lai voi vi tri moi.
      ve_tuong_quan_ben_canh(0)
fig.canvas.mpl_connect('button_press_event', onclick)

# DANH SACH CAC THANH PHAN CUA GIAO DIEN:

Button(mainWindow, text="Play", command=choi).grid(row=1, column=0)
button=Button(mainWindow,text="Chon file wav",command=show).grid(row=1,column=1)

label=Label(mainWindow,text="Do dai frame").grid(row=2,column=0)

entry = Entry(mainWindow)
entry.grid(row=2,column=1)

label2=Label(mainWindow,text="Muc nang luong").grid(row=3,column=0)

entry2 = Entry(mainWindow)
entry2.grid(row=3,column=1)

button2=Button(mainWindow,text="Thiet lap config",command=thiet_lap).grid(row=4,column=1)

button3=Button(mainWindow,text="Xac dinh khoang lang",command=xac_dinh_khoang_lang).grid(row=5,column=1)

button4=Button(mainWindow,text="<",command=lambda: ve_tuong_quan_ben_canh(0)).grid(row=6,column=0)
button5=Button(mainWindow,text="Hien thi f0",command=tinh_f0).grid(row=6,column=1)
button6=Button(mainWindow,text=">",command=lambda: ve_tuong_quan_ben_canh(1)).grid(row=6,column=2)

mainWindow.geometry('310x200+10+10')
mainWindow.title("Xu li am thanh")
Button(mainWindow,text="Thoat",command=quit).grid(row=7,column=1)
mainWindow.mainloop()
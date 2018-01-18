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

mainWindow=Tk()

fig, ax = plt.subplots(2, 1, num='Sound Diagram')
fig.suptitle('wav file', fontsize=20)
FRAME_DURATION = 0.04
frame_length = None
time_array = None
filename = "./khoosoothunhus.wav"
data = None
fs = None

def show():  
  global data,fs,filename,ax,fig,time_array,frame_length
  
  filename =  filedialog.askopenfilename(initialdir = "./",
    title = "Choose your file",
    filetypes = (("wav files","*.wav"),("mp3 files","*.mp3"),("all files","*.*")))  
  
  try:
    fs, data = wavfile.read(filename)
  except (TypeError, FileNotFoundError):
    print("Chua chon file hop le.")
    return None
  data = data / (2. ** 15)    
  time_array=arange(0, len(data)) / fs
  
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
  ax[0].plot(time_array, data, color="blue")      
  ax[0].set_xlabel('Time(s)')
  ax[0].set_ylabel('Amplitude')   
  
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
  
  energy_array = []  
  half_frame_length = (int)(frame_length/2)

  for i in range(0, data_length, half_frame_length):
    if i + half_frame_length >= data_length:
      energy_array.append(sum(np.power(data[i:data_length], 2)))
    else:
      energy_array.append(sum(np.power(data[i:(i + half_frame_length)], 2)))
  print("So luong tong: ", np.array(energy_array).size)
  
  dang_trong_khoang_lang = True # tuc la dang trong khoang lang, khong co tieng noi.

  # Lay gia tri nguong nang luong tu giao dien:
  nguong_nang_luong = None
  try:
    nguong_nang_luong = (float)(entry2.get())
    if nguong_nang_luong <= 0:
      return None    
  except ValueError:
    # print("Oops!  Hay nhap gia tri muc nang luong hop le vao !")
    nguong_nang_luong = 0.5  
  #-----------
  diem_dau = diem_cuoi = 0
  for i in range(0, len(energy_array)):
    if i == len(energy_array) - 1:
      nang_luong_cua_frame_nay = math.sqrt(energy_array[i] )
    else:
      nang_luong_cua_frame_nay = math.sqrt(energy_array[i] + energy_array[i + 1])
    toa_do_thoi_gian_cua_frame_nay = i * half_frame_length
    if nang_luong_cua_frame_nay >= nguong_nang_luong:
      if dang_trong_khoang_lang:          
        # ax[0].axvline(x=toa_do_thoi_gian_cua_frame_nay / fs, color='black', linestyle='-')
        diem_dau = toa_do_thoi_gian_cua_frame_nay
        dang_trong_khoang_lang = False                
    else:
      if not dang_trong_khoang_lang:
        # ax[0].axvline(x=toa_do_thoi_gian_cua_frame_nay / fs, color='black', linestyle='-')
        diem_cuoi = toa_do_thoi_gian_cua_frame_nay
        ax[0].plot(time_array[diem_dau:diem_cuoi], data[diem_dau:diem_cuoi], color="red")
        ax[0].axvspan(diem_dau / fs, diem_cuoi / fs, facecolor='g', alpha=0.5)
        dang_trong_khoang_lang = True
  if not dang_trong_khoang_lang:    
    # ax[0].axvline(x=toa_do_thoi_gian_cua_frame_nay / fs, color='black', linestyle='--')
    diem_cuoi = toa_do_thoi_gian_cua_frame_nay
    ax[0].plot(time_array[diem_dau:diem_cuoi], data[diem_dau:diem_cuoi], color="red")
    ax[0].axvspan(diem_dau / fs, diem_cuoi / fs, facecolor='g', alpha=0.5)
  fig.show()

def ham_tu_tuong_quan_R_k(frame_length, array): # i la chi so bat dau cua frame dang xet.
  N = frame_length
  K = (int)(4*N/5)

  R = []
  for k in range(0, K):
    sum = 0
    for n in range(0, N - k):
      sum += array[n] * array[n + k]
    R.append(sum)  
  return R
def cuc_dai_tiep_theo_cua_R(array):
  array_length = len(array)
  cuc_tieu_dau_tien = array.index(min(array[1:array_length]))
  return array.index(max(array[cuc_tieu_dau_tien+1:array_length]))
def tinh_f0():
  global data,fs,filename,ax,fig,time_array,frame_length
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
  
  energy_array = []  
  half_frame_length = (int)(frame_length/2)

  for i in range(0, data_length, half_frame_length):
    if i + half_frame_length >= data_length:
      energy_array.append(sum(np.power(data[i:data_length], 2)))
    else:
      energy_array.append(sum(np.power(data[i:(i + half_frame_length)], 2)))
  print("So luong tong: ", np.array(energy_array).size)
  
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
  for i in range(0, len(energy_array)):
    if i == len(energy_array) - 1:
      nang_luong_cua_frame_nay = math.sqrt(energy_array[i] )
    else:
      nang_luong_cua_frame_nay = math.sqrt(energy_array[i] + energy_array[i + 1])
    toa_do_cua_frame_nay = i * half_frame_length
    if nang_luong_cua_frame_nay >= nguong_nang_luong:
      count += 1
      t = ham_tu_tuong_quan_R_k(frame_length, data[toa_do_cua_frame_nay:toa_do_cua_frame_nay+frame_length])
      chu_ky = cuc_dai_tiep_theo_cua_R(t)
      # danh_sach_tan_so.append(1.0/chu_ky)
      if count == 1:
        ax[1].plot(t)        
        ax[1].axvline(x=chu_ky, color='orange', linestyle='-')        
        print("Tan so la",1.0/chu_ky)                
        # break    
  # axs[2].plot(danh_sach_tan_so)
  fig.show()

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
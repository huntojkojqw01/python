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
fig2, ax2 = plt.subplots(3, 2, num='Sound Diagram 2')
fig2.suptitle('hamming', fontsize=20)

config = Config()
toa_do_frame = 0
toa_do_tieng = 0
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
  ax[0].set_xlim(0, time)
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
  if not sem is None:
    sem.remove()
  ax[1].clear()
  fig.show()

  frame_length = config.do_dai_frame
  print("Frame length: ", frame_length)

  frames = fai.frames(frame_length)
  print("Number of frames: ", np.array(frames).size)

  dang_trong_khoang_lang = True # tuc la dang trong khoang lang, khong co tieng noi.
  nguong_nang_luong = config.nguong_nang_luong
  fs = fai.sample_rate()
  x_data = []
  y_data = []
  for frame in frames:
    if frame.nang_luong() >= nguong_nang_luong:
      if dang_trong_khoang_lang:
        diem_dau = frame.toa_do()
        dang_trong_khoang_lang = False
      else:
        x_data.append(frame.toa_do() / fs)
        y_data.append(frame.tan_so_co_ban(fs))
    else:
      if not dang_trong_khoang_lang:
        diem_cuoi = frame.toa_do()
        ax[1].axvspan(diem_dau / fs, diem_cuoi / fs, facecolor='g', alpha=0.5)
        dang_trong_khoang_lang = True
  if not dang_trong_khoang_lang:
    diem_cuoi = frame.toa_do()
    ax[1].axvspan(diem_dau / fs, diem_cuoi / fs, facecolor='g', alpha=0.1)
  fig.show()
  ax[1].scatter(x_data, y_data, s=5, c='blue')
  ax[1].set_xlim(0, math.ceil(fai.time()))
  ax[1].set_ylim(0, 600)
  ax[1].set_xlabel('Time(s)')
  ax[1].set_ylabel('F0(Hz)')
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
    else:
      config.do_dai_frame = int(fai.sample_rate() / 100) # tuc la 10ms
  except ValueError:
    pass
  try:
    tmp = (int)(entry2.get())
    if 0 < tmp:
      config.nguong_nang_luong = tmp
  except ValueError:
    pass

def xep_chong_du_lieu(data_goc, data_moi, vi_tri):
  i = vi_tri
  for x in data_moi:
    if i < len(data_goc):
      data_goc[i] = x
    else:
      data_goc.append(x)
    i+=1
def xu_li_tieng():
  tiengs = fai.tiengs(config.do_dai_frame, config.nguong_nang_luong)
  # print("So luong tieng", len(tiengs))
  # fai.show(ax2[0])
  # fs = fai.sample_rate()
  # for tieng in tiengs:
  #   diem_dau, diem_cuoi = tieng.toa_do()
  #   ax2[0].axvspan(diem_dau / fs, diem_cuoi / fs, facecolor='g', alpha=0.1)
  # fig2.show()

  # tieng = tiengs[toa_do_tieng]
  # tieng.show(ax2[0])
  # ax2[1].plot(np.hamming(tieng.length()))

  frame_length = config.do_dai_frame
  frame = tiengs[toa_do_tieng].frames(frame_length)[10]
  ax2[0][0].plot(frame.data())
  ax2[0][1].plot(frame.ham_ttq())
  hamming = np.hamming(frame_length)
  ax2[1][0].plot(hamming)

  i=0
  tmp = []
  for x in frame.data():
    tmp.append(x*hamming[i])
    i+=1
  ax2[2][0].plot(tmp)

  new_frame = Frame(np.array(tmp), 0, len(tmp))
  ax2[2][1].plot(new_frame.ham_ttq())

  fig2.show()

def nghe_tieng():
  tiengs = fai.tiengs(config.do_dai_frame, config.nguong_nang_luong)
  tiengs[toa_do_tieng].play()

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
button=Button(mainWindow,text="Choose wav file",command=show).grid(row=1,column=1)

label=Label(mainWindow,text="Frame length").grid(row=2,column=0)

entry = Entry(mainWindow)
entry.grid(row=2,column=1)

label2=Label(mainWindow,text="Energy").grid(row=3,column=0)

entry2 = Entry(mainWindow)
entry2.grid(row=3,column=1)

button2=Button(mainWindow,text="Set config",command=thiet_lap).grid(row=4,column=1)

# button3=Button(mainWindow,text="Xac dinh khoang lang",command=xac_dinh_khoang_lang).grid(row=5,column=1)

button4=Button(mainWindow,text="<",command=lambda: ve_tuong_quan_ben_canh(0)).grid(row=6,column=0)
button5=Button(mainWindow,text="F0 contour",command=tinh_f0).grid(row=6,column=1)
button6=Button(mainWindow,text=">",command=lambda: ve_tuong_quan_ben_canh(1)).grid(row=6,column=2)

# button7=Button(mainWindow,text="Tieng",command=xu_li_tieng).grid(row=7,column=1)
# button8=Button(mainWindow,text="nghe",command=nghe_tieng).grid(row=7,column=2)

mainWindow.geometry('350x250+10+10')
mainWindow.title("Sound")
Button(mainWindow,text="Exit",command=quit).grid(row=9,column=1)
mainWindow.mainloop()

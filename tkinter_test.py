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

import scipy
import scipy.io
import scipy.io.wavfile as wavfile

mainWindow=Tk()
image = PhotoImage(file="./smilingpython.gif")
label=Label(mainWindow,image=image,text="Nguyen Dinh Hung")
label.grid(row=0,column=1)

fig, ax = plt.subplots(2, 1, num='Sound Diagram')
fig.suptitle('Test wav file', fontsize=20)

def show():	
	global data,fs,filename,ax,fix
	
	# filename =  filedialog.askopenfilename(initialdir = "~/Music",title = "Choose your file",filetypes = (("wav files","*.wav"),("mp3 files","*.mp3"),("all files","*.*")))
	filename = "/home/hungnd/Music/khoosoothunhus.wav"
	if not filename is None:
		fs, data = wavfile.read(filename)
		print(fs)
		print(data)
		timeArray=arange(1,len(data)+1)/fs
		print(len(timeArray),len(data))			
		ax[0].plot(timeArray, data)
		ax[0].set_xlabel('Time')
		ax[0].set_ylabel('Amplitude')		
		fix.show()		
		
def showfft():
	global data,fs,filename,ax,fix
	print(filename,data,fs)
	print(np.fft.fft(data))
	X = np.linspace(-np.pi, np.pi, 256, endpoint=True)	
	C, S = np.cos(X), np.sin(X)
			
	ax[1].plot(X, C)
	ax[1].plot(X, S)	
	ax[1].set_xlabel('Freq (Hz)')
	ax[1].set_ylabel('|Y(freq)|')
	fix.show()

button=Button(mainWindow,text="Choose file",command=show)
button.grid(row=1,column=1)
button2=Button(mainWindow,text="FFT",command=showfft)
button2.grid(row=2,column=1)

mainWindow.geometry('280x350+0+0')
mainWindow.title("いいね")
mainWindow.mainloop()
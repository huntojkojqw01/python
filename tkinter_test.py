#!/usr/bin/python3
try:
	# for python2
	from Tkinter import *
except ImportError:	
	# for python3
	from tkinter import *
	from tkinter import filedialog

import numpy as np
import matplotlib.pyplot as plt

import scipy
import scipy.io
import scipy.io.wavfile as wavfile

mainWindow=Tk()
image = PhotoImage(file="./smilingpython.gif")
label=Label(mainWindow,image=image,text="Nguyen Dinh Hung")
label.grid(row=0,column=1)

def show():
	print("Ban vua bam nut "+label['text'])
	
	filename =  filedialog.askopenfilename(initialdir = "~/Music",title = "Choose your file",filetypes = (("wav files","*.wav"),("mp3 files","*.mp3"),("all files","*.*")))
	if not filename is None:
		fs, data = wavfile.read(filename)
		print(fs)
		print(data)
		X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
		print(X)
		C, S = np.cos(X), np.sin(X)

		plt.plot(X, C)
		plt.plot(X, S)

		plt.show()

button=Button(mainWindow,text="Choose file",command=show)
button.grid(row=1,column=1)

mainWindow.geometry('280x350+500+200')
mainWindow.title("いいね")
mainWindow.mainloop()
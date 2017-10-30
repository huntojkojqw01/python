#!/usr/bin/python3
try:
	# for python2
	from Tkinter import *
except ImportError:	
	# for python3
	from tkinter import *
	from tkinter import filedialog
import scipy
import scipy.io
import scipy.io.wavfile as wavfile
mainWindow=Tk()
# file = tkFileDialog.askopenfile(parent=mainWindow,mode='rb',title='Choose a file')
# if file != None:
#     data = file.read()
#     file.close()
#     print("I got %d bytes from this file.") % len(data)
logo = PhotoImage(file="./smilingpython.gif")
label=Label(mainWindow,image=logo,text="Nguyen Dinh Hung")
label.grid(row=0,column=1)

def show():
	print("Ban vua bam nut "+label['text'])
	
	filename =  filedialog.askopenfilename(initialdir = "~/Music",title = "Choose your file",filetypes = (("mp3 files","*.mp3"),("wav files","*.wav"),("all files","*.*")))
	tmp=wavfile.read(filename)
	print(tmp)	

button=Button(mainWindow,text="button",command=show)
button.grid(row=1,column=1)

mainWindow.geometry('280x350+500+200')
mainWindow.mainloop()
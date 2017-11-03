#!/usr/bin/python3
try:
    import tkinter as tk  # for python 3    
except:
    import Tkinter as tk  # for python 2
import pygubu,os,sys
import matplotlib
matplotlib.use('TkAgg')
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class Application:    
    def __init__(self, master):
        #1: Create a builder
        self.builder = builder = pygubu.Builder()
        #2: Load an ui file
        builder.add_from_file('giaodien.ui')
        #2.5: Set image path
        img_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
        img_path = os.path.abspath(img_path)
        builder.add_resource_path(img_path)
        #3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('mainwindow', master)        
        #4: Create callbacks        
        builder.connect_callbacks(self)
        #5: Cavans
        f = Figure(figsize=(5, 4), dpi=100)
        a = f.add_subplot(211)
        a.plot([1,2,3,4], [1,4,9,16], 'k-')
        a.set_title('a plot')
        a.set_xlabel('Xaa axis label')
        a.set_ylabel('Yaa label')

        b = f.add_subplot(212)
        b.plot([1,2,3,4,5], [10,5,10,5,10], 'r-')
        b.set_title('b plot')
        b.set_xlabel('Xbb axis label')
        b.set_ylabel('Ybb label')
        cv = self.builder.get_object('Canvas_1')
        # a tk.DrawingArea
        canvas = FigureCanvasTkAgg(f, master=cv)
        canvas.show()
        canvas.get_tk_widget().grid(row=1,column=1)
        # canvas._tkcanvas.grid(row=6,column=3)

    def choosefile(self):        
        print("bam btn chon file")
    def showfft(self):
        print("bam btn showfft")
    def playwav(self):
        print("bam btn play")
    def quit(self):
        sys.exit()    

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.title("いいですね")    
    root.mainloop()

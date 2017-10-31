#!/usr/bin/python3
try:
    import tkinter as tk  # for python 3
except:
    import Tkinter as tk  # for python 2
import pygubu,os,sys

def show():        
    print("bam btn 1")
def showfft():
    print("bam btn 2")
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
    
        #4: Configure callbacks
        callbacks = {
            'show': show,
            'showfft': showfft,
            'quit': sys.exit
        }
        builder.connect_callbacks(callbacks)        
    

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.title("いいですね")
    root.mainloop()

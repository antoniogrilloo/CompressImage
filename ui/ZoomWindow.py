from tkinter import ttk
from ui.CanvasImage import CanvasImage

class ZoomWindow(ttk.Frame):
    """ Main window class """
    def __init__(self, mainframe, image, zoom):
        """ Initialize the main Frame """
        ttk.Frame.__init__(self, master=mainframe)
        if zoom == 1:
            self.master.title('Original Image Zoom')
        else:
            self.master.title('Compressed Image Zoom')

        self.master.geometry('800x600')  # size of the main window
        self.master.rowconfigure(0, weight=1)  # make the CanvasImage widget expandable
        self.master.columnconfigure(0, weight=1)
        canvas = CanvasImage(self.master, image, self.master)  # create widget
        canvas.grid(row=0, column=0)  # show widget
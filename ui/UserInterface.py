import os
import tkinter as tk
import warnings
from threading import Thread
from tkinter import W, TRUE, FALSE, BOTH, N, E, ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

import numpy as np
from PIL import ImageTk, Image

import customtkinter
from customtkinter import StringVar
import time

from model.Compressor import Compressor

from ui.ZoomWindow import ZoomWindow


class UserInterface:

    def __init__(self):

        self.open_button = None
        self.zoom1_button = None
        self.zoom2_button = None

        self.root = customtkinter.CTk()
        self.root.geometry(str(self.root.winfo_screenwidth()) + "x" + str(self.root.winfo_screenheight()))
        self.root.title('Jpeg Compressor')

        self.canZoom = False

        self.image = StringVar()
        self.file_chosen = StringVar()
        self.file_chosen.set('Chose File')
        self.im = None

    def startUI(self):

        frame0 = customtkinter.CTkFrame(master=self.root, fg_color="transparent")
        frame0.pack(pady=30, expand=FALSE)

        self.frame1 = customtkinter.CTkFrame(master=frame0)
        self.frame1.grid(row=1, column=1, sticky=W)

        customtkinter.CTkLabel(master=self.frame1, text="Choose:", font=("calibri", 14, "bold")).grid(row=1, column=1,
                                                                                                      pady=10, sticky=N)

        frame2 = customtkinter.CTkFrame(master=self.frame1, fg_color="transparent")
        frame2.grid(row=2, column=1, padx=25, pady=10, sticky=E)

        self.frame3 = customtkinter.CTkFrame(master=frame0, fg_color="transparent")
        self.frame3.grid(row=1, column=2, padx=15, sticky=E)

        self.frame4 = customtkinter.CTkFrame(master=self.root)
        self.frame4.pack(fill=BOTH, expand=TRUE, padx=30, pady=(0, 30))

        self.root.update_idletasks()

        widthFrame = self.frame4.winfo_width()
        heighFrame = self.frame4.winfo_height()

        self.frame5 = customtkinter.CTkFrame(master=self.frame4)
        self.frame5.configure(height=480, width=widthFrame*0.35)
        self.frame5.grid(row=1, column=1, pady=(heighFrame*0.05, 0), padx=widthFrame*0.075)

        self.frame6 = customtkinter.CTkFrame(master=self.frame4)
        self.frame6.configure(height=480, width=widthFrame*0.35)
        self.frame6.grid(row=1, column=2, pady=(heighFrame*0.05, 0), padx=widthFrame*0.075)

        self.frame7 = customtkinter.CTkFrame(master=self.frame4, fg_color="transparent")
        self.frame7.grid(row=2, column=1)

        self.frame8 = customtkinter.CTkFrame(master=self.frame4, fg_color="transparent")
        self.frame8.grid(row=2, column=2)


        self.labelAnte = tk.Label(self.frame3)
        self.labelBefore = tk.Label(self.frame5)
        self.labelAfter = tk.Label(self.frame6)

        self.labelTextPreview = customtkinter.CTkLabel(self.frame3, text="Image preview",
                                                       font=("calibri", 14, "bold")).place(x=50, y=0)
        self.labelTextBefore = customtkinter.CTkLabel(self.frame7, text="Original image   ",
                                                      font=("calibri", 14, "bold")).grid(row=1, column=1)
        self.labelTetxAfter = customtkinter.CTkLabel(self.frame8, text="Compressed image   ",
                                                     font=("calibri", 14, "bold")).grid(row=1, column=1)

        customtkinter.CTkLabel(master=frame2, text="Image:", font=("calibri", 14, "bold")).grid(row=1, column=1,
                                                                                                sticky=W)
        self.open_button = customtkinter.CTkButton(
            frame2,
            text=self.file_chosen.get(),
            command=self.threading1,
            width=85,
            height=10,
            text_color='white',
            fg_color='#555555',
            hover_color='#555555'
        )

        self.open_button.grid(row=1, column=2)

        self.zoom1_button = customtkinter.CTkButton(
            self.frame7,
            text='Zoom',
            command=lambda: self.zoom(1),
            width=85,
            height=10,
            text_color='white',
            fg_color='#555555',
            hover_color='#555555'
        ).grid(row=1, column=2)

        self.zoom2_button = customtkinter.CTkButton(
            self.frame8,
            text='Zoom',
            command=lambda: self.zoom(2),
            width=85,
            height=10,
            text_color='white',
            fg_color='#555555',
            hover_color='#555555'
        ).grid(row=1, column=2)

        customtkinter.CTkLabel(master=frame2, text="Parameter F:   ", font=("calibri", 14, "bold")).grid(row=2,
                                                                                                         column=1,
                                                                                                         sticky=W)
        self.entry = customtkinter.CTkEntry(master=frame2,
                                            width=85,
                                            height=22,
                                            border_width=2,
                                            corner_radius=5)
        self.entry.grid(row=2, column=2, sticky=W)

        customtkinter.CTkLabel(master=frame2, text="Parameter D:   ", font=("calibri", 14, "bold")).grid(row=3,
                                                                                                         column=1,
                                                                                                         sticky=W)
        self.entry2 = customtkinter.CTkEntry(master=frame2,
                                             width=85,
                                             height=22,
                                             border_width=2,
                                             corner_radius=5)
        self.entry2.grid(row=3, column=2, sticky=W)

        customtkinter.CTkButton(self.frame1, text="Compress", command=self.threading2, width=150).grid(row=3, pady=10,
                                                                                                       column=1,
                                                                                                       sticky=N)

        self.progressbarPreview = customtkinter.CTkProgressBar(self.frame3, orientation="horizontal")
        self.progressbarPreview.configure(mode="indeterminate", width=100)

        self.progressbarBefore = customtkinter.CTkProgressBar(self.frame5, orientation="horizontal")
        self.progressbarBefore.configure(mode="indeterminate")

        self.progressbarAfter = customtkinter.CTkProgressBar(self.frame6, orientation="horizontal")
        self.progressbarAfter.configure(mode="indeterminate")

        self.last_filename = ""

        self.root.resizable(False, False)
        self.root.mainloop()


    def zoom(self, zoom):

        if self.canZoom == False:
            tk.messagebox.showerror(title=None, message='There is no image to zoom!')
            return

        if zoom == 1:
            ZoomWindow(tk.Tk(), Image.open(self.image.get()), 1)
        else:
            ZoomWindow(tk.Tk(), self.im, 2)


    def select_file(self):
        self.labelAnte.place_forget()
        self.root.update_idletasks()

        filetypes = (
            ('bmp files', '*.bmp'),
            ('png files', '*.png'),
            ('jpeg files', '*.jpeg'),
            ('jpg files', '*.jpg'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='.',
            filetypes=filetypes)
        if filename != '':
            self.last_filename = filename

        if filename == '' and self.last_filename != '':
            filename = self.last_filename

        self.image.set(filename)

        head_tail = os.path.split(filename)
        if head_tail[1] == '':
            self.open_button.configure(text='Chose File')
        else:
            if len(head_tail[1]) > 9:
                button_text = head_tail[1]
                if button_text[6] == '.':
                    button_text = button_text[0:6] + "..."
                else:
                    button_text = button_text[0:7] + "..."
                self.open_button.configure(text=button_text)
            else:
                self.open_button.configure(text=head_tail[1])

            self.labelBefore.place_forget()
            self.labelAfter.place_forget()

            self.canZoom = False

            self.progressbarPreview.place(x=50, y=110)
            self.progressbarPreview.start()
            self.root.update_idletasks()
            time.sleep(1)
            im = Image.open(filename)

            width, height = im.size
            if height > width:
                new_height = 160
                new_width = width * new_height / height
            else:
                new_width = 160
                new_height = height * new_width / width

            resized_image = im.resize((int(new_width), int(new_height)), Image.ANTIALIAS)
            test = ImageTk.PhotoImage(resized_image)

            self.labelAnte.configure(image=test)
            self.labelAnte.image = test
            if new_height == 160:
                asc = (180 - new_width) / 2
                self.labelAnte.place(x=asc + 10, y=37)
            else:
                ord = ((180 - new_height) / 2)
                self.labelAnte.place(x=17, y=ord)

            self.progressbarPreview.stop()
            self.progressbarPreview.place_forget()

    def threading1(self):
        t1 = Thread(target=self.select_file)
        t1.start()

    def threading2(self):
        t1 = Thread(target=self.show_before)
        t1.start()

    def threading3(self):
        t1 = Thread(target=self.compress)
        t1.start()

    def show_before(self):
        self.labelBefore.place_forget()
        self.labelAfter.place_forget()
        self.root.update_idletasks()

        filename = self.image.get()
        if filename == '':
            tk.messagebox.showerror(title=None, message='File not selected!')
            return
        while True:
            try:
                num = int(self.entry.get())
                break
            except:
                tk.messagebox.showerror(title=None, message='Parameter F not valid')
                return

        while True:
            try:
                num = int(self.entry2.get())
                break
            except:
                tk.messagebox.showerror(title=None, message='Parameter D not valid')
                return

        im = Image.open(filename)
        width, height = im.size
        min = 0
        if width < height:
            min = width
        else:
            min = height

        if int(self.entry.get()) > min or int(self.entry.get())<0:
            tk.messagebox.showerror(title=None, message='Parameter F not valid,  must be beetween 0 and ' + str(min))
            return
        if int(self.entry2.get()) < 0 or int(self.entry2.get()) >(2 * int(self.entry.get()) -2):
            tk.messagebox.showerror(title=None, message='Parameter D not valid,  must be beetween 0 and ' + str(2 * int(self.entry.get()) -2))
            return

        self.frame4.pack_propagate(False)
        self.progressbarBefore.place(x=150, y=250)
        self.progressbarBefore.start()
        self.root.update_idletasks()
        time.sleep(1)

        if height > width:
            new_height = 460
            new_width = width * new_height / height
        else:
            new_width = 460
            new_height = height * new_width / width

        resized_image = im.resize((int(new_width), int(new_height)), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(resized_image)

        self.labelBefore.configure(image=test)
        self.labelBefore.image = test

        if new_height >= new_width:
            y = (self.frame5.winfo_height() / 2) - (new_height / 2)
            x = (self.frame5.winfo_width() / 2) - (new_width / 2)
        elif new_width > new_height:
            y = (self.frame5.winfo_height() / 2) - (new_height / 2)
            x = (self.frame5.winfo_width() / 2) - (new_width / 2)

        self.labelBefore.place(x=x, y=y)

        self.progressbarBefore.stop()
        self.progressbarBefore.place_forget()
        self.threading3()

    def compress(self):
        self.frame4.pack_propagate(False)
        self.progressbarAfter.place(x=150, y=250)
        self.progressbarAfter.start()
        self.root.update_idletasks()

        time.sleep(1)

        self.im = np.asarray(Image.open(self.image.get()))

        c = Compressor(self.im, int(self.entry.get()), int(self.entry2.get()))
        self.im = c.compress()
        self.im = Image.fromarray(self.im.astype(np.uint8))

        width, height = self.im.size
        if height > width:
            new_height = 460
            new_width = width * new_height / height
        else:
            new_width = 460
            new_height = height * new_width / width

        resized_image = self.im.resize((int(new_width), int(new_height)), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(resized_image)

        self.labelAfter.configure(image=test)
        self.labelAfter.image = test

        if new_height >= new_width:
            y = (self.frame6.winfo_height() / 2) - (new_height / 2)
            x = (self.frame6.winfo_width() / 2) - (new_width / 2)
        elif new_width > new_height:
            y = (self.frame6.winfo_height() / 2) - (new_height / 2)
            x = (self.frame6.winfo_width() / 2) - (new_width / 2)

        self.labelAfter.place(x=x, y=y)

        self.progressbarAfter.stop()
        self.progressbarAfter.place_forget()

        self.canZoom = True

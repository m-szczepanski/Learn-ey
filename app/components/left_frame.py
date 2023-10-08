import tkinter as tk
from tkinter import PhotoImage



class LeftFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(width=696, height=698, bg="red")
        self.background_image = PhotoImage(file="./components/graphical_components/main_panel/left_frame.png")
        self.background = tk.Label(self, image=self.background_image)
        self.background.place(relwidth=1, relheight=1)
        self.pack(side="left")


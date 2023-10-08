import tkinter as tk
from tkinter import PhotoImage


class RightFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(width=265, height=698)
        self.background_image = PhotoImage(file="./components/graphical_components/main_panel/right_frame.png")
        self.background = tk.Label(self, image=self.background_image)
        self.background.place(relwidth=1, relheight=1)
        self.pack(side="right")

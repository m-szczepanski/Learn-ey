import tkinter as tk
from tkinter import PhotoImage
from app.components.frames.left_frame import LeftFrame
from app.components.frames.right_frame import RightFrame


class MainPanel:
    def __init__(self, root):
        self.panel = root
        self.panel.title("Learn-ey")
        self.panel.geometry('961x698')
        self.panel.resizable(False, False)
        self.background_image = PhotoImage(file="./components/graphical_components/shared/background.png")
        self.background = tk.Label(self.panel, image=self.background_image)
        self.background.place(relwidth=1, relheight=1)

        frame1 = LeftFrame(self.panel)
        frame2 = RightFrame(self.panel)

    def quit_app(self):
        self.panel.destroy()

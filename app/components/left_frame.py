import tkinter as tk
from tkinter import PhotoImage


class LeftFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(width=696, height=698)
        self.background_image = PhotoImage(file="./components/graphical_components/main_panel/left_frame.png")
        self.background = tk.Label(self, image=self.background_image)
        self.background.place(relwidth=1, relheight=1)
        self.pack(side="left")

        # top panel
        panels_position_x = [255, 463, 47, 255, 463]
        panels_position_y = [47, 57, 217, 217, 217]
        self.new_session_button_bg = (
            PhotoImage(file="./components/graphical_components/main_panel/add_session_button.png"))

        self.new_session_button = tk.Button(self, command=self.populate_top_panel, image=self.new_session_button_bg, bd=0,
                                            background='#9ed2be')
        self.new_session_button.place(x=50, y=42)

    def populate_top_panel(self):
        pass


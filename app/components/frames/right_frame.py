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

        self.main_panel_bg = PhotoImage(file="./components/graphical_components/main_panel/main_panel_button.png")
        self.about_button_bg = PhotoImage(file="./components/graphical_components/main_panel/about_button.png")
        self.quit_button_bg = PhotoImage(file="./components/graphical_components/main_panel/quit_button.png")
        self.main_panel_button = tk.Button(self, command=self.open_main_panel, image=self.main_panel_bg,
                                           bd=0, background='#cde3b6')
        self.main_panel_button.place(x=45, y=471)

        self.about_button = tk.Button(self, command=self.open_about, image=self.about_button_bg, bd=0,
                                      background='#cde3b6', highlightthickness=0, highlightbackground=self.cget("bg"))
        self.about_button.place(x=45, y=537)

        self.quit_button = tk.Button(self, command=self.quit_app, image=self.quit_button_bg, bd=0, background='#cde3b6',
                                     highlightthickness=0, highlightbackground='#cde3b6')
        self.quit_button.place(x=45, y=602)

    def open_main_panel(self):
        print('Main Panel button has been pressed')

    def open_about(self):
        print('About button has been pressed')

    def quit_app(self):
        from app.components.main_panel import MainPanel
        main_panel = MainPanel(self.master)
        main_panel.quit_app()

import tkinter as tk
from tkinter import PhotoImage


class PomodoroSettings:
    def __init__(self, root):
        self.root = root
        self.root.geometry("247x285")
        self.root.resizable(False, False)
        self.root.title("Settings")
        self.background_image = PhotoImage(file="./components/graphical_components/pomodoro/pomodoro_settings.png")
        self.background = tk.Label(self.root, image=self.background_image)
        self.background.place(relwidth=1, relheight=1)

        self.confirm_button_bg = PhotoImage(file="./components/graphical_components/pomodoro/confirm_button.png")
        self.default_button_bg = PhotoImage(file="./components/graphical_components/pomodoro/default_button.png")

        self.work_entry = tk.Entry(self.root, selectbackground="#c8e4b2")
        self.short_break_entry = tk.Entry(self.root)
        self.long_break_entry = tk.Entry(self.root)

        self.confirm_button = tk.Button(self.root, text="Confirm", bd=0, image=self.confirm_button_bg,
                                        command=self.confirm_settings, background="#c8e4b2")

        self.default_settings_button = tk.Button(self.root, text="Default Settings", bd=0, image=self.default_button_bg,
                                                 command=self.set_default_settings, background="#c8e4b2")

        self.work_entry.place(x=63, y=34)
        self.short_break_entry.place(x=63, y=98)
        self.long_break_entry.place(x=63, y=162)
        self.default_settings_button.place(x=11, y=231)
        self.confirm_button.place(x=135, y=231)


    def confirm_settings(self):
        work_min = self.work_entry.get()
        short_break_min = self.short_break_entry.get()
        long_break_min = self.long_break_entry.get()


    def set_default_settings(self):
        pass



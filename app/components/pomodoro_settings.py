import tkinter as tk
from tkinter import PhotoImage
import json


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

        self.work_entry = tk.Entry(self.root, width=10, background="#7eaa92", fg="white", bd=0, justify="center")
        self.short_break_entry = tk.Entry(self.root, width=10, background="#7eaa92", fg="white", bd=0, justify="center")
        self.long_break_entry = tk.Entry(self.root, width=10, background="#7eaa92", fg="white", bd=0, justify="center")

        self.confirm_button = tk.Button(self.root, text="Confirm", bd=0, image=self.confirm_button_bg,
                                        command=self.confirm_settings, background="#c8e4b2")

        self.default_settings_button = tk.Button(self.root, text="Default Settings", bd=0, image=self.default_button_bg,
                                                 command=self.set_default_settings, background="#c8e4b2")

        self.work_entry.place(x=92, y=40)
        self.short_break_entry.place(x=92, y=104)
        self.long_break_entry.place(x=92, y=168)
        self.default_settings_button.place(x=11, y=231)
        self.confirm_button.place(x=135, y=231)

    def confirm_settings(self):
        """Confirm the Pomodoro settings.

            This method confirms the Pomodoro settings by retrieving the values from the entry fields, updating
            the settings file, and closing the settings window.

            Args:
                self: The instance of the class.

            Returns:
                None.
            """
        work_min = self.work_entry.get()
        short_break_min = self.short_break_entry.get()
        long_break_min = self.long_break_entry.get()

        new_values = {
            "WORK_MIN": int(work_min),
            "SHORT_BREAK_MIN": int(short_break_min),
            "LONG_BREAK_MIN": int(long_break_min)
        }

        with open("components/Pomodoro/settings.json", "w") as json_file:
            json.dump(new_values, json_file)

        self.root.destroy()

    def set_default_settings(self):
        """Set the default Pomodoro settings.

            This method sets the default Pomodoro settings by updating the values in the settings file and closing
            the settings window.

            Args:
                self: The instance of the class.

            Returns:
                None.
            """
        default_values = {
            "WORK_MIN": 25,
            "SHORT_BREAK_MIN": 5,
            "LONG_BREAK_MIN": 20
        }

        with open("components/Pomodoro/settings.json", "w") as json_file:
            json.dump(default_values, json_file)

        self.root.destroy()

import tkinter as tk
from tkinter import PhotoImage
import math
import json
from app.components.pomodoro_settings import PomodoroSettings


BACKGROUND = "#cde3b6"
repetitions = 0
num_of_ticks = ""
timer = None


class MainPanel(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Learn-ey Main Panel")
        self.geometry('961x698')
        self.resizable(False, False)
        self.background_image = PhotoImage(file="./components/graphical_components/shared/background.png")
        self.background = tk.Label(self, image=self.background_image)
        self.background.place(relwidth=1, relheight=1)
        self.current_left_frame = None

        self.frames = {}

        # Utwórz ramki
        self.frames["left_frame"] = Frame1(self)
        self.frames["right_frame"] = Frame2(self)
        self.frames["word_frame"] = Frame3(self)

        self.open_initial_frames()

    def show_frame(self, frame_name):
        frame = self.frames.get(frame_name)
        if frame:
            if frame_name == 'right_frame':
                frame.pack(side="right", fill='y')
            else:
                frame.pack(side="left", fill='y')

            frame.tkraise()

            if self.current_left_frame:
                self.current_left_frame.forget()
                self.current_left_frame = frame

    def open_initial_frames(self):
        self.show_frame("left_frame")
        self.show_frame("right_frame")
        self.current_left_frame = self.frames['left_frame']


class Frame1(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
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

        self.new_session_button = tk.Button(self, command=lambda: master.show_frame("word_frame"),
                                            image=self.new_session_button_bg, bd=0, background='#9ed2be')
        self.new_session_button.place(x=50, y=42)

    def forget(self):
        self.pack_forget()


class Frame2(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(width=265, height=698)
        self.background_image = PhotoImage(file="./components/graphical_components/main_panel/right_frame.png")
        self.background = tk.Label(self, image=self.background_image)
        self.background.place(relwidth=1, relheight=1)
        self.pack(side="right")

        # Pomodoro section
        self.get_settings()

        self.timer = tk.Label(self, text="--:--", font=('Courier', 28, "normal"), fg="#FFD9B7", background="#dd2e44",
                              bd=0)
        self.timer.place(x=80, y=130)

        self.tick = tk.Label(self, text='', fg="#7EAA92", bg="#dd2e44", font=('Courier', 10, "bold"))
        self.tick.place(x=95, y=200)

        self.start_button_bg = PhotoImage(file="./components/graphical_components/pomodoro/pomodoro_start_button.png")
        self.options_button_bg = PhotoImage(file=
                                            "./components/graphical_components/pomodoro/pomodoro_options_button.png")
        self.stop_button_bg = PhotoImage(file="./components/graphical_components/pomodoro/pomodoro_stop_button.png")

        self.start_button = tk.Button(self, command=lambda: self.start_timer(),
                                      image=self.start_button_bg, bd=0, background=BACKGROUND)
        self.start_button.place(x=41, y=267)
        self.stop_button = tk.Button(self, command=self.reset_timer, image=self.stop_button_bg, bd=0,
                                     background=BACKGROUND)
        self.stop_button.place(x=110, y=267)

        self.options_button = tk.Button(self, command=self.open_settings, image=self.options_button_bg, bd=0,
                                        background=BACKGROUND)
        self.options_button.place(x=178, y=267)

        self.timer_state_idle_bg = PhotoImage(file="./components/graphical_components/pomodoro/start_the_timer.png")
        self.timer_state_learning_time_bg = PhotoImage(
            file="./components/graphical_components/pomodoro/learning_time.png")
        self.timer_state_quick_break_bg = PhotoImage(file="./components/graphical_components/pomodoro/quick_break.png")
        self.timer_state_long_break_bg = PhotoImage(file="./components/graphical_components/pomodoro/long_break.png")

        self.status_label = tk.Label(self, image=self.timer_state_idle_bg, fg="#FFD9B7", background="#c8e4b2", bd=0)
        self.status_label.place(x=50, y=333)

        # Menu section
        self.main_panel_bg = PhotoImage(file="./components/graphical_components/main_panel/main_panel_button.png")
        self.about_button_bg = PhotoImage(file="./components/graphical_components/main_panel/about_button.png")
        self.quit_button_bg = PhotoImage(file="./components/graphical_components/main_panel/quit_button.png")

        self.main_panel_button = tk.Button(self, command=lambda: master.show_frame("left_frame"), image=self.main_panel_bg,
                                           bd=0, background='#cde3b6')
        self.main_panel_button.place(x=38, y=471)

        self.about_button = tk.Button(self, command=self.open_about, image=self.about_button_bg, bd=0,
                                      background='#cde3b6', highlightthickness=0, highlightbackground=self.cget("bg"))
        self.about_button.place(x=38, y=537)

        self.quit_button = tk.Button(self, command=self.quit_app, image=self.quit_button_bg, bd=0, background='#cde3b6',
                                     highlightthickness=0, highlightbackground='#cde3b6')
        self.quit_button.place(x=38, y=602)

    def count_down(self, count):
        global num_of_ticks
        count_min = math.floor(count / 60)
        count_sec = count % 60
        if count_min < 10:
            count_min = f"0{count_min}"
        if count_sec == 0:
            count_sec = "00"
        elif count_sec < 10:
            count_sec = f"0{count_sec}"
        self.timer.config(text=f"{count_min}:{count_sec}")
        if count > 0:
            global timer
            timer = self.master.after(1000, self.count_down, count - 1)
        else:
            self.start_timer()
            if repetitions % 2 == 0:
                num_of_ticks += "✔️"
                self.tick.config(text=num_of_ticks)
            if repetitions % 8 == 0:
                num_of_ticks = ""
                self.tick.config(text=num_of_ticks)

    def reset_timer(self):
        global repetitions, num_of_ticks
        self.after_cancel(timer)
        self.timer.config(text="--:--")
        self.tick.config(text="")
        self.status_label.config(image=self.timer_state_idle_bg)
        repetitions = 0
        num_of_ticks = ""

    def open_settings(self):
        root = tk.Toplevel()
        settings_app = PomodoroSettings(root)

    def get_settings(self):
        with open("components/Pomodoro/settings.json", 'r') as pomodoro_settings:
            data = json.load(pomodoro_settings)
        work_min = data["WORK_MIN"]
        short_break_min = data["SHORT_BREAK_MIN"]
        long_break_min = data["LONG_BREAK_MIN"]
        return work_min, short_break_min, long_break_min

    def start_timer(self):
        global repetitions
        work_min, short_break_min, long_break_min = self.get_settings()
        repetitions += 1
        if repetitions % 8 == 0:
            self.count_down(int(long_break_min) * 60)
            self.status_label.config(image=self.timer_state_long_break_bg)
        elif repetitions % 2 == 0:
            self.count_down(int(short_break_min) * 60)
            self.status_label.config(image=self.timer_state_quick_break_bg)
        else:
            self.count_down(int(work_min) * 60)
            self.status_label.config(image=self.timer_state_learning_time_bg)

    def open_main_panel(self):
        print('Main Panel button has been pressed')
        from app.components.main_panel import MainPanel
        # self.master.destroy()

    def open_about(self):
        print('About button has been pressed')

    def quit_app(self):
        # from app.components.main_panel import MainPanel
        # main_panel = MainPanel(self.master)
        # main_panel.quit_app()
        self.master.destroy()


class Frame3(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(width=696, height=698)
        self.background_image = PhotoImage(file="./components/graphical_components/material_panel/word_section.png")
        self.background = tk.Label(self, image=self.background_image)
        self.background.place(relwidth=1, relheight=1)
        self.pack(side="left")


if __name__ == "__main__":
    app = MainPanel()
    app.mainloop()

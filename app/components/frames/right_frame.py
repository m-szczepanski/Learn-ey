import tkinter as tk
from tkinter import PhotoImage
import math

BACKGROUND = "#cde3b6"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
repetitions = 0
num_of_ticks = ""
timer = None
current_stare = "idle"


class RightFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(width=265, height=698)
        self.background_image = PhotoImage(file="./components/graphical_components/main_panel/right_frame.png")
        self.background = tk.Label(self, image=self.background_image)
        self.background.place(relwidth=1, relheight=1)
        self.pack(side="right")

    # Pomodoro section
        self.timer = tk.Label(self, text="--:--", font=('Courier', 28, "normal"), fg="#FFD9B7", background="#dd2e44",
                              bd=0)
        self.timer.place(x=80, y=130)

        self.tick = tk.Label(self, text='', fg="#7EAA92", bg="#dd2e44", font=('Courier', 10, "bold"))
        self.tick.place(x=95, y=200)

        self.start_button_bg = PhotoImage(file="./components/graphical_components/pomodoro/pomodoro_start_button.png")
        self.pause_button_bg = PhotoImage(file="./components/graphical_components/pomodoro/pomodoro_pause_button.png")
        self.stop_button_bg = PhotoImage(file="./components/graphical_components/pomodoro/pomodoro_stop_button.png")

        self.pause_button = tk.Button(self, command=self.open_about, image=self.pause_button_bg, bd=0,
                                      background=BACKGROUND)
        self.pause_button.place(x=44, y=267)
        self.pause_button.place(x=44, y=267)
        self.start_button = tk.Button(self, command=self.start_timer, image=self.start_button_bg, bd=0,
                                      background=BACKGROUND)
        self.start_button.place(x=112, y=267)
        self.stop_button = tk.Button(self, command=self.reset_timer, image=self.stop_button_bg, bd=0,
                                     background=BACKGROUND)
        self.stop_button.place(x=180, y=267)

        self.timer_state_idle_bg = PhotoImage(file="./components/graphical_components/pomodoro/start_the_timer.png")
        self.timer_state_learning_time = PhotoImage(file="./components/graphical_components/pomodoro/learning_time.png")
        self.timer_state_quick_break = PhotoImage(file="./components/graphical_components/pomodoro/quick_break.png")
        self.timer_state_long_break = PhotoImage(file="./components/graphical_components/pomodoro/long_break.png")

    # Menu section
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
        repetitions = 0
        num_of_ticks = ""

    def start_timer(self):
        global repetitions
        repetitions += 1
        if repetitions % 8 == 0:
            self.count_down(LONG_BREAK_MIN * 60)
            #title.config(text=f"Przerwa", fg=RED, font=(FONT_NAME, 28, "bold"))
        elif repetitions % 2 == 0:
            self.count_down(SHORT_BREAK_MIN * 60)
            #title.config(text=f"Przerwa", fg=PINK, font=(FONT_NAME, 28, "bold"))
        else:
            self.count_down(WORK_MIN * 60)
            #title.config(text=f"Praca", fg=GREEN, font=(FONT_NAME, 32, "bold"))

    def open_main_panel(self):
        print('Main Panel button has been pressed')

    def open_about(self):
        print('About button has been pressed')

    def quit_app(self):
        from app.components.main_panel import MainPanel
        main_panel = MainPanel(self.master)
        main_panel.quit_app()

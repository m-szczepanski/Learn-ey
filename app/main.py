import tkinter as tk
from tkinter import PhotoImage
import math
import json
from app.components.pomodoro_settings import PomodoroSettings
import threading
import time
from functions.safe_session import save_data
from functions.get_file_path import get_file_path
from functions.get_data_from_file import fetch_data
from tkinter import messagebox
import os
from functions.check_session_number import list_files_in_directory
from functions.get_session_date import get_file_creation_time
from functions.delete_session import delete_session

BACKGROUND = "#cde3b6"
repetitions = 0
num_of_ticks = ""
timer = None


class MainPanel(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Learn-ey")
        self.geometry('961x698')
        self.resizable(False, False)
        self.background_image = PhotoImage(file="./components/graphical_components/shared/background.png")
        self.background = tk.Label(self, image=self.background_image)
        self.background.place(relwidth=1, relheight=1)
        self.current_left_frame = None

        self.frames = {}

        self.frames["left_frame"] = LeftFrame(self)
        self.frames["right_frame"] = RightFrame(self)
        self.frames["word_frame"] = WordFrame(self)
        self.frames["expression_frame"] = ExpressionSection(self)
        self.frames["full_word_list"] = FullWordList(self)

        self.open_initial_frames()
        self.frames["right_frame"].set_main_panel_button_visibility(False)

    def show_frame(self, frame_name):
        if frame := self.frames.get(frame_name):
            if frame_name == 'left_frame':
                self.frames["right_frame"].set_main_panel_button_visibility(False)
                self.frames["left_frame"].update_top_panel()
            if frame_name == 'right_frame':
                frame.pack(side="right", fill='y')
            else:
                frame.pack(side="left", fill='y')
                self.frames['right_frame'].set_main_panel_button_visibility(True)

            frame.tkraise()

            self.frames['right_frame'].monitor_button_state()

            if self.current_left_frame:
                self.current_left_frame.forget()
                self.current_left_frame = frame

    def open_initial_frames(self):
        for frame in self.frames:
            if frame != ['left_frame', 'right_frame']:
                self.frames[frame].forget()

        self.show_frame("left_frame")
        self.show_frame("right_frame")
        self.current_left_frame = self.frames['left_frame']


class LeftFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(width=696, height=698)
        self.background_image = PhotoImage(file="./components/graphical_components/main_panel/left_frame.png")
        self.background = tk.Label(self, image=self.background_image)
        self.background.place(relwidth=1, relheight=1)
        self.pack(side="left")

        # top panel
        self.new_session_button_bg = (
            PhotoImage(file="./components/graphical_components/main_panel/add_session_button.png"))
        self.session_bg = PhotoImage(file="./components/graphical_components/main_panel/session_bg.png")
        self.session_delete_bg = PhotoImage(file="components/graphical_components/main_panel/delete_session.png")
        self.blank_session_bg = PhotoImage(file="components/graphical_components/main_panel/blank_session_panel.png")
        self.new_session_button = tk.Button(self, command=lambda: master.show_frame("word_frame"),
                                            image=self.new_session_button_bg, bd=0, background='#9ed2be')
        self.new_session_button.place(x=50, y=42)

        # bottom panel
        self.full_list_bg = PhotoImage(file="components/graphical_components/main_panel/full_list_button.png")
        self.full_list = tk.Button(self, image=self.full_list_bg, command=lambda: master.show_frame("full_word_list"),
                                   bd=0, bg="#9ed2be", width=188, height=62)
        self.full_list.place(x=468, y=569)

        self.german_button = tk.Button(self, text="German", font=('Inter', 18, "bold"), background="#7eaa92",
                                       fg="#FFD9B7", bd=0, width=11)
        self.german_button.place(x=61, y=487)

        self.polish_button = tk.Button(self, text="Polish", font=('Inter', 18, "bold"), background="#7eaa92",
                                       fg="#FFD9B7", bd=0, width=11)
        self.polish_button.place(x=270, y=487)

        self.spanish_button = tk.Button(self, text="Spanish", font=('Inter', 18, "bold"), background="#7eaa92",
                                        fg="#FFD9B7", bd=0, width=11)
        self.spanish_button.place(x=478, y=487)

        self.norwegian_button = tk.Button(self, text="Norwegian", font=('Inter', 18, "bold"), background="#7eaa92",
                                          fg="#FFD9B7", bd=0, width=11)
        self.norwegian_button.place(x=60, y=577)

        self.esperanto_button = tk.Button(self, text="Esperanto", font=('Inter', 18, "bold"), background="#7eaa92",
                                          fg="#FFD9B7", bd=0, width=11)
        self.esperanto_button.place(x=268, y=577)

    def update_top_panel(self):
        saved_sessions = list_files_in_directory("./data/session_data", 5)
        self.populate_session_panel(saved_sessions)

    def open_full_list(self):
        pass

    def populate_session_panel(self, saved_sessions):
        panels_position_x = [255, 463, 47, 255, 463]
        panels_position_y = [42, 42, 211, 211, 211]
        panels_date_position_y = [168, 168, 337, 337, 337]
        panels_name_position_x = [292, 499, 82, 293, 501]
        panels_name_position_y = [95, 95, 262, 262, 262]
        panels_delete_button_position_y = [49, 49, 218, 218, 218]

        sessions_number = len(saved_sessions)

        for i, session in enumerate(saved_sessions):
            session_label = tk.Label(self, image=self.session_bg, background="#9ed2be", bd=0)
            session_label.place(x=panels_position_x[i], y=panels_position_y[i])
            session_name = tk.Label(self, background="#7EAA92", font=('Inter', 30, "bold"), fg="#FFD9B7", bd=0,
                                    text=session[:-5])
            session_name.place(x=panels_name_position_x[i], y=panels_name_position_y[i])
            session_date = get_file_creation_time(saved_sessions[i])
            session_date_panel = tk.Label(self, background="#7eaa92", bd=0, font=('Inter', 10, "normal"), fg="#ffffff",
                                          text=session_date)
            session_date_panel.place(x=panels_position_x[i] + 60, y=panels_date_position_y[i])
            session_delete_button = tk.Button(self, image=self.session_delete_bg, background="#7eaa92", bd=0,
                                              command=lambda session=session: self.delete_session(session))
            session_delete_button.place(x=panels_position_x[i] + 158, y=panels_delete_button_position_y[i])

            while sessions_number < 5:
                session_label = tk.Label(self, image=self.blank_session_bg, background="#9ed2be", bd=0)
                session_label.place(x=panels_position_x[sessions_number], y=panels_position_y[sessions_number])
                sessions_number += 1

    def delete_session(self, session_name):
        if confirmation := messagebox.askyesno(
                "Delete session",
                f"Are you sure you want to delete this " f"session: {session_name[:-5]}?",
        ):
            delete_session(session_name)
            messagebox.showinfo("Success", f"{session_name[:-5]} has been deleted.")

        else:
            messagebox.showinfo("Info", f"{session_name[:-5]} has not been deleted.")
        self.update_top_panel()

    def forget(self):
        self.pack_forget()


class RightFrame(tk.Frame):
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
        self.main_panel_button_enabled = False

        self.main_panel_bg = PhotoImage(file="./components/graphical_components/main_panel/main_panel_button.png")
        self.about_button_bg = PhotoImage(file="./components/graphical_components/main_panel/about_button.png")
        self.quit_button_bg = PhotoImage(file="./components/graphical_components/main_panel/quit_button.png")

        self.main_panel_button = tk.Button(self, command=self.open_main_panel,
                                           image=self.main_panel_bg, bd=0, background='#cde3b6')
        self.main_panel_button.place(x=38, y=471)

        self.about_button = tk.Button(self, command=self.open_about, image=self.about_button_bg, bd=0,
                                      background='#cde3b6', highlightthickness=0, highlightbackground=self.cget("bg"))
        self.about_button.place(x=38, y=537)

        self.quit_button = tk.Button(self, command=self.quit_app, image=self.quit_button_bg, bd=0, background='#cde3b6',
                                     highlightthickness=0, highlightbackground='#cde3b6')
        self.quit_button.place(x=38, y=602)

        self.monitor_button_state()

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
        if self.main_panel_button_enabled:
            self.master.show_frame("left_frame")
            self.set_main_panel_button_visibility(False)

    def set_main_panel_button_visibility(self, value):
        self.main_panel_button_enabled = value

    def monitor_button_state(self):
        def check_state():
            while True:
                self.main_panel_button.config(state="normal") if self.main_panel_button_enabled else (
                    self.main_panel_button.config(state="disabled"))
                time.sleep(0.5)

        thread = threading.Thread(target=check_state)
        thread.daemon = True
        thread.start()


    def open_about(self):
        print('About button has been pressed')

    def quit_app(self):
        self.master.destroy()


class WordFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(width=696, height=698)
        self.background_image = PhotoImage(file="./components/graphical_components/material_panel/word_section.png")
        self.background = tk.Label(self, image=self.background_image)
        self.background.place(relwidth=1, relheight=1)
        self.pack(side="left")

        self.words = []
        self.translations = []

        self.next_one_button_bg = PhotoImage(file=
                                             "./components/graphical_components/material_panel/next_one_button.png")
        self.switch_button_bg = PhotoImage(file="./components/graphical_components/material_panel/switch_button.png")
        self.file_upload_bg = PhotoImage(file="./components/graphical_components/material_panel/file_upload.png")
        self.blank_button_bg = PhotoImage(file="./components/graphical_components/material_panel/blank_button.png")
        self.confirm_button_bg = PhotoImage(file="./components/graphical_components/material_panel/confirm_button.png")

        self.word_entry = tk.Entry(self, width=32, background="#7eaa92", fg="white", bd=0, justify="center",
                                   font=("Arial", 16))
        self.word_entry.place(x=210, y=164)

        self.translation_entry = tk.Entry(self, width=32, background="#7eaa92", fg="white", bd=0, justify="center",
                                          font=("Arial", 16))
        self.translation_entry.place(x=210, y=264)

        self.next_one = tk.Button(self, command=self.append_arrays, image=self.next_one_button_bg, bd=0,
                                  background='#9ed2be', highlightthickness=0)
        self.next_one.place(x=314, y=328)

        self.switch_button = tk.Button(self, command=lambda: master.show_frame("expression_frame"),
                                       image=self.switch_button_bg, bd=0, background='#9ed2be', highlightthickness=0)
        self.switch_button.place(x=425, y=416)

        self.upload_button = tk.Button(self, command=self.get_data_from_file,
                                       image=self.file_upload_bg, bd=0, background='#9ed2be', highlightthickness=0)
        self.upload_button.place(x=75, y=573)

        self.safe_as_label = tk.Entry(self, width=19, background="#7eaa92", fg="white", bd=0, justify="center",
                                      font=("Arial", 12))
        self.safe_as_label.place(x=448, y=569)
        self.safe_as_label.configure(takefocus=False)

        self.safe_as_button = tk.Button(self, command=self.safe_session, image=self.confirm_button_bg, bd=0,
                                        background='#9ed2be', highlightthickness=0)
        self.safe_as_button.place(x=442, y=609)

    def switch_panel_frame(self):
        pass

    def get_data_from_file(self):
        file_path = get_file_path()
        self.words, self.translations = fetch_data(file_path)

    def safe_session(self):
        session_name = self.safe_as_label.get()
        data_directory = "data/session_data"
        file_path = os.path.join(data_directory, f"{session_name}.json")
        if os.path.exists(file_path):
            messagebox.showinfo("Session name error", "Session with this name exists. Chose another name.")
            self.safe_as_label.delete(0, 'end')
        else:
            save_data(self.words, self.translations, session_name)
            self.safe_as_label.delete(0, 'end')


    def append_arrays(self):
        x = self.word_entry.get()
        y = self.translation_entry.get()
        if x != '' or y != '':
            self.words.append(x)
            self.translations.append(y)
            print(self.words, self.translations)
            self.word_entry.delete(0, 'end')
            self.translation_entry.delete(0, 'end')


class ExpressionSection(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(width=696, height=698)
        self.background_image = PhotoImage(file=
                                           "./components/graphical_components/material_panel/expression_section.png")
        self.background = tk.Label(self, image=self.background_image)
        self.background.place(relwidth=1, relheight=1)

        self.expressions = []
        self.definitions = []

        self.next_one_button_bg = PhotoImage(file=
                                             "./components/graphical_components/material_panel/next_one_button.png")
        self.switch_button_bg = PhotoImage(file="./components/graphical_components/material_panel/switch_button.png")
        self.file_upload_bg = PhotoImage(file="./components/graphical_components/material_panel/file_upload.png")
        self.blank_button_bg = PhotoImage(file="./components/graphical_components/material_panel/blank_button.png")
        self.confirm_button_bg = PhotoImage(file="./components/graphical_components/material_panel/confirm_button.png")

        self.expression_entry = tk.Entry(self, width=32, background="#7eaa92", fg="white", bd=0, justify="center",
                                   font=("Arial", 16))
        self.expression_entry.place(x=210, y=164)

        self.definition_entry = tk.Entry(self, width=32, background="#7eaa92", fg="white", bd=0, justify="center",
                                          font=("Arial", 16))
        self.definition_entry.place(x=210, y=264)

        self.next_one = tk.Button(self, command=self.append_arrays, image=self.next_one_button_bg, bd=0,
                                  background='#9ed2be', highlightthickness=0)
        self.next_one.place(x=314, y=328)

        self.switch_button = tk.Button(self, command=lambda: master.show_frame("word_frame"),
                                       image=self.switch_button_bg, bd=0, background='#9ed2be', highlightthickness=0)
        self.switch_button.place(x=425, y=416)

        self.upload_button = tk.Button(self, command=self.get_data_from_file,
                                       image=self.file_upload_bg, bd=0, background='#9ed2be', highlightthickness=0)
        self.upload_button.place(x=75, y=573)

        self.safe_as_label = tk.Entry(self, width=19, background="#7eaa92", fg="white", bd=0, justify="center",
                                      font=("Arial", 12))
        self.safe_as_label.place(x=448, y=569)
        self.safe_as_label.configure(takefocus=False)

        self.safe_as_button = tk.Button(self, command=self.safe_session,
                                        image=self.confirm_button_bg, bd=0, background='#9ed2be', highlightthickness=0)
        self.safe_as_button.place(x=442, y=609)

    def switch_panel_frame(self):
        pass

    def get_data_from_file(self):
        file_path = get_file_path()
        self.expressions, self.definitions = fetch_data(file_path)

    def safe_session(self):
        session_name = self.safe_as_label.get()
        data_directory = "data/session_data"
        file_path = os.path.join(data_directory, f"{session_name}.json")
        if os.path.exists(file_path):
            messagebox.showinfo("Session name error", "Session with this name exists. Chose another name.")
            self.safe_as_label.delete(0, 'end')
        else:
            save_data(self.expressions, self.definitions, session_name)
            self.safe_as_label.delete(0, 'end')

    def append_arrays(self):
        x = self.expression_entry.get()
        y = self.definition_entry.get()
        if x != '' or y != '':
            self.expressions.append(x)
            self.definitions.append(y)
            print(self.expressions, self.definitions)
            self.expression_entry.delete(0, 'end')
            self.definition_entry.delete(0, 'end')


class FullWordList(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(width=696, height=698)
        self.background_image = PhotoImage(file=
                                           "./components/graphical_components/material_panel/language_full_list.png")
        self.background = tk.Label(self, image=self.background_image)
        self.background.place(relwidth=1, relheight=1)
        self.create_buttons()

    def create_buttons(self):
        button_width = 11
        button_height = 1
        x_pos = [90, 285, 485]
        y_pos = [236, 296, 359, 418, 480, 541, 601]
        languages = list_files_in_directory("./data/words", 30)

        language_index = 0
        for row in range(7):
            for column in range(3):

                button = tk.Button(self, background="#7EAA92", fg="#FFD9B7", bd=0, width=button_width,
                                   height=button_height, text=languages[language_index][:-5], font=('Inter', 12, "bold"))
                button.place(x=x_pos[column], y=y_pos[row])
                language_index += 1

                if language_index >= len(languages):
                    break


if __name__ == "__main__":
    app = MainPanel()
    app.mainloop()

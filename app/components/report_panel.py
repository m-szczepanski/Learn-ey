import tkinter as tk
from tkinter import PhotoImage


class ReportPanel(tk.Toplevel):
    def __init__(self, wrong_answers, session_len):
        super().__init__()
        self.data = wrong_answers
        self.session_len = session_len
        self.title("Session report")
        self.geometry('426x555')
        self.resizable(False, False)
        self.wm_attributes("-topmost", True)
        self.background_image = PhotoImage(file="./components/graphical_components/shared/report_panel.png")
        self.background = tk.Label(self, image=self.background_image)
        self.background.place(relwidth=1, relheight=1)
        self.current_left_frame = None

        print("wrong answers: ", wrong_answers)
        print(f"you got {session_len - len(wrong_answers)}/{session_len}")

        self.frames = {}

        # self.frames["flashcard"] = Flashcard(self)
        # self.frames["flashcard"] = MatchDefinition(self)
        # self.frames["flashcard"] = TrueFalse(self)
        # self.frames["flashcard"] = PickCorrect(self)
        # self.frames["flashcard"] = Hangman(self)

    def show_frame(self, frame_name):
        if frame := self.frames.get(frame_name):
            frame.tkrise()

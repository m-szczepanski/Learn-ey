import tkinter as tk
from tkinter import PhotoImage
from app.functions.csv_to_dict import read_csv_to_dict
from app.functions.distribute_session_data import distribute_data_json


class LearningSession(tk.Toplevel):
    def __init__(self, session):
        super().__init__()
        self.learning_session = session
        self.title(f"Flashcard - {self.learning_session}")
        self.geometry("681x686")
        self.resizable(False, False)
        self.wm_attributes("-topmost", True)

        self.frames = {}

        # self.frames["flashcard"] = Flashcard(self)
        # self.frames["flashcard"] = MatchDefinition(self)
        # self.frames["flashcard"] = TrueFalse(self)
        # self.frames["flashcard"] = PickCorrect(self)
        # self.frames["flashcard"] = Hangman(self)

        (self.flashcard_dict, self.match_expression_dict, self.match_translation_dict, self.tf_dict, self.pick_dict,
         self.hangman_dict) = distribute_data_json(self.learning_session)

        print("flashcard: ", self.flashcard_dict)
        print("match_expression: ", self.match_expression_dict)
        print("match_translation: ", self.match_translation_dict)
        print("tf: ", self.tf_dict)
        print("pick: ", self.pick_dict)
        print("hangman: ", self.hangman_dict)



        #


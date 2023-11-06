import tkinter as tk
from tkinter import PhotoImage
import random
import pandas as pd


class WordFlashcard(tk.Toplevel):
    def __init__(self, language):
        super().__init__()
        self.chose_language = language
        self.geometry("681x686")
        self.resizable(False, False)
        self.wm_attributes("-topmost", True)

        # self.background_image = PhotoImage(file="app/components/graphical_components/flashcard/flashcard_panel.png")
        # self.background = tk.Label(self, image=self.background_image)
        # self.background.place(relwidth=1, relheight=1)
        # self.text = tk.Label(self, text="dupa")
        # self.text.pack()

        self.background_image = PhotoImage(file=
                                           "./components/graphical_components/flashcard/flashcard_panel.png")
        self.background = tk.Label(self, image=self.background_image)
        self.background.place(relwidth=1, relheight=1)

        self.language = ''

        self.flashcard_front_bg = PhotoImage(file="./components/graphical_components/flashcard/flashcard_front.png")
        self.flashcard_back_bg = PhotoImage(file="./components/graphical_components/flashcard/flashcard_back.png")
        self.flip_button_bg = PhotoImage(file="./components/graphical_components/flashcard/flip_button.png")
        self.canvas_background = PhotoImage(file="./components/graphical_components/flashcard/canvas_bg.png")
        self.yes_button_bg = PhotoImage(file="./components/graphical_components/flashcard/yes_button.png")
        self.no_button_bg = PhotoImage(file="./components/graphical_components/flashcard/no_button.png")

        self.canvas = tk.Canvas(self, width=616, height=311, bg="#7EAA92", highlightthickness=0)
        self.canvas_bg = self.canvas.create_image(260, 200, anchor=tk.NW, image=self.flashcard_front_bg)
        self.card_language = self.canvas.create_text(300, 50, text="Language", font=("Inter", 30, "normal"),
                                                     fill="#FFD9B7")
        self.card_word = self.canvas.create_text(300, 163, text="word", font=("Inter", 80, "bold"), fill="#FFFFFF")
        self.canvas.place(x=32, y=62)

        self.flip_button = tk.Button(self, image=self.flip_button_bg, command=self.flip_card, bd=0, bg="#9ED2BE")
        self.flip_button.place(x=248, y=398)

        self.unknown_button = tk.Button(self, image=self.no_button_bg, command=lambda: self.next_card(
            self.checked_language),
                                        bd=0, bg="#9ED2BE")
        self.unknown_button.place(x=82, y=488)

        self.known_button = tk.Button(self, image=self.yes_button_bg, command=self.is_known, bd=0, bg="#9ED2BE")
        self.known_button.place(x=448, y=488)

        self.print_lang()

    def print_lang(self):
        print(self.chose_language)

    def next_card(self, language):
        title = language.capitalize()
        current_card = random.choice(self.dict)
        self.canvas.itemconfig(self.card_language, text=f"{title}", fill="#FFD9B7")
        self.canvas.itemconfig(self.card_word, text=current_card[f"{title}"], fill="White")
        self.canvas.itemconfig(self.canvas_bg, image=self.flashcard_front_bg)

    def flip_card(self):
        self.canvas.itemconfig(self.canvas_bg, image=self.flashcard_back_bg)
        self.canvas.itemconfig(self.card_word, text="English", fill="white")
        self.canvas.itemconfig(self.card_word, text=self.current_card["English"], fill="white")

    def is_known(self):
        self.to_learn.remove(self.current_card)
        data = pd.DataFrame(self.to_learn)
        data.to_csv("./data/words_to_learn.csv", index=False)
        self.next_card(self.checked_language)

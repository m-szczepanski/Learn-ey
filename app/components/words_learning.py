import tkinter as tk
from tkinter import PhotoImage
import random
import pandas as pd
from app.functions.csv_to_dict import read_csv_to_dict


class WordFlashcard(tk.Toplevel):
    def __init__(self, language):
        super().__init__()
        self.picked_lang = language
        self.lang_name = self.picked_lang.capitalize()
        self.geometry("681x686")
        self.resizable(False, False)
        self.wm_attributes("-topmost", True)

        self.background_image = PhotoImage(file=
                                           "./components/graphical_components/flashcard/flashcard_panel.png")
        self.background = tk.Label(self, image=self.background_image)
        self.background.place(relwidth=1, relheight=1)

        self.flashcard_front_bg = PhotoImage(file="./components/graphical_components/flashcard/flashcard_front.png")
        self.flashcard_back_bg = PhotoImage(file="./components/graphical_components/flashcard/flashcard_back.png")
        self.flip_button_bg = PhotoImage(file="./components/graphical_components/flashcard/flip_button.png")
        self.canvas_background = PhotoImage(file="./components/graphical_components/flashcard/canvas_bg.png")
        self.yes_button_bg = PhotoImage(file="./components/graphical_components/flashcard/yes_button.png")
        self.no_button_bg = PhotoImage(file="./components/graphical_components/flashcard/no_button.png")

        self.canvas = tk.Canvas(self, width=616, height=311, bg="#9ed2be", highlightthickness=0)
        self.canvas_bg = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.flashcard_front_bg)
        self.card_language = self.canvas.create_text(300, 50, text="Language", font=("Inter", 30, "normal"),
                                                     fill="#FFD9B7")
        self.card_word = self.canvas.create_text(300, 163, text="word", font=("Inter", 80, "bold"), fill="#FFFFFF")
        self.canvas.place(x=32, y=62)

        self.flip_button = tk.Button(self, image=self.flip_button_bg, command=self.flip_card, bd=0, bg="#9ED2BE")
        self.flip_button.place(x=248, y=398)

        self.unknown_button = tk.Button(self, image=self.no_button_bg, command=lambda: self.next_card(),
                                        bd=0, bg="#9ED2BE")
        self.unknown_button.place(x=82, y=488)

        self.known_button = tk.Button(self, image=self.yes_button_bg, command=self.is_known, bd=0, bg="#9ED2BE")
        self.known_button.place(x=448, y=488)

        self.print_lang()

        self.current_card = {}

        self.dict = read_csv_to_dict(f"./data/words/{self.picked_lang}.csv", self.lang_name)
        print(dict)
        self.next_card()

    def print_lang(self):
        print(self.picked_lang)

    def next_card(self):
        if self.dict:
            self.current_card = random.choice(list(self.dict.items()))
            print(self.current_card)
            self.canvas.itemconfig(self.card_language, text=self.lang_name, fill="#FFD9B7")
            self.canvas.itemconfig(self.card_word, text=self.current_card[0], fill="white")
        else:
            # Jeśli słownik jest pusty, to nie ma kart do wyświetlenia.
            self.current_card = None
            self.canvas.itemconfig(self.card_language, text="No cards remaining", fill="#FFD9B7")
            self.canvas.itemconfig(self.card_word, text="", fill="white")

        self.canvas.itemconfig(self.canvas_bg, image=self.flashcard_front_bg)

    # def flip_card(self):
    #     if self.current_card:
    #         self.canvas.itemconfig(self.canvas_bg, image=self.flashcard_back_bg)
    #         #self.canvas.itemconfig(self.canvas,)
    #         self.canvas.itemconfig(self.card_word, text=self.current_card[1], fill="white")
    #         self.canvas.itemconfig(self.card_word, text=self.dict[self.current_card[0]], fill="white")
    def flip_card(self):
        if self.current_card:
            if self.canvas.itemcget(self.canvas_bg, "image") == str(self.flashcard_front_bg):
                # Jeśli karta jest z przodu, to obróć na tył
                self.canvas.itemconfig(self.canvas_bg, image=self.flashcard_back_bg)
                self.canvas.itemconfig(self.card_word, text=self.current_card[1], fill="white")
                self.canvas.itemconfig(self.card_language, text="English", fill="black")
            else:
                # Jeśli karta jest z tyłu, to obróć na przód
                self.canvas.itemconfig(self.canvas_bg, image=self.flashcard_front_bg)
                self.canvas.itemconfig(self.card_word, text=self.current_card[0], fill="white")
                self.canvas.itemconfig(self.card_language, text=self.lang_name, fill="#FFD9B7")

    def is_known(self):
        if self.current_card:
            del self.dict[self.current_card[0]]
            self.next_card()

import tkinter as tk
from tkinter import PhotoImage
import random
from app.functions.csv_to_dict import read_csv_to_dict
from app.functions.open_session_report import open_session_report


class WordFlashcard(tk.Toplevel):
    def __init__(self, language):
        super().__init__()
        self.picked_lang = language
        self.lang_name = self.picked_lang.capitalize()
        self.title(f"Flashcard - {self.lang_name}")
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
        self.card_word = self.canvas.create_text(300, 163, text="word", font=("Inter", 70, "bold"), fill="#FFFFFF")
        self.canvas.place(x=32, y=62)

        self.flip_button = tk.Button(self, image=self.flip_button_bg, command=self.flip_card, bd=0, bg="#9ED2BE")
        self.flip_button.place(x=248, y=398)

        self.unknown_button = tk.Button(self, image=self.no_button_bg, command=lambda: self.is_unknown(),
                                        bd=0, bg="#9ED2BE")
        self.unknown_button.place(x=82, y=488)

        self.known_button = tk.Button(self, image=self.yes_button_bg, command=self.is_known, bd=0, bg="#9ED2BE")
        self.known_button.place(x=448, y=488)

        self.current_card = {}
        self.unknown = {}

        self.dict = read_csv_to_dict(f"./data/words/{self.picked_lang}.csv", self.lang_name)
        self.dict_len = len(self.dict)

        self.protocol("WM_DELETE_WINDOW", lambda: self.force_close(self.unknown, self.dict_len))
        self.draw_card()

    def draw_card(self):
        """Move to the next flashcard.

            This method moves to the next flashcard by selecting a random card from the dictionary and updating the
            canvas with the card details. If the dictionary is empty, it closes the learning session and opens the
            session report.

            Args:
                self: The instance of the class.

            Returns:
                None.
            """
        if self.dict:
            self.current_card = random.choice(list(self.dict.items()))
            self.canvas.itemconfig(self.card_language, text=self.lang_name, fill="#FFD9B7")
            self.canvas.itemconfig(self.card_word, text=self.current_card[0], fill="white")
        else:
            # If dictionary is empty, there's no cards to display.
            self.current_card = None
            self.canvas.itemconfig(self.card_language, text="No cards remaining", fill="#FFD9B7")
            self.canvas.itemconfig(self.card_word, text="", fill="white")
            self.close()
            open_session_report(self.unknown, self.dict_len)

        self.canvas.itemconfig(self.canvas_bg, image=self.flashcard_front_bg)

    def flip_card(self):
        """Flip the flashcard.

            This method flips the flashcard from the front side to the back side, or vice versa.

            Args:
                self: The instance of the class.

            Returns:
                None.
            """
        if self.current_card:
            if self.canvas.itemcget(self.canvas_bg, "image") == str(self.flashcard_front_bg):
                # If the card is faced upwards, flip to the backside
                self.canvas.itemconfig(self.canvas_bg, image=self.flashcard_back_bg)
                self.canvas.itemconfig(self.card_word, text=self.current_card[1], fill="#7eaa92")
                self.canvas.itemconfig(self.card_language, text="English", fill="black")
            else:
                # If the card is faced downwards, flip to the front-side
                self.canvas.itemconfig(self.canvas_bg, image=self.flashcard_front_bg)
                self.canvas.itemconfig(self.card_word, text=self.current_card[0], fill="white")
                self.canvas.itemconfig(self.card_language, text=self.lang_name, fill="#FFD9B7")

    def is_known(self):
        """Check if the current flashcard is known.

            This method checks if the current flashcard is known, and if so, removes it from the dictionary and
            moves to the next flashcard.

            Args:
                self: The instance of the class.

            Returns:
                None.
            """
        if self.current_card:
            del self.dict[self.current_card[0]]
            self.draw_card()

    def is_unknown(self):
        """Put current card to unknown list..

           This method adds current flashcard to the `unknown` dictionary and moves to the next flashcard.

           Args:
               self: The instance of the class.

           Returns:
               None.
           """
        if self.current_card:
            self.unknown[self.current_card[0]] = self.current_card[1]
            del self.dict[self.current_card[0]]
            self.draw_card()

    def close(self):
        """Close the window.

           This method closes the window.

           Args:
               self: The instance of the class.

           Returns:
               None.
           """
        self.destroy()

    def force_close(self, unknown, dict_len):
        """Force close the window.

            This method forces the window to close and opens the session report.

            Args:
                self: The instance of the class.
                unknown (dict): A dictionary containing unknown flashcards.
                dict_len (int): The length of the flashcard dictionary.

            Returns:
                None.
            """
        self.close()
        open_session_report(unknown, dict_len)

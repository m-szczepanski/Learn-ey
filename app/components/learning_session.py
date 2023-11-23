import tkinter as tk
from tkinter import PhotoImage
from app.functions.distribute_session_data import distribute_data_json
import random
from tkinter import messagebox


class LearningSession(tk.Toplevel):
    def __init__(self, session):
        super().__init__()
        self.learning_session = session
        self.title(f"Session: {self.learning_session}")
        self.geometry("681x686")
        self.resizable(False, False)
        self.wm_attributes("-topmost", True)

        self.frames = {}

        (self.flashcard_dict, self.match_expression_dict, self.match_translation_dict, self.tf_dict, self.pick_dict,
         self.hangman_dict) = distribute_data_json(self.learning_session)
        # debug
        print("flashcard: ", self.flashcard_dict)
        print("match_expression: ", self.match_expression_dict)
        print("match_translation: ", self.match_translation_dict)
        print("tf: ", self.tf_dict)
        print("pick: ", self.pick_dict)
        print("hangman: ", self.hangman_dict)

        self.chosen_dict, self.dict_name = self.random_dict()
        print("dict name: ", self.dict_name)

        key, value = self.get_random_key_value()
        wrong_answers = self.get_different_values(value, self.chosen_dict, 3)

        self.frames["flashcard"] = Flashcard(self, key, value)
        self.frames["match_expression"] = MatchExpression(self, key, value, wrong_answers)
        self.frames["match_translation"] = MatchTranslation(self, key, value, wrong_answers)
        self.frames["tf"] = TrueFalse(self, key, value)
        self.frames["pick"] = PickCorrect(self, key, value, wrong_answers)
        self.frames["hangman"] = Hangman(self, key, value)

        self.show_frame(self.dict_name)
        self.open_next_frame()

    def show_frame(self, frame_name):
        if frame := self.frames.get(frame_name):
            frame.tkraise()

            for name, other_frame in self.frames.items():
                if name != frame_name:
                    other_frame.forget()

    def random_dict(self, consecutive_limit=3):
        dict_choices = [
            ("flashcard", self.flashcard_dict),
            ("match_expression", self.match_expression_dict),
            ("match_translation", self.match_translation_dict),
            ("tf", self.tf_dict),
            ("pick", self.pick_dict),
            ("hangman", self.hangman_dict),
        ]
        available_dicts = [(name, dictionary) for name, dictionary in dict_choices if len(dictionary) > 0]

        if not available_dicts:
            return None, None

        chosen_entry = None
        for _ in range(consecutive_limit):
            chosen_entry = random.choice(available_dicts)
            if chosen_entry != getattr(self, f"last_chosen_{chosen_entry[0]}", None):
                break

        setattr(self, f"last_chosen_{chosen_entry[0]}", chosen_entry[0])

        return chosen_entry[1], chosen_entry[0]
        # debug -------------------------
        # dict = self.hangman_dict
        #
        # if len(dict) > 0:
        #     return self.match_translation_dict, "match_translation"
        # else:
        #     return None, None

    def get_random_key_value(self):
        if not self.chosen_dict:
            return None, None

        random_key = random.choice(list(self.chosen_dict.keys()))
        random_value = self.chosen_dict[random_key]
        return random_key, random_value

    def get_different_values(self, current_value, dict_to_choose_from, number_of_values=3):
        values_list = list(dict_to_choose_from.values())
        different_values = []

        while len(different_values) < number_of_values:
            random_value = random.choice(values_list)

            if random_value != current_value and random_value not in different_values:
                different_values.append(random_value)

        if len(different_values) < number_of_values:
            remaining_values = number_of_values - len(different_values)
            other_dicts = [d for d in [self.flashcard_dict, self.match_expression_dict, self.match_translation_dict,
                                       self.tf_dict, self.pick_dict, self.hangman_dict] if d != dict_to_choose_from]

            for other_dict in other_dicts:
                other_values = list(other_dict.values())
                for _ in range(remaining_values):
                    if other_values:
                        value = other_values.pop(random.randint(0, len(other_values) - 1))
                        different_values.append(value)

        return different_values

    def open_next_frame(self):
        if current_frame := self.frames.get(self.dict_name):
            current_frame.forget()

        self.chosen_dict, self.dict_name = self.random_dict()
        print("dict name: ", self.dict_name)

        key, value = self.get_random_key_value()

        wrong_answers = self.get_different_values(value, self.chosen_dict, 3)

        self.frames["flashcard"] = Flashcard(self, key, value)
        self.frames["match_expression"] = MatchExpression(self, key, value, wrong_answers)
        self.frames["match_translation"] = MatchTranslation(self, key, value, wrong_answers)
        self.frames["tf"] = TrueFalse(self, key, value)
        self.frames["pick"] = PickCorrect(self, key, value, wrong_answers)
        self.frames["hangman"] = Hangman(self, key, value)

        self.show_frame(self.dict_name)


# todo elementy UI klas tk.Frame
# todo do parametrów dodać jescze jeden, który jest arrayem zawierającym niepoprawne odpowiedzi

class Flashcard(tk.Frame):
    def __init__(self, parent, key, value):
        super().__init__(parent)
        self.key = key
        self.value = value
        self.configure(width=681, height=686)

        self.background_image = PhotoImage(file=
                                           "./components/graphical_components/flashcard/flashcard_panel.png")
        self.background = tk.Label(self, image=self.background_image)
        self.background.place(relwidth=1, relheight=1)
        self.pack()

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

        self.flip_button = tk.Button(self, image=self.flip_button_bg, command=self.test, bd=0, bg="#9ED2BE")
        self.flip_button.place(x=248, y=398)

        self.unknown_button = tk.Button(self, image=self.no_button_bg, command=lambda: self.test(),
                                        bd=0, bg="#9ED2BE")
        self.unknown_button.place(x=82, y=488)

        self.known_button = tk.Button(self, image=self.yes_button_bg, command=self.test, bd=0, bg="#9ED2BE")
        self.known_button.place(x=448, y=488)

        self.current_card = {}
        self.unknown = {}

        print(self.key, self.value)

    def test(self):
        pass


class MatchExpression(tk.Frame):
    def __init__(self, parent, key, value, list_of_wrong_answers):
        super().__init__(parent)
        self.key = key
        self.value = value
        self.wrong_answers = list_of_wrong_answers
        self.configure(width=681, height=686)

        self.background_image = PhotoImage(file="./components/graphical_components/games/match_expression/"
                                           "match_expression_bg.png")
        self.label_bg = PhotoImage(file="./components/graphical_components/games/pick_correct/label_bg.png")

        self.background = tk.Label(self, image=self.background_image)
        self.background.place(relwidth=1, relheight=1)

        self.canvas = tk.Canvas(self, width=616, height=357, bg="#9ed2be", highlightthickness=0)
        self.canvas_bg = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.label_bg)
        self.canvas.place(x=33, y=64)

        print("wrong answers: ", self.wrong_answers)

        self.word_to_display = tk.Label(
            self.canvas,
            text=key,
            font=('Inter', 60, 'bold'),
            background="#7eaa92",
            fg="#FFD9B7",
            wraplength=600
        )

        self.canvas.create_window(308, 178, window=self.word_to_display, anchor="center")

        self.answer_a = tk.Button(self, bd=0, bg="#7EAA92", fg="#FFFFFF", font=('Inter', 16, 'bold'), width=30)
        #self.answer_a.place(x=279, y=444)
        self.answer_b = tk.Button(self, bd=0, bg="#7EAA92", fg="#FFFFFF", font=('Inter', 16, 'bold'), width=30)
        #self.answer_b.place(x=279, y=515)
        self.answer_c = tk.Button(self, bd=0, bg="#7EAA92", fg="#FFFFFF", font=('Inter', 16, 'bold'), width=30)
        #self.answer_c.place(x=279, y=589)

        self.place_answers()
        self.pack()

    def place_answers(self):
        random_number = random.randint(0, 2)

        if random_number == 0:
            self.answer_a.configure(text=self.key)
            self.answer_b.configure(text=self.wrong_answers[0])
            self.answer_c.configure(text=self.wrong_answers[1])
        elif random_number == 1:
            self.answer_b.configure(text=self.key)
            self.answer_a.configure(text=self.wrong_answers[0])
            self.answer_c.configure(text=self.wrong_answers[1])
        elif random_number == 2:
            self.answer_c.configure(text=self.key)
            self.answer_a.configure(text=self.wrong_answers[0])
            self.answer_b.configure(text=self.wrong_answers[1])

        self.center_buttons_text_horizontally()

    def center_text_horizontally(self, button, y_pos):
        button.update_idletasks()  # Potrzebne do uzyskania dokładnych wymiarów przycisku po umieszczeniu na widżecie

        text_width = button.winfo_width()  # Szerokość przycisku
        button_width = button.winfo_reqwidth()  # Wymagana szerokość przycisku

        x_offset = (5 - text_width) / 2

        button.place(x=x_offset, y=y_pos, relx=0.5, anchor=tk.CENTER)

    def center_buttons_text_horizontally(self):
        self.center_text_horizontally(self.answer_a, 464)
        self.center_text_horizontally(self.answer_b, 535)
        self.center_text_horizontally(self.answer_c, 609)


class MatchTranslation(tk.Frame):
    def __init__(self, parent, key, value, list_of_wrong_answers):
        super().__init__(parent)
        self.key = key
        self.value = value
        self.value = value
        self.wrong_answers = list_of_wrong_answers
        self.configure(width=681, height=686)

        self.background_image = PhotoImage(file=
                                           "./components/graphical_components/games/match_translation/"
                                           "match_translation_bg.png")
        self.label_bg = PhotoImage(file="./components/graphical_components/games/pick_correct/label_bg.png")
        self.background = tk.Label(self, image=self.background_image)
        self.background.place(relwidth=1, relheight=1)

        self.canvas = tk.Canvas(self, width=616, height=357, bg="#9ed2be", highlightthickness=0)
        self.canvas_bg = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.label_bg)
        self.canvas.place(x=33, y=64)

        self.word_to_display = tk.Label(
            self.canvas,
            text=key,
            font=('Inter', 60, 'bold'),
            background="#7eaa92",
            fg="#FFD9B7",
            wraplength=600
        )

        self.canvas.create_window(308, 178, window=self.word_to_display, anchor="center")

        self.answer_a = tk.Button(self, bd=0, bg="#7EAA92", fg="#FFFFFF", font=('Inter', 20, 'bold'), width=14)
        self.answer_a.place(x=58, y=466)
        self.answer_b = tk.Button(self, bd=0, bg="#7EAA92", fg="#FFFFFF", font=('Inter', 20, 'bold'), width=14)
        self.answer_b.place(x=382, y=466)
        self.answer_c = tk.Button(self, bd=0, bg="#7EAA92", fg="#FFFFFF", font=('Inter', 20, 'bold'), width=14)
        self.answer_c.place(x=58, y=574)
        self.answer_d = tk.Button(self, bd=0, bg="#7EAA92", fg="#FFFFFF", font=('Inter', 20, 'bold'), width=14)
        self.answer_d.place(x=382, y=574)

        self.place_answers()
        self.pack()

    def place_answers(self):
        random_number = random.randint(0, 3)

        if random_number == 0:
            self.answer_a.configure(text=self.key, command=lambda: self.pick_answer(1))
            self.answer_b.configure(text=self.wrong_answers[0], command=lambda: self.pick_answer(0))
            self.answer_c.configure(text=self.wrong_answers[1], command=lambda: self.pick_answer(0))
            self.answer_d.configure(text=self.wrong_answers[2], command=lambda: self.pick_answer(0))
        elif random_number == 1:
            self.answer_b.configure(text=self.key, command=lambda: self.pick_answer(1))
            self.answer_a.configure(text=self.wrong_answers[0], command=lambda: self.pick_answer(0))
            self.answer_c.configure(text=self.wrong_answers[1], command=lambda: self.pick_answer(0))
            self.answer_d.configure(text=self.wrong_answers[2], command=lambda: self.pick_answer(0))
        elif random_number == 2:
            self.answer_c.configure(text=self.key, command=lambda: self.pick_answer(1))
            self.answer_a.configure(text=self.wrong_answers[0], command=lambda: self.pick_answer(0))
            self.answer_b.configure(text=self.wrong_answers[1], command=lambda: self.pick_answer(0))
            self.answer_d.configure(text=self.wrong_answers[2], command=lambda: self.pick_answer(0))
        elif random_number == 3:
            self.answer_d.configure(text=self.key, command=lambda: self.pick_answer(1))
            self.answer_a.configure(text=self.wrong_answers[0], command=lambda: self.pick_answer(0))
            self.answer_b.configure(text=self.wrong_answers[1], command=lambda: self.pick_answer(0))
            self.answer_c.configure(text=self.wrong_answers[2], command=lambda: self.pick_answer(0))

    def pick_answer(self, answer):
        # todo pass value to pointing system
        if answer == 1:
            print("yay 1 point")
        else:
            print("0 points :/")

        self.master.open_next_frame()


class TrueFalse(tk.Frame):
    def __init__(self, parent, key, value):
        super().__init__(parent)
        self.key = key
        self.value = value
        self.configure(width=681, height=686)

        self.background_image = PhotoImage(file=
                                           "./components/graphical_components/games/true_false/true_false_bg.png")
        self.no_button_bg = PhotoImage(file="./components/graphical_components/flashcard/no_button.png")
        self.yes_button_bg = PhotoImage(file="./components/graphical_components/flashcard/yes_button.png")
        self.label_bg = PhotoImage(file="./components/graphical_components/games/pick_correct/label_bg.png")
        self.background = tk.Label(self, image=self.background_image)
        self.background.place(relwidth=1, relheight=1)

        self.canvas = tk.Canvas(self, width=616, height=357, bg="#9ed2be", highlightthickness=0)
        self.canvas_bg = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.label_bg)
        self.canvas.place(x=33, y=67)

        self.word_to_display = tk.Label(
            self.canvas,
            text=key,
            font=('Inter', 60, 'bold'),
            background="#7eaa92",
            fg="#FFD9B7",
            wraplength=600
        )

        self.canvas.create_window(308, 178, window=self.word_to_display, anchor="center")

        self.false_button = tk.Button(self, image=self.no_button_bg, bd=0, bg="#9ed2be")
        self.false_button.place(x=87, y=488)

        self.true_button = tk.Button(self, image=self.yes_button_bg, bd=0, bg="#9ed2be")
        self.true_button.place(x=454, y=488)
        self.pack()


class PickCorrect(tk.Frame):
    def __init__(self, parent, key, value, list_of_wrong_answers):
        super().__init__(parent)
        self.key = key
        self.value = value
        self.wrong_answers = list_of_wrong_answers
        self.configure(width=681, height=686)

        self.background_image = PhotoImage(file=
                                           "./components/graphical_components/games/pick_correct/pick_correct_bg.png")
        self.button_bg = PhotoImage(file="./components/graphical_components/games/pick_correct/button.png")
        self.label_bg = PhotoImage(file="./components/graphical_components/games/pick_correct/label_bg.png")
        self.background = tk.Label(self, image=self.background_image)
        self.background.place(relwidth=1, relheight=1)

        self.canvas = tk.Canvas(self, width=616, height=357, bg="#9ed2be", highlightthickness=0)
        self.canvas_bg = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.label_bg)
        self.canvas.place(x=33, y=67)

        self.word_to_display = tk.Label(
            self.canvas,
            text=key,
            font=('Inter', 60, 'bold'),
            background="#7eaa92",
            fg="#FFD9B7",
            wraplength=600
        )

        self.canvas.create_window(308, 178, window=self.word_to_display, anchor="center")

        self.first_option = tk.Button(self, image=self.button_bg, bd=0, bg="#9ed2be")
        self.first_option.place(x=76, y=466)
        self.second_option = tk.Button(self, image=self.button_bg, bd=0, bg="#9ed2be")
        self.second_option.place(x=76, y=560)

        self.pack()


class Hangman(tk.Frame):
    def __init__(self, parent, key, value):
        super().__init__(parent)
        self.key = key
        self.value = value
        self.lives = 6
        self.is_game_over = False
        self.user_guesses = []
        self.configure(width=681, height=686)

        self.background_image = PhotoImage(file=
                                           "./components/graphical_components/games/hangman/hangman_bg.png")
        self.label_bg = PhotoImage(file="./components/graphical_components/games/hangman/canvas_bg.png")

        # hangman states
        self.hangman_none = PhotoImage(file="./components/graphical_components/games/hangman/none.png")
        self.hangman_head = PhotoImage(file="./components/graphical_components/games/hangman/head.png")
        self.hangman_body = PhotoImage(file="./components/graphical_components/games/hangman/body.png")
        self.hangman_hand = PhotoImage(file="./components/graphical_components/games/hangman/hand.png")
        self.hangman_hands = PhotoImage(file="./components/graphical_components/games/hangman/hands.png")
        self.hangman_leg = PhotoImage(file="./components/graphical_components/games/hangman/leg.png")
        self.hangman_whole = PhotoImage(file="./components/graphical_components/games/hangman/whole.png")

        self.background = tk.Label(self, image=self.background_image)
        self.background.place(relwidth=1, relheight=1)

        self.canvas = tk.Canvas(self, width=326, height=307, bg="#7EAA92", highlightthickness=0, bd=0)
        self.canvas_bg = self.canvas.create_image(0, 0, anchor=tk.W, image=self.label_bg)
        self.canvas.place(x=66, y=68)

        self.word_to_display = tk.Label(
            self.canvas,
            text=value,
            font=('Inter', 40, 'normal'),
            background="#7eaa92",
            fg="#FFD9B7",
            wraplength=600
        )

        self.canvas.create_window(163, 153, window=self.word_to_display, anchor="center")

        self.hangman_image = tk.Label(self, bd=2, bg="#7EAA92")
        self.hangman_image.place(x=382, y=68)

        self.word_length = len(key)
        self.display = []
        for _ in range(self.word_length):
            self.display += "_"

        self.dotted_txt = ' '.join(self.display)

        self.dotted_word = tk.Label(self, text=self.dotted_txt, bd=0, bg="#7EAA92", fg="#FFD9B7",
                                    font=('Inter', 30, 'normal'))
        dotted_word_width = self.dotted_word.winfo_reqwidth()

        element_x = 63
        element_width = 544
        dotted_word_x = element_x + (element_width - dotted_word_width) / 2

        self.dotted_word.place(x=dotted_word_x, y=591)

        self.create_letter_buttons()

        self.pack()

    def create_letter_buttons(self):
        y_pos = [394, 445, 495]
        buttons_x = [103, 151, 202, 250, 300, 350, 398, 451, 495, 546,
                     129, 177, 227, 277, 324, 374, 424, 472, 523,
                     179, 227, 276, 325, 374, 423, 471]

        letters = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z',
                   'X', 'C', 'V', 'B', 'N', 'M']

        button_index = 0
        button_counts = [10, 9, 7]

        for i in range(3):
            for _ in range(button_counts[i]):
                button = tk.Button(self, bd=0, bg="#C8E4B3", font=('Inter', 12, 'bold'), fg="#FFFFFF",
                                   text=letters[button_index], command=lambda char=letters[button_index].lower():
                                   self.button_press(char))
                button.place(x=buttons_x[button_index], y=y_pos[i])

                if button_index < len(letters):
                    button.configure(text=letters[button_index])
                    button_index += 1

    def button_press(self, char):
        self.user_guesses.append(char)
        self.check_letter(char)

    def check_letter(self, char):
        if char in self.key:
            for i, letter in enumerate(self.key):
                if letter == char:
                    self.display[i] = char
            self.update_display()
        else:
            self.lives -= 1
            self.switch(self.lives)
        self.check_game_over()

    def update_display(self):
        self.dotted_txt = ' '.join(self.display)
        self.dotted_word.config(text=self.dotted_txt)

    def check_game_over(self):
        if "_" not in self.display:
            # todo pass information to pointing system
            self.is_game_over = True
            self.master.open_next_frame()
        elif self.lives == 0:
            messagebox.showinfo("Wrong", "Unfortunately you didn't guess the word")
            self.is_game_over = True
            # todo pass information to pointing system
            self.master.open_next_frame()

    def switch(self, lives):
        hangman_images = {
            6: self.hangman_none,
            5: self.hangman_head,
            4: self.hangman_body,
            3: self.hangman_hand,
            2: self.hangman_hands,
            1: self.hangman_leg,
            0: self.hangman_whole
        }
        image_to_display = hangman_images.get(lives)

        if image_to_display is not None:
            self.hangman_image.configure(image=image_to_display)
        else:
            EOFError()

import tkinter as tk
from tkinter import PhotoImage
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ReportPanel(tk.Toplevel):
    def __init__(self, wrong_answers, session_len):
        super().__init__()
        self.wrong = wrong_answers
        self.session_len = session_len
        self.title("Session report")
        self.geometry('547x724')
        self.resizable(False, False)
        self.wm_attributes("-topmost", True)
        self.background_image = PhotoImage(file="./components/graphical_components/shared/report_panel.png")
        self.background = tk.Label(self, image=self.background_image)
        self.background.place(relwidth=1, relheight=1)

        self.close_button_bg = PhotoImage(file="./components/graphical_components/shared/close_button.png")

        self.close_button = tk.Button(self, image=self.close_button_bg, bd=0, bg="#9ED2BE", command=self.exit)
        self.close_button.place(x=168, y=663)

        print("wrong answers: ", self.wrong)
        print(f"you got {self.session_len - len(self.wrong)}/{self.session_len}")

        self.create_pie_chart(self.wrong, self.session_len)
        self.display_wrong_answers()

    def create_pie_chart(self, wrong_answers, session_len):
        """Create a pie chart.

            This method creates a pie chart to visualize the percentage of correct answers in the learning session.

            Args:
                self: The instance of the class.
                wrong_answers (list): A list of wrong answers.
                session_len (int): The length of the learning session.

            Returns:
                None.
            """
        correct_answers = session_len - len(wrong_answers)
        correct_percent = round((correct_answers / session_len) * 100)

        fig, ax = plt.subplots(figsize=(2.8, 2.8), facecolor="#9ed2be")
        ax.pie([correct_percent, 100 - correct_percent], colors=['#e38c0a', '#dd2e44'], startangle=140)
        ax.axis('equal')

        ax.text(0.5, 0.43, f'{correct_percent}%', fontsize=24, ha='center', va='center', transform=ax.transAxes,
                color='white')

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.place(x=90, y=76)

    def display_wrong_answers(self):
        """Display wrong answers.

            This method displays the wrong answers on the report panel.

            Args:
                self: The instance of the class.

            Returns:
                None.
            """
        panel_width = 360
        x_positions = []
        y_positions = [458, 505, 552, 599]

        for i, (answer, result) in enumerate(self.wrong.items()):
            if i >= 4:
                break
            combined_text = f'{answer} - {result}'
            if len(combined_text) <= 26:
                text_width = len(combined_text) * 12
                x_position = (panel_width - text_width) / 2
                x_positions.append(x_position)

                label = tk.Label(self, text=combined_text, font=("Inter", 24, "normal"), bg="#7eaa92", fg="white")
                label.place(x=x_position, y=y_positions[i])

    def exit(self):
        self.destroy()


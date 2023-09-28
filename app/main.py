import tkinter as tk
from tkinter import PhotoImage


class MainPanel:
    def __init__(self, root):
        self.panel = root
        self.panel.title("Main Panel")
        self.panel.geometry('961x698')
        self.panel.resizable(False, False)
        self.background_image = PhotoImage(file="./components/graphical_components/shared/background5.png")
        self.background = tk.Label(self.panel, image=self.background_image)
        self.background.place(relwidth=1, relheight=1)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainPanel(root)
    root.mainloop()



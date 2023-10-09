import tkinter as tk
from components.main_panel import MainPanel


def quit_app():
    root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainPanel(root)
    root.mainloop()

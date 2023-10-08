import tkinter as tk
from tkinter import PhotoImage
from .left_frame import LeftFrame
from .right_frame import RightFrame


class MainPanel:
    def __init__(self, root):
        self.panel = root
        self.panel.title("Learn-ey")
        self.panel.geometry('961x698')
        self.panel.resizable(False, False)
        self.background_image = PhotoImage(file="./components/graphical_components/shared/background.png")
        self.background = tk.Label(self.panel, image=self.background_image)
        self.background.place(relwidth=1, relheight=1)

        frame1 = LeftFrame(self.panel)
        frame2 = RightFrame(self.panel)


# class MainPanel:
#     def __init__(self, root):
#         self.panel = root
#         self.panel.title("Learn-ey")
#         self.panel.geometry('961x698')
#         self.panel.resizable(False, False)
#         self.background_image = PhotoImage(file="./components/graphical_components/shared/background.png")
#         self.background = tk.Label(self.panel, image=self.background_image)
#         self.background.place(relwidth=1, relheight=1)
#
#         self.background_image = PhotoImage(file="./graphical_components/main_panel/left_frame.png")  # Podaj ścieżkę do swojego obrazu
#         frame1 = tk.Label(root, image=self.background_image)
#         frame1.place(x=0, y=0,)

    #     # top panel
    #     panels_position_x = [255, 463, 47, 255, 463]
    #     panels_position_y = [47, 57, 217, 217, 217]
    #     self.new_session_button_bg = (
    #         PhotoImage(file="./components/graphical_components/main_panel/add_session_button.png"))
    #
    #     self.new_session_button = tk.Button(root, command=self.open_about, image=self.new_session_button_bg, bd=0,
    #                                         background='#a9d0bf')
    #     self.new_session_button.place(x=47, y=47)
    #     # buttons
    #     self.main_panel_bg = PhotoImage(file="./components/graphical_components/main_panel/main_panel_button.png")
    #     self.about_button_bg = PhotoImage(file="./components/graphical_components/main_panel/about_button.png")
    #     self.quit_button_bg = PhotoImage(file="./components/graphical_components/main_panel/quit_button.png")
    #     self.main_panel_button = tk.Button(root, command=self.open_main_panel, image=self.main_panel_bg,
    #                                        bd=0, background='#cde3b6')
    #     self.main_panel_button.place(x=735, y=475)
    #
    #     self.about_button = tk.Button(root, command=self.open_about, image=self.about_button_bg, bd=0,
    #                                   background='#cde3b6')
    #     self.about_button.place(x=735, y=542)
    #
    #     self.quit_button = tk.Button(root, command=self.quit_app, image=self.quit_button_bg, bd=0, background='#cde3b6')
    #     self.quit_button.place(x=735, y=606)
    #
    #
    # def populate_top_panel(self):
    #     pass
    #
    # def open_main_panel(self):
    #     print('Main Panel button has been pressed')
    #
    # def open_about(self):
    #     print('About button has been pressed')
    #
    # def quit_app(self):
    #     self.panel.destroy()

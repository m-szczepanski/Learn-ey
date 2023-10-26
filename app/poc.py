import tkinter
from tkinter import filedialog



def set_path():
    path = filedialog.askopenfilename()
    print(path)




root = tkinter.Tk()
root.geometry("600x600")


btn_get_path = tkinter.Button(root, text="Chose file", command=set_path)
btn_get_path.pack()

root.mainloop()
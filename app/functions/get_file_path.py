from tkinter import filedialog


def get_file_path():
    """Get the file path.

       This function opens a file dialog to allow the user to select a file and returns the selected file path.

       Returns:
           str: The selected file path.
       """
    return filedialog.askopenfilename()

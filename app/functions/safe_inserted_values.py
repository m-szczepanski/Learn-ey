import json
from tkinter import messagebox


def safe_session_data(data1, data2, session_name):
    """Safely save session data.

        This function safely saves the session data by writing it to a JSON file.

        Args:
            data1 (list): The first list of data.
            data2 (list): The second list of data.
            session_name (str): The name of the session.

        Raises:
            ValueError: If the number of elements in data1 and data2 is different.
        """
    if len(data1) != len(data2):
        raise ValueError("A difference in the number of elements to be written was encountered")

    data = dict(zip(data1, data2))
    with open(f"./data/session_data/{session_name}.json", 'w') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    messagebox.showinfo("Session saved", f"{session_name[:-5]} has been saved as a session.")

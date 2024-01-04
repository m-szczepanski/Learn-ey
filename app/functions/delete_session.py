import os


def delete_session(session_name):
    """Delete a session file.

       This function deletes the specified session file.

       Args:
           session_name (str): The name of the session file to delete.
       """
    directory_path = "./data/session_data"
    try:
        file_path = os.path.join(directory_path, session_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File {session_name} has been deleted.")
        else:
            print(f"File {session_name} does not exists in {directory_path}.")
    except Exception as e:
        print(f"Error: {str(e)}")

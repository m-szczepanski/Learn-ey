import os


def list_files_in_directory():
    files = os.listdir("./data/session_data")
    max_files = 5

    return files[:max_files]

import os


def list_files_in_directory(path, max_number):
    files = os.listdir(path)
    max_files = max_number

    return files[:max_files]

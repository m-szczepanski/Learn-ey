import os


def list_files_in_directory(path, max_number):
    """List files in a directory.

       This function lists the files in the specified directory up to the maximum number.

       Args:
           path (str): The path of the directory.
           max_number (int): The maximum number of files to list.

       Returns:
           list: A list of files in the directory.
       """
    files = os.listdir(path)
    max_files = max_number

    return files[:max_files]

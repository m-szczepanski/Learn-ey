import os
from datetime import datetime


def get_file_creation_time(file_name):
    try:
        directory_path = "./data/session_data"
        directory = os.listdir(directory_path)
        for filename in directory:
            if filename == file_name:
                file_path = os.path.join(directory_path, filename)
                if os.path.exists(file_path):
                    if os.name == 'nt':  # Windows
                        creation_time = os.path.getctime(file_path)
                    else:  # Unix/Linux/Mac
                        creation_time = os.path.getmtime(file_path)

                    # Format the date
                    formatted_creation_time = datetime.fromtimestamp(creation_time).strftime('%d-%m-%Y')
                    return formatted_creation_time

        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None


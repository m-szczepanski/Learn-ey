import json


def fetch_json_data(file_path):
    """Fetch data from a JSON file.

       This function fetches data from a JSON file and returns the keys and values as separate lists.

       Args:
           file_path (str): The path of the JSON file.

       Returns:
           tuple: A tuple containing the keys and values as separate lists.

       Raises:
           FileNotFoundError: If the specified file path does not exist.
           json.JSONDecodeError: If there is an error decoding the JSON file.
       """
    keys = []
    values = []

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            for key, value in data.items():
                keys.append(key)
                values.append(value)

        return keys, values
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file: {file_path}")

    return None, None
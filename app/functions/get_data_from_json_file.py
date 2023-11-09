import json


def fetch_json_data(file_path):
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
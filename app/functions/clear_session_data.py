import json


def clear_json_file(file_path):
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

        # Usunięcie wartości kluczy "type" i "path"
        if 'type' in data:
            del data['type']
        if 'path' in data:
            del data['path']

        # Zapisanie zaktualizowanych danych z powrotem do pliku
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        return True
    except FileNotFoundError:
        return False



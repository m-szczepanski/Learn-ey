import json


def pass_session_data(session_type, file_path):
    file_name = str(file_path).lower()
    real_path = f"./data/words/{file_name}.csv"
    data = {
        'type': session_type,
        'path': real_path
    }

    with open('./data/temporary_data/session.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

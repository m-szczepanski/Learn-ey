import json


def safe_session_data(words, translations, session_name):
    if len(words) != len(translations):
        raise ValueError("A difference in the number of elements to be written was encountered")

    directory_path = "../data/session_data"
    file_path = f"{directory_path}/{session_name}.json"
    data = dict(zip(words, translations))
    with open(f"./data/session_data/{session_name}.json", 'w') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


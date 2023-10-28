import json


def safe_session_data(data1, data2, session_name):
    if len(data1) != len(data2):
        raise ValueError("A difference in the number of elements to be written was encountered")

    data = dict(zip(data1, data2))
    with open(f"./data/session_data/{session_name}.json", 'w') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

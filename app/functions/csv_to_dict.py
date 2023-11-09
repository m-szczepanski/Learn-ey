import pandas as pd


def read_csv_to_dict(file_path, language):
    try:
        data = pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")

    records = data.to_dict(orient="records")
    dictionary = {record[str(language)]: record['English'] for record in records}
    return dictionary

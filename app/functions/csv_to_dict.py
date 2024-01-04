import pandas as pd


def read_csv_to_dict(file_path, language):
    """Read a CSV file and convert it to a dictionary.

        This function reads a CSV file and converts it to a dictionary using the specified language column as the key
        and the English column as the value.

        Args:
            file_path (str): The path of the CSV file.
            language (str): The language column to use as the key in the dictionary.

        Returns:
            dict: A dictionary with the language column as the key and the English column as the value.

        Raises:
            FileNotFoundError: If the specified file path does not exist.
        """
    try:
        data = pd.read_csv(file_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_path}") from e

    records = data.to_dict(orient="records")
    dictionary = {record[str(language)]: record['English'] for record in records}
    return dictionary

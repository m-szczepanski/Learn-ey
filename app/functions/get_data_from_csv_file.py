import pandas as pd


def fetch_csv_data(file_path):
    """Fetch data from a CSV file.

       This function fetches data from a CSV file and returns the keys and values as separate lists.

       Args:
           file_path (str): The path of the CSV file.

       Returns:
           tuple: A tuple containing the keys and values as separate lists.

       Raises:
           pd.errors.EmptyDataError: If the CSV file is empty.
           FileNotFoundError: If the specified file path does not exist.
           Exception: If there is an error reading the CSV file.
       """
    keys = []
    values = []

    try:
        df = pd.read_csv(file_path, encoding='utf-8', header=None)

        if len(df.columns) >= 2:
            keys = df.iloc[:, 0].tolist()
            values = df.iloc[:, 1].tolist()
        else:
            print("Error: CSV file is not suited for Learne'y to open.")

    except pd.errors.EmptyDataError:
        print("Error: File is empty")
    except FileNotFoundError:
        print("Error: File does not exist")
    except Exception as e:
        print(f"Error: {str(e)}")

    return keys, values

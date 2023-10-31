import pandas as pd


def fetch_csv_data(file_path):
    words = []
    translations = []

    try:
        df = pd.read_csv(file_path, encoding='utf-8', header=None)

        if len(df.columns) >= 2:
            words = df.iloc[:, 0].tolist()
            translations = df.iloc[:, 1].tolist()
        else:
            print("Error: CSV file is not suited for Learne'y to open.")

    except pd.errors.EmptyDataError:
        print("Error: File is empty")
    except FileNotFoundError:
        print("Error: File does not exist")
    except Exception as e:
        print(f"Error: {str(e)}")

    return words, translations

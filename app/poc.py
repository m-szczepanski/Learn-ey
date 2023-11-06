






def funkcja():
    # Ścieżka do pliku CSV
    file_path = "./data/temporary_data/check_language.csv"

    try:
        with open(file_path, mode='r', newline='') as file:
            csv_reader = csv.reader(file)
            first_row = next(csv_reader)  # Odczytaj pierwszą linię

            # Wyświetl pierwszą linię
            print(first_row)

    except FileNotFoundError:
        print(f"Plik '{file_path}' nie został znaleziony.")
    except Exception as e:
        print(f"Wystąpił błąd: {str(e)}")
    return first_row[0]
#
#
# x = funkcja()
# print(x)
import json


def distribute_data_json(file_name):
    """Distribute data from a JSON file into different dictionaries.

       This function distributes the data from a JSON file into different dictionaries based on the length of the key
       and value.

       Args:
           file_name (str): The name of the JSON file.

       Returns:
           tuple: A tuple containing the distributed data dictionaries for flashcards, match expressions, match
           translations, true/false questions, pick questions, and hangman questions.

       Raises:
           FileNotFoundError: If the specified file name does not exist.
       """
    try:
        with open(f"./data/session_data/{file_name}.json", 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {file_name}") from e

    flashcard_dict = {}
    match_expression_dict = {}
    match_translation_dict = {}
    tf_dict = {}
    pick_dict = {}
    hangman_dict = {}

    dicts = [flashcard_dict, match_expression_dict, match_translation_dict, tf_dict, pick_dict, hangman_dict]

    for key, value in data.items():
        dict_lengths = [len(d) for d in dicts]

        # Check if the key and value lengths meet the requirements for each dictionary
        conditions = [
            (len(key) < 70 and len(value) < 31),  # hangman_dict
            (len(key) < 10 and len(value) < 19),  # pick_dict
            (len(key) < 19 and len(value) < 19),  # tf_dict
            (len(key) < 11 and len(value) < 11),  # match_translation_dict
            (len(key) < 16),  # match_expression_dict
            (len(key) < 13 and len(value) < 13)  # flashcard_dict
        ]

        for i, condition in enumerate(conditions):
            if condition and len(dicts[i]) == min(dict_lengths):
                dicts[i][key] = value
                break

    return flashcard_dict, match_expression_dict, match_translation_dict, tf_dict, pick_dict, hangman_dict

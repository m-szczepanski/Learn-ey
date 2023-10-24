from app.functions.safe_inserted_values import safe_session_data


def save_data(words, translations, session_name):
    safe_session_data(words, translations, session_name)
    translations.clear()
    words.clear()

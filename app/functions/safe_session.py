from app.functions.safe_inserted_values import safe_session_data


def save_data(array1, array2, session_name):
    safe_session_data(array1, array2, session_name)
    array2.clear()
    array1.clear()

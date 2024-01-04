from app.functions.safe_inserted_values import safe_session_data


def save_data(array1, array2, session_name):
    """Save session data.

        This function saves the session data by calling the `safe_session_data` function and clearing the arrays.

        Args:
            array1 (list): The first array of data.
            array2 (list): The second array of data.
            session_name (str): The name of the session.
        """
    safe_session_data(array1, array2, session_name)
    array2.clear()
    array1.clear()

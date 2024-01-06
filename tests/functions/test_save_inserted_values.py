import pytest
import json
import os
from unittest.mock import patch
from app.functions.save_inserted_values import save_session_data

# Constants for test paths and file names
TEST_SESSION_PATH = "./data/session_data/"
TEST_SESSION_PREFIX = "test_session_"

# Ensure the directory for session data exists before running tests
os.makedirs(TEST_SESSION_PATH, exist_ok=True)

# Helper function to read a session file
def read_session_file(session_name):
    with open(f"{TEST_SESSION_PATH}{session_name}.json", 'r') as json_file:
        return json.load(json_file)

# Parametrized test for happy path scenarios
@pytest.mark.parametrize("data1, data2, session_name, test_id", [
    (['key1', 'key2'], ['value1', 'value2'], TEST_SESSION_PREFIX + "happy", 'happy_path_1'),
    (['user', 'password'], ['admin', '1234'], TEST_SESSION_PREFIX + "credentials", 'happy_path_2'),
    ([], [], TEST_SESSION_PREFIX + "empty", 'happy_path_3')
])
def test_safe_session_data_happy_path(data1, data2, session_name, test_id):
    # Arrange
    expected_data = dict(zip(data1, data2))
    session_file_path = f"{TEST_SESSION_PATH}{session_name}.json"

    # Act
    with patch('tkinter.messagebox.showinfo') as mock_messagebox:
        save_session_data(data1, data2, session_name)

    # Assert
    assert os.path.exists(session_file_path)
    assert read_session_file(session_name) == expected_data
    mock_messagebox.assert_called_once()
    os.remove(session_file_path)  # Cleanup

# Parametrized test for edge cases
@pytest.mark.parametrize("data1, data2, session_name, test_id", [
    (['key1'], ['value1'], TEST_SESSION_PREFIX + "single", 'edge_case_1'),
    (['key'*100], ['value'*100], TEST_SESSION_PREFIX + "long_key_value", 'edge_case_2')
])
def test_safe_session_data_edge_cases(data1, data2, session_name, test_id):
    # Arrange
    expected_data = dict(zip(data1, data2))
    session_file_path = f"{TEST_SESSION_PATH}{session_name}.json"

    # Act
    with patch('tkinter.messagebox.showinfo') as mock_messagebox:
        save_session_data(data1, data2, session_name)

    # Assert
    assert os.path.exists(session_file_path)
    assert read_session_file(session_name) == expected_data
    mock_messagebox.assert_called_once()
    os.remove(session_file_path)  # Cleanup

# Parametrized test for error cases
@pytest.mark.parametrize("data1, data2, session_name, expected_exception, test_id", [
    (['key1'], ['value1', 'value2'], TEST_SESSION_PREFIX + "mismatch", ValueError, 'error_case_1'),
    (['key1', 'key2'], ['value1'], TEST_SESSION_PREFIX + "mismatch_reverse", ValueError, 'error_case_2')
])
def test_safe_session_data_error_cases(data1, data2, session_name, expected_exception, test_id):
    # Act / Assert
    with pytest.raises(expected_exception):
        save_session_data(data1, data2, session_name)

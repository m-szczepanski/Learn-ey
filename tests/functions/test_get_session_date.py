import pytest
import os
from datetime import datetime
from app.functions.get_session_date import get_file_creation_time

# Constants for test
DIRECTORY_PATH = "./data/session_data"
TEST_FILE_NAME = "test_file.txt"
TEST_FILE_PATH = os.path.join(DIRECTORY_PATH, TEST_FILE_NAME)


# Helper functions for setting up the test environment
def setup_file_in_directory(file_name, timestamp=None):
    os.makedirs(DIRECTORY_PATH, exist_ok=True)
    file_path = os.path.join(DIRECTORY_PATH, file_name)
    with open(file_path, 'w') as f:
        f.write("Test content")
    if timestamp:
        os.utime(file_path, (timestamp, timestamp))


def remove_test_directory():
    if os.path.exists(DIRECTORY_PATH):
        for file in os.listdir(DIRECTORY_PATH):
            os.remove(os.path.join(DIRECTORY_PATH, file))
        os.rmdir(DIRECTORY_PATH)


@pytest.fixture
def clean_directory():
    remove_test_directory()
    yield
    remove_test_directory()


# Parametrized test cases
@pytest.mark.parametrize("file_name, timestamp, expected_date, test_id", [
    # Happy path tests with various realistic test values
    ("existing_file.txt", 1610000000, "07-01-2021", "happy_path_unix"),
    ("existing_file.txt", 1610000000, "06-01-2024", "happy_path_windows"),

    # Edge cases
    ("", 1610000000, None, "edge_case_empty_filename"),
    ("non_existing_file.txt", 1610000000, None, "edge_case_non_existing_file"),

    # Error cases
    (None, 1610000000, None, "error_case_none_filename"),
    # todo fix this bug
    #(str(123), 1610000000, None, "error_case_non_string_filename"),
])
def test_get_file_creation_time(file_name, timestamp, expected_date, test_id, clean_directory, monkeypatch):
    # Arrange
    if file_name is not None and not isinstance(file_name, str):
        file_name = str(file_name)  # Convert non-string filenames to string to simulate user error
    if file_name and file_name != "non_existing_file.txt":
        setup_file_in_directory(file_name, timestamp)
    if test_id == "happy_path_windows":
        monkeypatch.setattr(os, 'name', 'nt')
    else:
        monkeypatch.setattr(os, 'name', 'posix')

    # Act
    result = get_file_creation_time(file_name)

    # Assert
    assert result == expected_date, f"Test failed for test_id: {test_id}"

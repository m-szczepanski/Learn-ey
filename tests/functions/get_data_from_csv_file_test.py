import pytest
import pandas as pd
from app.functions.get_data_from_csv_file import fetch_csv_data
from unittest.mock import mock_open, patch


# todo fix errors
# Constants for test cases
VALID_CSV_CONTENT = "key,value\na,1\nb,2\nc,3"
SINGLE_COLUMN_CSV_CONTENT = "key\na\nb\nc"
EMPTY_CSV_CONTENT = ""
NON_EXISTENT_FILE_PATH = "c:/non_existent_file.csv"
INVALID_CSV_PATH = "c:/invalid_file.csv"

# Helper function to simulate file reading
def mock_file_open(mock, content):
    m = mock_open(read_data=content)
    mock.side_effect = [m.return_value]

# Happy path tests with various realistic test values
@pytest.mark.parametrize("file_path, file_content, expected_keys, expected_values, test_id", [
    ("c:/valid_file.csv", VALID_CSV_CONTENT, ['a', 'b', 'c'], ['1', '2', '3'], "happy_path_valid_csv"),
    # Add more test cases for different valid CSV contents
])
def test_fetch_csv_data_happy_path(file_path, file_content, expected_keys, expected_values, test_id):
    with patch("builtins.open") as mock:
        mock_file_open(mock, file_content)

        # Act
        keys, values = fetch_csv_data(file_path)

        # Assert
        assert keys[1:] == expected_keys, f"Test {test_id} failed: keys don't match"
        assert values[1:] == expected_values, f"Test {test_id} failed: values don't match"


# Edge cases
@pytest.mark.parametrize("file_path, file_content, expected_keys, expected_values, test_id", [
    ("c:/single_column_file.csv", SINGLE_COLUMN_CSV_CONTENT, [], [], "edge_case_single_column"),
    # Add more test cases for different edge cases
])
def test_fetch_csv_data_edge_cases(file_path, file_content, expected_keys, expected_values, test_id):
    with patch("builtins.open") as mock:
        mock_file_open(mock, file_content)

        # Act
        keys, values = fetch_csv_data(file_path)

        # Assert
        assert keys == expected_keys, f"Test {test_id} failed: keys don't match"
        assert values == expected_values, f"Test {test_id} failed: values don't match"

# Error cases
@pytest.mark.parametrize("file_path, file_content, exception, test_id", [
    (NON_EXISTENT_FILE_PATH, None, FileNotFoundError, "error_case_file_not_found"),
    ("c:/empty_file.csv", EMPTY_CSV_CONTENT, pd.errors.EmptyDataError, "error_case_empty_file"),
    # Add more test cases for different exceptions and error messages
])
def test_fetch_csv_data_error_cases(file_path, file_content, exception, test_id, capsys):
    if file_content is not None:
        with patch("builtins.open") as mock:
            mock_file_open(mock, file_content)

    # Act and Assert
    with pytest.raises(exception):
        fetch_csv_data(file_path)

    captured = capsys.readouterr()
    assert "Error:" in captured.out, f"Test {test_id} failed: Error message not printed"

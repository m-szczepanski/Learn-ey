import pytest
import pandas as pd
from app.functions.get_data_from_csv_file import fetch_csv_data
import os

# Constants for test file paths
TEST_DATA_DIR = "tests/test_data/"
VALID_CSV = TEST_DATA_DIR + "valid.csv"
SINGLE_COLUMN_CSV = TEST_DATA_DIR + "single_column.csv"
EMPTY_CSV = TEST_DATA_DIR + "empty.csv"
NON_EXISTENT_CSV = TEST_DATA_DIR + "non_existent.csv"

# Prepare test data files
@pytest.fixture(scope="module", autouse=True)
def setup_test_files():
    # Arrange
    os.makedirs(TEST_DATA_DIR, exist_ok=True)
    # Valid CSV content
    pd.DataFrame({'key': ['key1', 'key2'], 'value': ['value1', 'value2']}).to_csv(VALID_CSV, index=False, header=False)
    # Single column CSV content
    pd.DataFrame({'key': ['key1', 'key2']}).to_csv(SINGLE_COLUMN_CSV, index=False, header=False)
    # Empty CSV content
    pd.DataFrame().to_csv(EMPTY_CSV, index=False, header=False)
    yield
    # Teardown
    os.remove(VALID_CSV)
    os.remove(SINGLE_COLUMN_CSV)
    os.remove(EMPTY_CSV)

# Happy path tests with various realistic test values
@pytest.mark.parametrize("file_path, expected_keys, expected_values, test_id", [
    (VALID_CSV, ['key1', 'key2'], ['value1', 'value2'], 'happy_path_valid_csv'),
])
def test_fetch_csv_data_happy_path(file_path, expected_keys, expected_values, test_id):
    # Act
    keys, values = fetch_csv_data(file_path)

    # Assert
    assert keys == expected_keys, f"Test {test_id} failed: keys mismatch"
    assert values == expected_values, f"Test {test_id} failed: values mismatch"

# Edge case: CSV with only one column
@pytest.mark.parametrize("file_path, expected_output, test_id", [
    (SINGLE_COLUMN_CSV, ([], []), 'edge_case_single_column'),
])
def test_fetch_csv_data_edge_case(file_path, expected_output, test_id, capsys):
    # Act
    keys, values = fetch_csv_data(file_path)
    captured = capsys.readouterr()  # Capture the print output

    # Assert
    assert (keys, values) == expected_output, f"Test {test_id} failed: output mismatch"
    assert "Error: CSV file is not suited for Learne'y to open." in captured.out, f"Test {test_id} failed: error message not printed"

# Error case: Empty CSV file
@pytest.mark.parametrize("file_path, test_id", [
    (EMPTY_CSV, 'error_case_empty_csv'),
])
def test_fetch_csv_data_error_empty_file(file_path, test_id, capsys):
    # Act
    keys, values = fetch_csv_data(file_path)
    captured = capsys.readouterr()  # Capture the print output

    # Assert
    assert keys == [] and values == [], f"Test {test_id} failed: output not empty"
    assert "Error: File is empty" in captured.out, f"Test {test_id} failed: error message not printed"

# Error case: File does not exist
@pytest.mark.parametrize("file_path, test_id", [
    (NON_EXISTENT_CSV, 'error_case_non_existent_file'),
])
def test_fetch_csv_data_error_file_not_found(file_path, test_id, capsys):
    # Act
    keys, values = fetch_csv_data(file_path)
    captured = capsys.readouterr()  # Capture the print output

    # Assert
    assert keys == [] and values == [], f"Test {test_id} failed: output not empty"
    assert "Error: File does not exist" in captured.out, f"Test {test_id} failed: error message not printed"

# Error case: General exception handling
@pytest.mark.parametrize("file_path, test_id", [
    (VALID_CSV, 'error_case_general_exception'),
])
def test_fetch_csv_data_error_general_exception(file_path, test_id, monkeypatch, capsys):
    # Arrange
    def mock_read_csv(*args, **kwargs):
        raise Exception("Unexpected error")
    monkeypatch.setattr(pd, 'read_csv', mock_read_csv)

    # Act
    keys, values = fetch_csv_data(file_path)
    captured = capsys.readouterr()  # Capture the print output

    # Assert
    assert keys == [] and values == [], f"Test {test_id} failed: output not empty"
    assert "Error: Unexpected error" in captured.out, f"Test {test_id} failed: error message not printed"

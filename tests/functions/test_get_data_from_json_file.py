import pytest
import json
import os
from app.functions.get_data_from_json_file import fetch_json_data

# Constants for test file paths
TEST_DATA_DIR = "test_data"
VALID_JSON_FILE = os.path.join(TEST_DATA_DIR, "valid.json")
EMPTY_JSON_FILE = os.path.join(TEST_DATA_DIR, "empty.json")
INVALID_JSON_FILE = os.path.join(TEST_DATA_DIR, "invalid.json")
NON_EXISTENT_FILE = os.path.join(TEST_DATA_DIR, "nonexistent.json")

# Prepare test data
@pytest.fixture(scope="module", autouse=True)
def setup_test_files():
    os.makedirs(TEST_DATA_DIR, exist_ok=True)
    with open(VALID_JSON_FILE, 'w') as file:
        json.dump({"key1": "value1", "key2": "value2"}, file)
    with open(EMPTY_JSON_FILE, 'w') as file:
        file.write("{}")
    with open(INVALID_JSON_FILE, 'w') as file:
        file.write("{invalid_json}")

@pytest.mark.parametrize("file_path, expected_keys, expected_values, test_id", [
    (VALID_JSON_FILE, ["key1", "key2"], ["value1", "value2"], "happy_path_valid_json"),
    (EMPTY_JSON_FILE, [], [], "happy_path_empty_json"),
    (NON_EXISTENT_FILE, None, None, "error_case_nonexistent_file"),
    (INVALID_JSON_FILE, None, None, "error_case_invalid_json"),
])
def test_fetch_json_data(file_path, expected_keys, expected_values, test_id):
    # Arrange
    # (No arrange step needed as input values are provided via test parameters)

    # Act
    actual_keys, actual_values = fetch_json_data(file_path)

    # Assert
    if expected_keys is not None and expected_values is not None:
        assert actual_keys == expected_keys, f"Test Failed: {test_id} - Keys do not match"
        assert actual_values == expected_values, f"Test Failed: {test_id} - Values do not match"
    else:
        assert actual_keys is None and actual_values is None, f"Test Failed: {test_id} - Function should return None, None"

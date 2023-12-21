import pytest
import json
from app.functions.distribute_session_data import distribute_data_json
from unittest.mock import mock_open, patch

# Define the path where the function expects the JSON files
DATA_PATH = "./data/session_data/"

# Test IDs for different scenarios
HAPPY_PATH_ID = "happy_path"
EDGE_CASE_ID = "edge_case"
ERROR_CASE_ID = "error_case"

# Test data for happy path scenarios
happy_path_data = [
    (HAPPY_PATH_ID + "_balanced", "balanced", {
        "short1": "short1", "short2": "short2", "short3": "short3",
        "medium1": "medium1", "medium2": "medium2",
        "long1": "long1", "long2": "long2"
    }),
    # Add more test cases with different lengths and combinations
]

# Test data for edge cases
edge_case_data = [
    (EDGE_CASE_ID + "_empty", "empty", {}),
    # Add more edge cases like maximum length strings, special characters, etc.
]

# Test data for error cases
error_case_data = [
    (ERROR_CASE_ID + "_file_not_found", "nonexistent", FileNotFoundError),
    # Add more error cases if necessary
]


@pytest.mark.parametrize("test_id, file_name, expected_data", happy_path_data)
def test_distribute_data_json_happy_path(test_id, file_name, expected_data):
    # Arrange
    mock_data = json.dumps(expected_data)
    with patch("builtins.open", mock_open(read_data=mock_data)) as mock_file:
        # Act
        result = distribute_data_json(file_name)

        # Assert
        assert mock_file.call_args[0][0] == DATA_PATH + file_name + ".json"
        assert all(isinstance(d, dict) for d in result)
        # Add more assertions to check if the data is distributed correctly


@pytest.mark.parametrize("test_id, file_name, expected_data", edge_case_data)
def test_distribute_data_json_edge_cases(test_id, file_name, expected_data):
    # Arrange
    mock_data = json.dumps(expected_data)
    with patch("builtins.open", mock_open(read_data=mock_data)):
        # Act
        result = distribute_data_json(file_name)

        # Assert
        # Assertions will depend on the edge case being tested


@pytest.mark.parametrize("test_id, file_name, expected_exception", error_case_data)
def test_distribute_data_json_error_cases(test_id, file_name, expected_exception):
    # Arrange
    with patch("builtins.open", side_effect=expected_exception):
        # Act & Assert
        with pytest.raises(expected_exception):
            distribute_data_json(file_name)

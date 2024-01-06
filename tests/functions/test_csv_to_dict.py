import pytest
import pandas as pd
from app.functions.csv_to_dict import read_csv_to_dict
from unittest.mock import mock_open, patch

# Constants for test cases
VALID_FILE_PATH = "valid_file.csv"
INVALID_FILE_PATH = "invalid_file.csv"
LANGUAGE = "Spanish"
NON_EXISTENT_LANGUAGE = "Klingon"
TEST_DATA = pd.DataFrame({
    'English': ['Hello', 'World'],
    'Spanish': ['Hola', 'Mundo']
})
TEST_DATA_NON_EXISTENT_LANGUAGE = pd.DataFrame({
    'English': ['Hello', 'World']
})

# Helper function to simulate reading CSV
def mock_read_csv(file_path):
    if file_path == VALID_FILE_PATH:
        return TEST_DATA
    elif file_path == INVALID_FILE_PATH:
        raise FileNotFoundError

# Parametrized test cases
@pytest.mark.parametrize("file_path, language, expected", [
    # ID: HappyPath-ValidInputs
    (VALID_FILE_PATH, LANGUAGE, {'Hola': 'Hello', 'Mundo': 'World'}),
    # ID: EdgeCase-EmptyCSV
    (VALID_FILE_PATH, LANGUAGE, {'Hola': 'Hello', 'Mundo': 'World'}),
    # ID: ErrorCase-FileNotFound
    (INVALID_FILE_PATH, LANGUAGE, FileNotFoundError),
    # ID: ErrorCase-NonExistentLanguage
    (VALID_FILE_PATH, NON_EXISTENT_LANGUAGE, KeyError),
])
def test_read_csv_to_dict(file_path, language, expected):
    # Arrange
    with patch('pandas.read_csv', side_effect=mock_read_csv):
        if expected is FileNotFoundError:
            with pytest.raises(FileNotFoundError) as excinfo:
                # Act
                read_csv_to_dict(file_path, language)
            # Assert
            assert str(excinfo.value) == f"File not found: {file_path}"
        elif expected is KeyError:
            with pytest.raises(KeyError):
                # Act
                read_csv_to_dict(file_path, language)
        else:
            # Act
            result = read_csv_to_dict(file_path, language)
            # Assert
            if isinstance(expected, dict):
                assert result == expected, f"Expected {expected}, got {result}"
            else:
                assert result == {}, f"Expected empty dict, got {result}"

# Additional test to cover the empty CSV edge case
def test_read_csv_to_dict_empty_csv():
    # Arrange
    empty_data = pd.DataFrame()
    with patch('pandas.read_csv', return_value=empty_data):
        # Act
        result = read_csv_to_dict(VALID_FILE_PATH, LANGUAGE)
        # Assert
        assert result == {}

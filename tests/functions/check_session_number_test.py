import pytest
import os
from app.functions.check_session_number import list_files_in_directory

# Directory for test files
TEST_DIR = "test_dir"

# Setup and teardown for creating a test directory with test files
@pytest.fixture(scope="module", autouse=True)
def setup_teardown():
    # Arrange: Create a directory with test files
    if not os.path.exists(TEST_DIR):
        os.makedirs(TEST_DIR)
    for i in range(10):
        with open(os.path.join(TEST_DIR, f"test_file_{i}.txt"), "w") as f:
            f.write(f"Content of file {i}")

    yield  # This separates setup from teardown

    # Teardown: Remove the directory with test files
    for i in range(10):
        os.remove(os.path.join(TEST_DIR, f"test_file_{i}.txt"))
    os.rmdir(TEST_DIR)

# Happy path tests with various realistic test values
@pytest.mark.parametrize("path, max_number, expected", [
    (TEST_DIR, 5, [f"test_file_{i}.txt" for i in range(5)]),  # ID: HappyPath-PartialList
    (TEST_DIR, 10, [f"test_file_{i}.txt" for i in range(10)]),  # ID: HappyPath-FullList
    (TEST_DIR, 15, [f"test_file_{i}.txt" for i in range(10)]),  # ID: HappyPath-MoreThanExists
], ids=["HappyPath-PartialList", "HappyPath-FullList", "HappyPath-MoreThanExists"])
def test_list_files_in_directory_happy_path(path, max_number, expected):
    # Act
    result = list_files_in_directory(path, max_number)

    # Assert
    assert result == expected, f"Expected {expected}, got {result}"

# Edge cases
# @pytest.mark.parametrize("path, max_number, expected", [
#     (TEST_DIR, 0, []),  # ID: EdgeCase-NoFilesRequested
#     (TEST_DIR, -1, []),  # ID: EdgeCase-NegativeNumber
# ], ids=["EdgeCase-NoFilesRequested", "EdgeCase-NegativeNumber"])
# def test_list_files_in_directory_edge_cases(path, max_number, expected):
#     # Act
#     result = list_files_in_directory(path, max_number)
#
#     # Assert
#     assert result == expected, f"Expected {expected}, got {result}"


# Error cases
@pytest.mark.parametrize("path, max_number, exception", [
    ("non_existent_dir", 5, FileNotFoundError),  # ID: ErrorCase-NonExistentDirectory
    (123, 5, TypeError),  # ID: ErrorCase-InvalidPathType
], ids=["ErrorCase-NonExistentDirectory", "ErrorCase-InvalidPathType"])
def test_list_files_in_directory_error_cases(path, max_number, exception):
    # Act / Assert
    with pytest.raises(exception):
        list_files_in_directory(path, max_number)

import os
import pytest
from app.functions.delete_session import delete_session

# todo repair 4 tests
# Directory where session files are stored
SESSION_DIR = "./data/session_data"

# Ensure the directory exists for the tests
os.makedirs(SESSION_DIR, exist_ok=True)

# Parametrized test for happy path scenarios
@pytest.mark.parametrize("test_id, session_name, expected_output", [
    ("happy-1", "session1.txt", "File session1.txt has been deleted."),
    ("happy-2", "session2.log", "File session2.log has been deleted."),
    ("happy-3", "session3.json", "File session3.json has been deleted.")
])
def test_delete_session_happy_path(test_id, session_name, expected_output, capsys):
    # Arrange
    # Create a dummy session file to delete
    file_path = os.path.join(SESSION_DIR, session_name)
    with open(file_path, 'w') as f:
        f.write('dummy content')

    # Act
    delete_session(session_name)

    # Assert
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_output
    assert not os.path.exists(file_path)

# Parametrized test for edge cases
@pytest.mark.parametrize("test_id, session_name, expected_output", [
    ("edge-1", "", "File  does not exists in ./data/session_data."),
    ("edge-2", ".", "Error: [Errno 21] Is a directory: './data/session_data/.'"),
    ("edge-3", "..", "Error: [Errno 21] Is a directory: './data/session_data/..'"),
])
def test_delete_session_edge_cases(test_id, session_name, expected_output, capsys):
    # Act
    delete_session(session_name)

    # Assert
    captured = capsys.readouterr()
    expected_output = expected_output.replace('\\', '/')  # Normalize path separator
    assert captured.out.strip().replace('\\', '/') == expected_output

# Parametrized test for error cases
@pytest.mark.parametrize("test_id, session_name, expected_output", [
    ("error-1", "non_existent_file.txt", "File non_existent_file.txt does not exists in ./data/session_data."),
    ("error-2", "../outside.txt", "Error: [Errno 2] No such file or directory: './data/session_data/../outside.txt'")
])
def test_delete_session_error_cases(test_id, session_name, expected_output, capsys):
    # Act
    delete_session(session_name)

    # Assert
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_output

# Teardown code to clean up the session directory after tests
def teardown_module(module):
    # Remove the session directory and all its contents
    if os.path.exists(SESSION_DIR):
        for file in os.listdir(SESSION_DIR):
            os.remove(os.path.join(SESSION_DIR, file))
        os.rmdir(SESSION_DIR)

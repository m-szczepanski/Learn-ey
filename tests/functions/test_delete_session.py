import os
import pytest
from app.functions.delete_session import delete_session


SESSION_DIR = "./data/session_data"

os.makedirs(SESSION_DIR, exist_ok=True)


# Parametrized test for happy path scenarios
@pytest.mark.parametrize("test_id, session_name, expected_output", [
    ("happy-1", "session1.txt", "File session1.txt has been deleted."),
    ("happy-2", "session3.json", "File session3.json has been deleted.")
])
def test_delete_session_happy_path(test_id, session_name, expected_output, capsys):
    # Arrange
    file_path = os.path.join(SESSION_DIR, session_name)
    with open(file_path, 'w') as f:
        f.write('dummy content')

    # Act
    delete_session(session_name)

    # Assert
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_output
    assert not os.path.exists(file_path)


# Teardown code to clean up the session directory after tests
def teardown_module(module):
    # Remove the session directory and all its contents
    if os.path.exists(SESSION_DIR):
        for file in os.listdir(SESSION_DIR):
            os.remove(os.path.join(SESSION_DIR, file))
        os.rmdir(SESSION_DIR)

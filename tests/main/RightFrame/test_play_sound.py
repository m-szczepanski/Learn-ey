import pytest
import pygame

@pytest.fixture
def mock_pygame(mocker):
    mocker.patch('pygame.mixer.init')
    mocker.patch('pygame.mixer.music.set_volume')
    mocker.patch('pygame.mixer.music.load')
    mocker.patch('pygame.mixer.music.play')

# Parametrized test for happy path scenarios
@pytest.mark.parametrize("test_id, sound_input", [
    ("happy-1", 1),
    ("happy-2", 2),
    ("happy-3", 3),
])
def test_play_sound_happy_path(mock_pygame, test_id, sound_input):
    from app.main import RightFrame

    # Act
    RightFrame.play_sound(None, sound_input)

    # Assert
    pygame.mixer.init.assert_called_once()
    pygame.mixer.music.set_volume.assert_called_once_with(0.5)
    pygame.mixer.music.load.assert_called_once()
    pygame.mixer.music.play.assert_called_once_with(loops=0)

# Parametrized test for error cases
@pytest.mark.parametrize("test_id, sound_input, expected_exception", [
    ("error-nonexistent-sound", 0, ValueError),
    ("error-nonexistent-sound", 4, ValueError),
    ("error-invalid-type", "invalid", ValueError),
])
def test_play_sound_error_cases(mock_pygame, test_id, sound_input, expected_exception):
    from app.main import RightFrame

    # Act & Assert
    with pytest.raises(expected_exception):
        RightFrame.play_sound(None, sound_input)

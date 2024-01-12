import pytest
import tkinter as tk


class MockFrame(tk.Frame):
    def __init__(self):
        super().__init__()
        self.is_mapped = False

    def winfo_ismapped(self):
        return int(self.is_mapped)

class MockContainer:
    def __init__(self, frame_names):
        self.frames = {name: MockFrame() for name in frame_names}

    def show_frame(self, frame_name):
        if frame := self.frames.get(frame_name):
            frame.is_mapped = True

            for name, other_frame in self.frames.items():
                if name != frame_name:
                    other_frame.is_mapped = False


@pytest.mark.parametrize("frame_name, frame_names, test_id", [
    # Happy path tests
    ("frame1", ["frame1", "frame2", "frame3"], "happy_path_frame1"),
    ("frame2", ["frame1", "frame2", "frame3"], "happy_path_frame2"),
    ("frame3", ["frame1", "frame2", "frame3"], "happy_path_frame3"),

    # Edge cases
    ("frame1", ["frame1"], "edge_case_single_frame"),

    # Error cases
    ("frame4", ["frame1", "frame2", "frame3"], "error_case_nonexistent_frame"),
])
def test_show_frame(frame_name, frame_names, test_id):
    # Arrange
    container = MockContainer(frame_names)

    # Act
    container.show_frame(frame_name)

    # Assert
    for name, frame in container.frames.items():
        if name == frame_name:
            assert frame.winfo_ismapped() == 1, f"{test_id}: {frame_name} should be raised"
        else:
            assert frame.winfo_ismapped() == 0, f"{test_id}: {name} should be forgotten"


import pytest


class MockApp:
    def __init__(self):
        self.frames = {
            "left_frame": MockFrame("left_frame"),
            "right_frame": MockFrame("right_frame")
        }
        self.current_left_frame = None

    def show_frame(self, frame_name):
        if frame := self.frames.get(frame_name):
            if frame_name == 'left_frame':
                self.frames["right_frame"].set_main_panel_button_visibility(False)
                self.frames["left_frame"].update_top_panel()
            if frame_name == 'right_frame':
                frame.pack(side="right", fill='y')
                self.current_left_frame = None
            else:
                frame.pack(side="left", fill='y')
                self.frames['right_frame'].set_main_panel_button_visibility(True)

            frame.tkraise()

            if self.current_left_frame:
                self.current_left_frame.forget()
            self.current_left_frame = frame


class MockFrame:
    def __init__(self, name):
        self.name = name
        self.packed = False
        self.side = None
        self.visibility = None

    def pack(self, side, fill):
        self.packed = True
        self.side = side

    def tkraise(self):
        pass

    def forget(self):
        self.packed = False

    def set_main_panel_button_visibility(self, visibility):
        self.visibility = visibility

    def update_top_panel(self):
        pass


@pytest.mark.parametrize("frame_name, expected_side, expected_visibility, test_id", [
    # Happy path tests
    ("left_frame", "left", True, "happy_left_frame"),
    ("right_frame", "right", None, "happy_right_frame"),

    # Edge cases
    ("left_frame", "left", True, "edge_nonexistent_right_frame"),
    # Assuming there could be more frames in a real scenario
    ("bottom_frame", "left", True, "edge_unhandled_frame"),

    # Error cases
    # Assuming an error case where frame_name is None or empty
    (None, None, None, "error_none_frame_name"),
    ("", None, None, "error_empty_frame_name"),
])
def test_show_frame(frame_name, expected_side, expected_visibility, test_id):
    # Arrange
    app = MockApp()

    # Act
    app.show_frame(frame_name)

    # Assert
    if frame_name in app.frames:
        frame = app.frames[frame_name]
        assert frame.packed, f"{test_id}: Frame should be packed."
        assert frame.side == expected_side, f"{test_id}: Frame side should be '{expected_side}'."
        if frame_name == "left_frame":
            assert app.frames["right_frame"].visibility == expected_visibility, \
                f"{test_id}: Right frame visibility should be {expected_visibility}."
        elif frame_name == "right_frame":
            assert app.current_left_frame is frame, \
                f"{test_id}: Current left frame should be updated to the right frame."
    else:
        # Assuming that the original function should handle non-existent frames gracefully
        assert not app.frames["left_frame"].packed and not app.frames["right_frame"].packed, \
            f"{test_id}: Non-existent frames should not affect existing frames."

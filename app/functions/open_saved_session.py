from app.components.learning_session import LearningSession


def open_learning_session(session_name):
    """Open a learning session.

        This function opens a learning session with the specified session name.

        Args:
            session_name (str): The name of the learning session.
        """
    app = LearningSession(session_name)
    app.mainloop()

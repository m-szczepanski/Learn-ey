from app.components.learning_session import LearningSession


def open_learning_session(session_name):
    app = LearningSession(session_name)
    app.mainloop()

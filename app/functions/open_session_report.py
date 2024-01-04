from app.components.report_panel import ReportPanel


def open_session_report(wrong_answers, session_len):
    """Open a session report.

        This function opens a session report with the specified wrong answers and session length.

        Args:
            wrong_answers (list): A list of wrong answers.
            session_len (int): The length of the session.
        """
    app = ReportPanel(wrong_answers, session_len)
    app.mainloop()

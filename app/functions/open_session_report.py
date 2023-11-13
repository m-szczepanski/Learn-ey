from app.components.report_panel import ReportPanel


def open_session_report(wrong_answers, session_len):
    app = ReportPanel(wrong_answers, session_len)
    app.mainloop()

import tkinter as tk
from .main_window import Page


class AnswerGrader(Page):
    """Answer grading page - placeholder for now."""
    
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self._setup_ui()
        
    def _setup_ui(self):
        tk.Label(self, text="Answer Grading", font=("Arial", 16)).pack(pady=10)
        tk.Label(self, text="Answer grading functionality will be implemented here.").pack(pady=20)
import tkinter as tk
from .main_window import Page


class QuestionSetup(Page):
    """Question setup page - placeholder for now."""
    
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self._setup_ui()
        
    def _setup_ui(self):
        tk.Label(self, text="Question Setup", font=("Arial", 16)).pack(pady=10)
        tk.Label(self, text="Question setup functionality will be implemented here.").pack(pady=20)
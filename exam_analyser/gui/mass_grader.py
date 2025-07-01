import tkinter as tk
from .main_window import Page


class MassGrader(Page):
    """Mass grading page - placeholder for now."""
    
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self._setup_ui()
        
    def _setup_ui(self):
        tk.Label(self, text="Mass Grading", font=("Arial", 16)).pack(pady=10)
        tk.Label(self, text="Mass grading functionality will be implemented here.").pack(pady=20)
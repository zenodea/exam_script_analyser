import tkinter as tk
from .main_window import Page


class OCRAnalyzer(Page):
    """OCR analysis page - placeholder for now."""
    
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self._setup_ui()
        
    def _setup_ui(self):
        tk.Label(self, text="OCR Analysis", font=("Arial", 16)).pack(pady=10)
        tk.Label(self, text="OCR analysis functionality will be implemented here.").pack(pady=20)
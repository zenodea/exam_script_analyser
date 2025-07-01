import tkinter as tk


class Page(tk.Frame):
    """Base page class for GUI pages."""
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        """Bring this page to the front."""
        self.lift()


class MassGrader(Page):
    """Mass grading page - placeholder for now."""
    
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self._setup_ui()
        
    def _setup_ui(self):
        tk.Label(self, text="Mass Grading", font=("Arial", 16)).pack(pady=10)
        tk.Label(self, text="Mass grading functionality will be implemented here.").pack(pady=20)
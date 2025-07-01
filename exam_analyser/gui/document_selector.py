import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from ..core.document_analysis import DocumentImageAnalysis


class Page(tk.Frame):
    """Base page class for GUI pages."""
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        """Bring this page to the front."""
        self.lift()


class DocumentSelector(Page):
    """Document selection and analysis page."""
    
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.filename = None
        self.layout_model = None
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the user interface."""
        tk.Label(self, text="Document Selection", font=("Arial", 16)).pack(pady=10)
        
        # File selection button
        tk.Button(
            self,
            text="Select Document",
            width=25,
            height=2,
            command=self._select_file
        ).pack(pady=10)
        
        # Analysis button
        self.analyze_button = tk.Button(
            self,
            text="Analyze Document",
            width=25,
            height=2,
            command=self._analyze_document,
            state='disabled'
        )
        self.analyze_button.pack(pady=10)
        
        # Show results button
        self.show_button = tk.Button(
            self,
            text="Show Analysis",
            width=25,
            height=2,
            command=self._show_analysis,
            state='disabled'
        )
        self.show_button.pack(pady=10)
        
    def _select_file(self):
        """Select a document file."""
        self.filename = filedialog.askopenfilename(
            title="Select Document",
            filetypes=[("Image files", "*.png *.jpg *.jpeg")]
        )
        if self.filename:
            self.analyze_button.config(state='normal')
            
    def _analyze_document(self):
        """Analyze the selected document."""
        if not self.filename:
            return
            
        try:
            custom_label_map = {0: "answer", 1: "question", 2: "sub-question"}
            self.layout_model = DocumentImageAnalysis(
                r"Model/config.yaml",
                r"Model/model_final.pth",
                custom_label_map
            )
            self.layout_model.analyse_document(self.filename)
            self.show_button.config(state='normal')
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to analyze document: {e}")
            
    def _show_analysis(self):
        """Show the analysis results."""
        if self.layout_model:
            self.layout_model.draw_analysed_document()
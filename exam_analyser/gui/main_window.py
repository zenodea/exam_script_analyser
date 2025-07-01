import tkinter as tk
from .document_selector import DocumentSelector
from .ocr_analyzer import OCRAnalyzer
from .question_setup import QuestionSetup
from .answer_grader import AnswerGrader
from .mass_grader import MassGrader


class Page(tk.Frame):
    """Base page class for GUI pages."""
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        """Bring this page to the front."""
        self.lift()


class MainWindow(tk.Frame):
    """Main application window with tabbed interface."""
    
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        
        # Create pages
        self.document_selector = DocumentSelector(self)
        self.ocr_analyzer = OCRAnalyzer(self)
        self.question_setup = QuestionSetup(self)
        self.answer_grader = AnswerGrader(self)
        self.mass_grader = MassGrader(self)
        
        # Create button frame and container
        button_frame = tk.Frame(self)
        container = tk.Frame(self, bg="grey")
        button_frame.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)
        
        # Place pages in container
        self.document_selector.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.ocr_analyzer.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.question_setup.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.answer_grader.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.mass_grader.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        
        # Create navigation buttons
        tk.Button(
            button_frame, 
            text="Document Selection", 
            command=self.document_selector.show
        ).pack(side="left")
        
        tk.Button(
            button_frame, 
            text="OCR Analysis", 
            command=self.ocr_analyzer.show
        ).pack(side="left")
        
        tk.Button(
            button_frame, 
            text="Question Setup", 
            command=self.question_setup.show
        ).pack(side="left")
        
        tk.Button(
            button_frame, 
            text="Grade Answers", 
            command=self.answer_grader.show
        ).pack(side="left")
        
        tk.Button(
            button_frame, 
            text="Mass Grading", 
            command=self.mass_grader.show
        ).pack(side="right")
        
        # Show default page
        self.question_setup.show()

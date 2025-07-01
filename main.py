#!/usr/bin/env python3
"""
Exam Script Analyser - Main Entry Point

A Python application for analyzing and grading exam documents using OCR and document analysis.
"""

import tkinter as tk
import nltk
from exam_analyser.gui.main_window import MainWindow


def setup_nltk():
    """Download required NLTK data."""
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
    except Exception as e:
        print(f"Warning: Could not download NLTK data: {e}")


def main():
    """Main application entry point."""
    setup_nltk()
    
    root = tk.Tk()
    root.title("Exam Script Analyser")
    root.geometry("1000x800")
    
    app = MainWindow(root)
    app.pack(side="top", fill="both", expand=True)
    
    root.mainloop()


if __name__ == "__main__":
    main()

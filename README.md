# Exam Script Analyser

A Python application for analyzing and grading exam documents using optical character recognition (OCR) and document layout analysis.

## Features

- Document image analysis and layout detection
- Optical character recognition for handwritten text
- Automated answer grading and similarity comparison
- Question setup and keyword extraction  
- Mass document processing capabilities
- User-friendly graphical interface

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Setup

1. Clone or download this repository
2. Install the required dependencies
3. Run the application

## Usage

### Running the Application

```bash
python main.py
```

### Using the Interface

The application provides several modules:

1. **Document Selection**: Choose and analyze document images
2. **OCR Analysis**: Extract text from documents using OCR
3. **Question Setup**: Configure questions and keywords
4. **Answer Grading**: Grade individual answers
5. **Mass Grading**: Process multiple documents at once

### Supported File Formats

- PNG images
- JPEG images  
- JPG images

## Project Structure

```
exam_script_analyser/
├── exam_analyser/           # Main package
│   ├── core/               # Core functionality
│   │   ├── character_recognition.py
│   │   ├── document_analysis.py
│   │   └── grading.py
│   ├── gui/                # User interface
│   │   ├── main_window.py
│   │   ├── document_selector.py
│   │   └── other_components.py
│   └── utils/              # Utility functions
│       ├── file_operations.py
│       └── text_processing.py
├── main.py                 # Application entry point
├── requirements.txt        # Dependencies
└── setup.py               # Package setup
```

## Dependencies

The application requires several Python packages for document processing, OCR, and machine learning:

- OpenCV for image processing
- PIL/Pillow for image handling
- NLTK for natural language processing
- Layout Parser for document analysis
- Transformers for OCR models
- PyTorch for deep learning
- And others (see requirements.txt)
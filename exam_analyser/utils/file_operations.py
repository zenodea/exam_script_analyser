import os
import cv2
from ..core.document_analysis import DocumentImageAnalysis
from ..core.character_recognition import OpticalCharacterRecognition
from ..core import grading
from . import text_processing


def get_images_from_folder(folder_path):
    """Extract images from a folder and return image list and file paths."""
    image_list = []
    file_paths = []
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(folder_path, filename)
            file_paths.append(file_path)
            image = cv2.imread(file_path)
            image = image[..., ::-1]  # Convert BGR to RGB
            image_list.append(image)
    
    return image_list, file_paths


def analyse_documents(file_names):
    """Analyse multiple documents and extract text content."""
    result_list = []
    extracted_pages = []
    
    custom_label_map = {0: "answer", 1: "question", 2: "sub-question"}
    layout_model = DocumentImageAnalysis(
        r"Model/config.yaml",
        r"Model/model_final.pth",
        custom_label_map
    )
    
    # Analyse each document
    for file_path in file_names:
        name = os.path.basename(file_path)
        layout_model.analyse_document(file_path)
        extracted_pages.append((
            name,
            layout_model.stored_images_answer,
            layout_model.stored_images_questions,
            layout_model.stored_images_sub_questions
        ))
    
    # Process with OCR
    ocr = OpticalCharacterRecognition(use_pretrained=False)
    answer_dict = {}
    
    for page in extracted_pages:
        page_name, answers, questions, sub_questions = page
        temp = [page_name, len(answers)]
        answer_data = {}
        question_list = []
        
        try:
            for i in range(len(answers)):
                sub_question = ocr.direct_ocr(questions[i])[0] if i < len(questions) else ""
                question_list.append(sub_question)
                
                main_question = ocr.direct_ocr(sub_questions[i])[0] if i < len(sub_questions) else ""
                
                # Analyse answer text
                answer_text = ocr.analyse_image(answers[i], False)
                word_list = []
                for block in answer_text:
                    word_list.extend(block.split(" "))
                
                text_processor = text_processing.TextProcessor(word_list, [])
                processed_answer = text_processor.cleaned_text
                answer_data[sub_question + main_question] = processed_answer
                
        except IndexError:
            temp.extend(["error", "error"])
        
        temp.extend([question_list, []])
        result_string = (
            f"FileName: {temp[0]}\n"
            f"  No of Answers: {temp[1]}\n"
            f"    Question: {temp[2][0] if temp[2] else 'N/A'}\n"
            f"    Sub-Question: {temp[3][0] if temp[3] else 'N/A'}\n\n"
        )
        result_list.append(result_string)
        answer_dict[temp[0]] = answer_data
    
    return result_list, answer_dict


def grade_answers(question_dict, answer_dict):
    """Grade answers by comparing with question keywords."""
    question_keys = set(question_dict.keys())
    final_results = []
    
    for file_name, answers in answer_dict.items():
        file_results = [file_name]
        answer_keys = set(answers.keys())
        
        for key in answer_keys.intersection(question_keys):
            if key in question_dict and key in answers:
                similarity = grading.calculate_similarity(
                    question_dict[key], answers[key]
                )
                result_string = f"\n{key} : {similarity:.3f}"
                file_results.append(result_string)
        
        final_results.append(file_results)
    
    return final_results

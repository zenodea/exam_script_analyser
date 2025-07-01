import layoutparser as lp
import cv2
import numpy
from PIL import Image


class DocumentImageAnalysis:
    def __init__(self, config_path, model_path, custom_label_map):
        self.doc_path = None
        self.stored_images_answer = None
        self.stored_images_questions = None
        self.stored_images_sub_questions = None
        self.model = lp.Detectron2LayoutModel(
            config_path,
            model_path,
            extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8],
            label_map=custom_label_map
        )

    def analyse_document(self, document_path):
        self.doc_path = document_path
        image = Image.open(document_path)
        layout = self.model.detect(image)
        
        # Extract answer blocks
        answer_blocks = lp.Layout([b for b in layout if b.type == 'answer'])
        answer_images = []
        for block in answer_blocks:
            image_numpy = numpy.array(image)
            segment_image = (
                block.pad(left=5, right=5, top=5, bottom=5)
                .crop_image(image_numpy)
            )
            answer_images.append(segment_image)
        self.stored_images_answer = answer_images

        # Extract question blocks
        question_blocks = lp.Layout([b for b in layout if b.type == 'question'])
        question_images = []
        for block in question_blocks:
            image_numpy = numpy.array(image)
            segment_image = block.crop_image(image_numpy)
            question_images.append(segment_image)
        self.stored_images_questions = question_images

        # Extract sub-question blocks
        sub_question_blocks = lp.Layout([b for b in layout if b.type == 'sub-question'])
        sub_question_images = []
        for block in sub_question_blocks:
            image_numpy = numpy.array(image)
            segment_image = block.crop_image(image_numpy)
            sub_question_images.append(segment_image)
        self.stored_images_sub_questions = sub_question_images

    def draw_analysed_document(self):
        image = cv2.imread(self.doc_path)
        image = image[..., ::-1]
        lp.draw_box(image, self.model.detect(image)).show()

import numpy
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from PIL import Image
from transformers import VisionEncoderDecoderModel, TrOCRProcessor


class OpticalCharacterRecognition:
    def __init__(self, use_pretrained=True):
        self.analysed_document = None
        self.model_doctr = ocr_predictor(pretrained=use_pretrained)
        self.model_trocr = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-small-handwritten')
        self.processor_trocr = TrOCRProcessor.from_pretrained('microsoft/trocr-small-handwritten')

    def _add_image_padding(self, np_array):
        image = Image.fromarray(np_array)
        padding = 100
        width, height = image.size
        new_width = width + 2 * padding
        new_height = height + 2 * padding
        result = Image.new(image.mode, (new_width, new_height), (255, 255, 255))
        result.paste(image, (padding, padding))
        
        filepath = '/tmp/output.jpg'
        rgb_image = image.convert('RGB')
        rgb_image.save(filepath)
        return filepath

    def _get_word_list(self, image, show_analysis=False):
        filepath = self._add_image_padding(image)
        doc = DocumentFile.from_images(filepath)
        self.analysed_document = self.model_doctr(doc)

        if show_analysis:
            self.analysed_document.show(doc)

        image_obj = Image.open(filepath)
        image_list = []
        
        for page in self.analysed_document.pages:
            width = page.dimensions[1]
            height = page.dimensions[0]
            for block in page.blocks:
                for lines in block.lines:
                    for words in lines.words:
                        left = words.geometry[0][0] * width
                        top = words.geometry[0][1] * height
                        right = words.geometry[1][0] * width
                        bottom = words.geometry[1][1] * height
                        cropped_image = image_obj.crop((left, top, right, bottom))
                        image_list.append(numpy.asarray(cropped_image))
        return image_list

    def analyse_image(self, image, show_analysis=False):
        word_list = self._get_word_list(image, show_analysis)
        pixel_values = self.processor_trocr(images=word_list, return_tensors="pt").pixel_values
        generated_ids = self.model_trocr.generate(pixel_values)
        return self.processor_trocr.batch_decode(generated_ids, skip_special_tokens=True)

    def get_analysed_image(self, image):
        doc = DocumentFile.from_images('/tmp/output.jpg')
        self.analysed_document.show(doc)

    def direct_ocr(self, image):
        image_new = Image.fromarray(image).convert('RGB')
        pixel_values = self.processor_trocr(images=image_new, return_tensors="pt").pixel_values
        generated_ids = self.model_trocr.generate(pixel_values)
        return self.processor_trocr.batch_decode(generated_ids, skip_special_tokens=True)

import numpy
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from PIL import Image
from transformers import VisionEncoderDecoderModel, TrOCRProcessor


class OpCharRec:
    def __init__(self, boolean):
        self.analysedDocument = None
        self.modelDOCTR = ocr_predictor(pretrained=boolean)
        self.modeltrOCR = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-small-handwritten')
        self.processortrOCR = processor = TrOCRProcessor.from_pretrained('microsoft/trocr-small-handwritten')

    def __imagePadding(self, npArray):
        image = Image.fromarray(npArray)
        right = 100
        left = 100
        top = 100
        bottom = 100
        width, height = image.size
        new_width = width + right + left
        new_height = height + top + bottom
        result = Image.new(image.mode, (new_width, new_height), (255, 255, 255))
        result.paste(image, (left, top))
        filepath = '/Users/zenodeangeli/Downloads/output.jpg'
        rgb_im = image.convert('RGB')
        rgb_im.save(filepath)
        return filepath

    def __getWordList(self, image, showAnalysis):
        filepath = self.__imagePadding(image)
        doc = DocumentFile.from_images(filepath)
        self.analysedDocument = self.modelDOCTR(doc)

        if showAnalysis:
            self.analysedDocument.show(doc)

        im = Image.open('/Users/zenodeangeli/Downloads/output.jpg')
        imagelist = []
        for page in self.analysedDocument.pages:
            width = page.dimensions[1]
            height = page.dimensions[0]
            for block in page.blocks:
                for lines in block.lines:
                    for words in lines.words:
                        left = words.geometry[0][0] * width
                        top = words.geometry[0][1] * height
                        right = words.geometry[1][0] * width
                        bottom = words.geometry[1][1] * height
                        imagefinal = im.crop((left, top, right, bottom))
                        imagelist.append(numpy.asarray(imagefinal))
        return imagelist

    def analyseImage(self, image, showAnalysis):
        wordlist = self.__getWordList(image, showAnalysis)
        # Obtain Pixel Values from list of images
        pixel_values = self.processortrOCR(images=wordlist, return_tensors="pt").pixel_values
        # Encode
        generated_ids = self.modeltrOCR.generate(pixel_values)
        # Decode
        return self.processortrOCR.batch_decode(generated_ids, skip_special_tokens=True)

    def getAnalysedImage(self, image):
        doc = DocumentFile.from_images('/Users/zenodeangeli/Downloads/output.jpg')
        self.analysedDocument.show(doc)

    def directOCR(self, image):
        imageNew = Image.fromarray(image).convert('RGB')
        pixel_values = self.processortrOCR(images=imageNew, return_tensors="pt").pixel_values
        # Encode
        generated_ids = self.modeltrOCR.generate(pixel_values)
        # Decode
        return self.processortrOCR.batch_decode(generated_ids, skip_special_tokens=True)

import layoutparser as lp
import cv2
import numpy
from PIL import Image


class DIA:
    def __init__(self, configPath, modelPath, customLabelMap):
        self.docPath = None
        self.storedImagesAnswer = None
        self.storedImagesQuestions = None
        self.storedImagesSubQuestions = None
        self.model = lp.Detectron2LayoutModel(configPath,
                                              modelPath,
                                              extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8],
                                              label_map=customLabelMap)

    def analyseDocument(self, documentPath):
        self.docPath = documentPath
        im = Image.open(documentPath)
        layout = self.model.detect(im)
        # Get Answer Texts
        answer_blocks = lp.Layout([b for b in layout if b.type == 'answer'])
        # Start image cropping
        temp = []
        for block in answer_blocks:
            imnumpy = numpy.array(im)
            segment_image = (block
                             .pad(left=5, right=5, top=5, bottom=5)
                             .crop_image(imnumpy))
            # add padding in each image segment can help
            # improve robustness
            temp.append(segment_image)
        self.storedImagesAnswer = temp

        # Get Answer Texts
        answer_blocks = lp.Layout([b for b in layout if b.type == 'question'])
        temp = []
        for block in answer_blocks:
            imnumpy = numpy.array(im)
            segment_image = (block
                             .crop_image(imnumpy))
            # add padding in each image segment can help
            # improve robustness
            temp.append(segment_image)
        self.storedImagesQuestions = temp

        # Get Answer Texts
        answer_blocks = lp.Layout([b for b in layout if b.type == 'sub-question'])
        temp = []
        for block in answer_blocks:
            imnumpy = numpy.array(im)
            segment_image = (block
                             .crop_image(imnumpy))
            # add padding in each image segment can help
            # improve robustness
            temp.append(segment_image)
        self.storedImagesSubQuestions = temp

    def drawAnalysedDocument(self):
        image = cv2.imread(self.docPath)
        image = image[..., ::-1]
        lp.draw_box(image, self.model.detect(image)).show()

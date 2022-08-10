import warnings
import os
import cv2
from documentImageAnalysis import DIA
from characterRecogntion import OpCharRec
import examGrading
import postProcessing

def obtainImages(folderPath):
    # Return Variable
    image_list = []

    # Image List Directory
    directory = os.fsencode(folderPath)

    listOfFiles = []
    # Loop through directory
    for file in os.listdir(directory):
        filename = os.fsdecode(file)

        # Obtain Image
        if filename.endswith(".png") or filename.endswith(".jpg"):
            filePath = folderPath + "/" + filename
            listOfFiles.append(filePath)
            image = cv2.imread(filePath)
            image = image[..., ::-1]
            image_list.append(image)

    return image_list, listOfFiles


def analyseDocuments(fileName):
    returnList = []
    extractedPages = []
    custom_label_map = {0: "answer", 1: "question", 2: "sub-question"}
    lpmodel = DIA(r"Model/config.yaml",
                  r"Model/model_final.pth",
                  custom_label_map)
    for count, file in enumerate(fileName):
        name = os.path.basename(file)
        lpmodel.analyseDocument(file)
        extractedPages.append((name, lpmodel.storedImagesAnswer, lpmodel.storedImagesQuestions,
                               lpmodel.storedImagesSubQuestions))
    ocr = OpCharRec(False)
    answerDict = {}
    for page in extractedPages:
        temp = [page[0], len(page[1])]
        subtemp = []
        answer = {}
        questiontemp = []
        try:
            for x in range(len(page[1])):
                subQuestion = ocr.directOCR(page[2][x])[0]
                subtemp.append(subQuestion)
                question = ocr.directOCR(page[3][x])[0]
                questiontemp.append(question)
                fia = ocr.analyseImage(page[1][x], False)
                wordList = []
                for block in fia:
                    words = block.split(" ")
                    for word in words:
                        wordList.append(word)
                text = postProcessing.TextCleanUp(wordList, [])
                currAnswerKeywords = text.cleanedUpText
                answer[subQuestion[0]+question[0]] = currAnswerKeywords
                print(currAnswerKeywords)
        except IndexError:
            temp.append("error")
            temp.append("error")
        temp.append(questiontemp)
        temp.append(subtemp)
        string = f"FileName: {temp[0]}\n  No of Answers: {temp[1]}\n    Question: {temp[2][0]}\n    " \
                 f"Sub-Question: {temp[3][0]}\n\n"
        returnList.append(string)
        answerDict[temp[0]] = answer
    print(answerDict)
    return returnList, answerDict


def gradeAnswers(questionDict,answerDict):
    q = set(questionDict)
    finalList = []
    for fileName in answerDict:
        temp = []
        a = set(fileName)
        temp.append(fileName)
        for name in a.intersection(q):
            answer = examGrading.obtainSimilarity(questionDict[name],answerDict[name])
            string = f"\n{name} : {answer}"
            temp.append(string)
        finalList.append(temp)
    return finalList

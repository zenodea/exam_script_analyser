from documentImageAnalysis import DIA
import tkinter as tk
from tkinter import filedialog
from characterRecogntion import OpCharRec
from postProcessing import  TextCleanUp
from quearyExpansion import QuearyExpansion
from PIL import Image
import os
import guiFunctions
import nltk

answerDict = None
questionKeywordsDict = {}
lpDocument = None
lpDocumentQuestions = None
lpDocumentSub = None
ocrAnalysis = None
currAnswerKeywords = None
currQuestionKeywords = None


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class massGradingPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.questionKeywords = None
        self.questions = None
        self.questionSub = None
        self.questionNumber = None
        self.query = QuearyExpansion("AIzaSyA08U6HI20_JVgCDkZTRp-B3Wq0Ch1j8co", "1341c904f8dbf41ed")
        label = tk.Label(self, text="Mass Grading Document")
        self.documentList = None
        self.previousRow = 0
        label.pack(side="top")
        self.__mainPage()

    def obtainKeywords(self):
        top10Terms = self.query.top_10_terms(self.questions.get("1.0", 'end-1c'))
        self.questionKeywords.insert(tk.END, top10Terms)

    def addRow(self):
        global questionKeywordsDict
        self.questionNumber["state"] = "disabled"
        self.questionSub["state"] = "disabled"
        self.questions["state"] = "disabled"
        self.obtainKeywords()
        questionKeywordsDict[str(self.questionNumber.get("1.0", 'end-1c'))+str(self.questionSub.get("1.0", 'end-1c'))] \
            = self.questionKeywords.get("1.0", 'end-1c')
        print(questionKeywordsDict)
        self.questionNumber = tk.Text(self.frameQuestions, height=3, width=5)
        self.questionNumber.grid(column=0, row=self.previousRow)
        self.questionSub = tk.Text(self.frameQuestions, height=3, width=5)
        self.questionSub.grid(column=1, row=self.previousRow)
        self.questions = tk.Text(self.frameQuestions, height=3, width=30)
        self.questions.grid(column=2, row=self.previousRow)
        self.questionKeywords = tk.Text(self.frameQuestions, height=3, width=30)
        self.questionKeywords.grid(column=3, row=self.previousRow)
        self.previousRow += 1

    def getDocumentNameList(self):
        filename = filedialog.askdirectory()
        images = main.obtainImages(filename)
        self.documentList = images[1]
        for i in images[1]:
            self.initialDocumentList.insert("end", os.path.basename(i))

    def analyseDocuments(self):
        global answerDict
        images = main.analyseDocuments(self.documentList)
        answerDict = images[1]
        for i in images[0]:
            self.analysedDocumentList.insert("end", i)

    def gradeAnswer(self):
        global answerDict, questionKeywordsDict
        print(main.gradeAnswers(questionKeywordsDict, answerDict))

    def __mainPage(self):
        frame = tk.Frame(self)
        frame.pack(padx=50, pady=50)
        self.initialDocumentList = tk.Listbox(frame)
        self.initialDocumentList.grid(column=0, row=0, columnspan=1)
        tk.Button(frame,
                  text="Get Information",
                  width=15,
                  height=5,
                  bg="grey",
                  fg="black",
                  command=self.getDocumentNameList
                  ).grid(column=0, row=1, columnspan=1)
        self.analysedDocumentList = tk.Text(frame, height=15, width=40)
        self.analysedDocumentList.grid(column=1, row=0, columnspan=1)
        tk.Button(frame,
                  text="Analyse Documents",
                  width=15,
                  height=5,
                  bg="grey",
                  fg="black",
                  command=self.analyseDocuments
                  ).grid(column=1, row=1, columnspan=1)
        self.correctedDocumentList = tk.Listbox(frame)
        self.correctedDocumentList.grid(column=2, row=0, columnspan=1)
        tk.Button(frame,
                  text="Grade",
                  width=15,
                  height=5,
                  bg="grey",
                  fg="black",
                  command=self.gradeAnswer
                  ).grid(column=2, row=1, columnspan=1)

        self.frameQuestions = tk.Frame(self)
        self.frameQuestions.pack()
        self.questionNumber = tk.Text(self.frameQuestions, height=3, width=5)
        self.questionNumber.grid(column=0, row=self.previousRow)
        self.questionSub = tk.Text(self.frameQuestions, height=3, width=5)
        self.questionSub.grid(column=1, row=self.previousRow)
        self.questions = tk.Text(self.frameQuestions, height=3, width=30)
        self.questions.grid(column=2, row=self.previousRow)
        self.questionKeywords = tk.Text(self.frameQuestions, height=3, width=30)
        self.questionKeywords.grid(column=3, row=self.previousRow)
        self.previousRow += 1
        self.addRowBtn = tk.Button(self,
                                   text="Add Question",
                                   width=25,
                                   height=5,
                                   bg="grey",
                                   fg="black",
                                   command=self.addRow
                                   )
        self.addRowBtn.pack()


class answerPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="Grade Document")
        label.pack(side="top")
        self.__mainPage()

    def __mainPage(self):
        frame = tk.Frame(self)
        frame.pack(padx=50, pady=50)
        self.studentAnswer = tk.Text(frame, height=6, width=30)
        self.studentAnswer.grid(column=0, row=0)
        self.studentAnswer["state"] = "disabled"
        self.questionKeywords = tk.Text(frame, height=6, width=30)
        self.questionKeywords.grid(column=3, row=0)
        self.questionKeywords["state"] = "disabled"
        tk.Button(frame,
                  text="Get Information",
                  width=15,
                  height=5,
                  bg="grey",
                  fg="black",
                  command=self.updateInformation
                  ).grid(column=1, row=1, columnspan=1)
        tk.Button(frame,
                  text="Similarity Between Information",
                  width=15,
                  height=5,
                  bg="grey",
                  fg="black"
                  ).grid(column=2, row=1, columnspan=1)
        self.similarity = tk.Text(self, height=6, width=30)
        self.similarity.pack()

    def updateInformation(self):
        global currQuestionKeywords, currAnswerKeywords
        self.studentAnswer.insert("end-1c", currAnswerKeywords)
        self.questionKeywords.insert("end-1c", currQuestionKeywords)


class DocumentSelection(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="Document Selection")
        label.pack(side="top")
        self.filename = None
        custom_label_map = {0: "answer", 1: "question", 2: "sub-question"}
        self.lpmodel = DIA(r"Model/config.yaml",
                           r"Model/model_final.pth",
                           custom_label_map)
        self.__firstPage()

    def selectFile(self):
        self.filename = filedialog.askopenfilename()
        self.__switch()

    def analyseDoc(self):
        global lpDocument, lpDocumentQuestions, lpDocumentSub
        if self.filename is None:
            print("No")
        else:
            self.lpmodel.analyseDocument(self.filename)
            lpDocument = self.lpmodel.storedImagesAnswer
            lpDocumentQuestions = self.lpmodel.storedImagesQuestions
            lpDocumentSub = self.lpmodel.storedImagesSubQuestions
            self.update_idletasks()

    def showAnalysedDoc(self):
        self.lpmodel.drawAnalysedDocument()

    def __switch(self):
        self.buttonAnalyseDoc['state'] = 'active'
        self.buttonShowAnalysedDoc['state'] = 'active'

    def __firstPage(self):
        self.buttonSelDoc = tk.Button(self,
                                      text="Select Document!",
                                      width=25,
                                      height=5,
                                      bg="grey",
                                      fg="black",
                                      command=self.selectFile
                                      )
        self.buttonSelDoc.pack(padx=50, pady=50)

        #
        self.buttonAnalyseDoc = tk.Button(self,
                                          text="Analyse Doc!",
                                          width=25,
                                          height=5,
                                          bg="grey",
                                          fg="black",
                                          command=self.analyseDoc
                                          )
        self.buttonAnalyseDoc['state'] = 'disabled'
        self.buttonAnalyseDoc.pack(padx=50, pady=50)

        #
        self.buttonShowAnalysedDoc = tk.Button(self,
                                               text="Show Doc!",
                                               width=25,
                                               height=5,
                                               bg="grey",
                                               fg="black",
                                               command=self.showAnalysedDoc
                                               )
        self.buttonShowAnalysedDoc['state'] = 'disabled'
        self.buttonShowAnalysedDoc.pack(padx=50, pady=50)


class OCRAnalysis(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.sub = None
        self.question = None
        label = tk.Label(self, text="Ocr Analysis")
        label.pack(side="top")
        self.pageIndex = 0
        self.ocrAnalysis = None
        self.ocr = OpCharRec(True)
        self.__mainPage()

    def __mainPage(self):
        global lpDocument
        frame1 = tk.Frame(self)
        frame1.pack(padx=50, pady=50)

        tk.Button(frame1,
                  text="Next Question",
                  width=25,
                  height=5,
                  bg="grey",
                  fg="black",
                  command=self.nextPage
                  ).grid(column=0, row=0, columnspan=1)

        self.ShowCurrNum = tk.Button(frame1,
                                     text="Show Answer #" + str(self.pageIndex + 1),
                                     width=25,
                                     height=5,
                                     bg="grey",
                                     fg="black",
                                     command=self.showSelectedPaper
                                     )
        self.ShowCurrNum.grid(column=1, row=0, columnspan=1)

        self.ShowCurrAnalysis = tk.Button(frame1,
                                          text="Show Answer Analysis",
                                          width=25,
                                          height=5,
                                          bg="grey",
                                          fg="black",
                                          command=self.showSelectedPaperAnalysis
                                          )
        self.ShowCurrAnalysis.grid(column=2, row=0, columnspan=1)
        self.ShowCurrAnalysis['state'] = 'disabled'

        self.ShowCurrQuestion = tk.Button(frame1,
                                          text="Show Question",
                                          width=25,
                                          height=5,
                                          bg="grey",
                                          fg="black",
                                          command=self.showSelectedQuestion
                                          )
        self.ShowCurrQuestion.grid(column=1, row=1, columnspan=1)

        self.ShowCurrSub = tk.Button(frame1,
                                     text="Show Sub-Question",
                                     width=25,
                                     height=5,
                                     bg="grey",
                                     fg="black",
                                     command=self.showSelectedSubQuestion
                                     )
        self.ShowCurrSub.grid(column=1, row=2, columnspan=1)

        frame = tk.Frame(self)
        frame.pack(padx=50, pady=50)
        tk.Button(frame,
                  text="Analyse Document with OCR",
                  width=25,
                  height=5,
                  bg="grey",
                  fg="black",
                  command=self.analyseOCR
                  ).grid(column=0, row=2, columnspan=1)

        # Create text widget and specify size.
        self.T = tk.Text(frame, height=5, width=52)
        self.T.grid(column=1, row=2, columnspan=1)

        tk.Button(frame,
                  text="Obtain KeyPoints",
                  width=25,
                  height=5,
                  bg="grey",
                  fg="black",
                  command=self.gatherKeywords
                  ).grid(column=0, row=3, columnspan=1)

        self.keyPoints = tk.Text(frame, height=5, width=52)
        self.keyPoints.grid(column=1, row=3, columnspan=1)

    def showSelectedPaper(self):
        global lpDocument
        Image.fromarray(lpDocument[self.pageIndex]).show()

    def showSelectedQuestion(self):
        global lpDocumentQuestions
        Image.fromarray(lpDocumentQuestions[self.pageIndex]).show()

    def showSelectedSubQuestion(self):
        global lpDocumentSub
        Image.fromarray(lpDocumentSub[self.pageIndex]).show()

    def showSelectedPaperAnalysis(self):
        global lpDocument
        self.ocr.getAnalysedImage(lpDocument[self.pageIndex])

    def nextPage(self):
        global lpDocument
        if self.pageIndex + 1 == len(lpDocument):
            self.pageIndex = 0
            self.ShowCurrNum['text'] = "Show Answer #" + str(self.pageIndex + 1)
            self.ShowCurrAnalysis['state'] = 'disabled'
        else:
            self.pageIndex += 1
            self.ShowCurrNum['text'] = "Show Answer #" + str(self.pageIndex + 1)
            self.ShowCurrAnalysis['state'] = 'disabled'

    def analyseOCR(self):
        global lpDocument, ocrAnalysis, lpDocumentQuestions, lpDocumentSub
        # Insert The Fact.
        self.question = self.ocr.directOCR(lpDocumentQuestions[self.pageIndex])
        self.sub = self.ocr.directOCR(lpDocumentSub[self.pageIndex])
        self.ocrAnalysis = self.ocr.analyseImage(lpDocument[self.pageIndex], False)
        self.T.insert(tk.END, "\nQuestion: " + str(self.question) + "\nSub-Question: " +
                              str(self.sub) + "\nAnswer: " + ' '.join(self.ocrAnalysis))
        self.ShowCurrAnalysis['state'] = 'active'

    def gatherKeywords(self):
        global currAnswerKeywords
        wordList = []
        for block in self.ocrAnalysis:
            words = block.split(" ")
            print(words)
            for word in words:
                wordList.append(word)
        text = TextCleanUp(wordList, [])
        currAnswerKeywords = text.cleanedUpText
        self.keyPoints.insert(tk.END, text.cleanedUpText)


class queryExpansion(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.questionKeywords = None
        self.questions = None
        self.questionSub = None
        self.questionNumber = None
        self.query = QuearyExpansion("AIzaSyA08U6HI20_JVgCDkZTRp-B3Wq0Ch1j8co", "1341c904f8dbf41ed")
        label = tk.Label(self, text="Question Set Up")
        label.pack(side="top")
        self.previousRow = 0
        self.query = QuearyExpansion("AIzaSyA08U6HI20_JVgCDkZTRp-B3Wq0Ch1j8co", "1341c904f8dbf41ed")
        self.__mainPage()
    def addRow(self):
        global questionKeywordsDict
        self.questionNumber["state"] = "disabled"
        self.questionSub["state"] = "disabled"
        self.questions["state"] = "disabled"
        self.obtainKeywords()
        questionKeywordsDict[str(self.questionNumber.get("1.0", 'end-1c'))+str(self.questionSub.get("1.0", 'end-1c'))] \
            = self.questionKeywords.get("1.0", 'end-1c')
        print(questionKeywordsDict)
        self.questionNumber = tk.Text(self.frameQuestions, height=3, width=5)
        self.questionNumber.grid(column=0, row=self.previousRow)
        self.questionSub = tk.Text(self.frameQuestions, height=3, width=5)
        self.questionSub.grid(column=1, row=self.previousRow)
        self.questions = tk.Text(self.frameQuestions, height=3, width=30)
        self.questions.grid(column=2, row=self.previousRow)
        self.questionKeywords = tk.Text(self.frameQuestions, height=3, width=30)
        self.questionKeywords.grid(column=3, row=self.previousRow)
        self.previousRow += 1

    def __mainPage(self):
        self.frameQuestions = tk.Frame(self)
        self.frameQuestions.pack()
        self.questionNumber = tk.Text(self.frameQuestions, height=3, width=5)
        self.questionNumber.grid(column=0, row=self.previousRow)
        self.questionSub = tk.Text(self.frameQuestions, height=3, width=5)
        self.questionSub.grid(column=1, row=self.previousRow)
        self.questions = tk.Text(self.frameQuestions, height=3, width=30)
        self.questions.grid(column=2, row=self.previousRow)
        self.questionKeywords = tk.Text(self.frameQuestions, height=3, width=30)
        self.questionKeywords.grid(column=3, row=self.previousRow)
        self.previousRow += 1
        self.addRowBtn = tk.Button(self,
                                   text="Add Question",
                                   width=25,
                                   height=5,
                                   bg="grey",
                                   fg="black",
                                   command=self.addRow
                                   )
        self.addRowBtn.pack()
        self.frameDataGather = tk.Frame(self)
        self.Datagather = tk.Text(self.frameDataGather, height=5, width=52)
        self.Datagather.grid(column=2, row=0)
        tk.Button(self.frameDataGather,
                  text="Confirm Topics of Exam",
                  width=25,
                  height=5,
                  bg="grey",
                  fg="black",
                  command=self.confirmTopic
                  ).grid(column=0, row=0)
        self.frameDataGather.pack()

    def obtainKeywords(self):
        top10Terms = self.query.top_10_terms(self.questions.get("1.0", 'end-1c'))
        self.questionKeywords.insert(tk.END, top10Terms)

    def confirmTopic(self):
        self.Datagather.tag_add("here", "1.0", tk.END)
        self.Datagather.tag_config("here", background="black", foreground="green")
        self.Datagather["state"] = "disabled"


class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = DocumentSelection(self)
        p2 = OCRAnalysis(self)
        p3 = queryExpansion(self)
        p4 = answerPage(self)
        p6 = massGradingPage(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self, bg="grey")
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p6.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Select Document", command=p1.show)
        b2 = tk.Button(buttonframe, text="Analyse Document", command=p2.show)
        b3 = tk.Button(buttonframe, text="Question Set up", command=p3.show)
        b4 = tk.Button(buttonframe, text="Grade Document", command=p4.show)
        b6 = tk.Button(buttonframe, text="Mass Document Grading", command=p6.show)

        b3.pack(side="left")
        b1.pack(side="left")
        b2.pack(side="left")
        b4.pack(side="left")
        b6.pack(side="right")

        p3.show()


if __name__ == "__main__":
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    root = tk.Tk()
    root.geometry("1000x800")
    app = MainView(root)
    app.pack(side="top", fill="both", expand=True)
    root.mainloop()

import nltk
from pyxdameraulevenshtein import damerau_levenshtein_distance


def findVN(wordList, boolean):
    tokenized = nltk.word_tokenize(' '.join(wordList))
    tagged = nltk.pos_tag(tokenized)
    nouns = [x[0] for x in tagged if x[1] == "NN"]
    verbs = [x[0] for x in tagged if x[1] == "VB"]
    adjective = [x[0] for x in tagged if x[1] == "JJ"]
    adverbs = [x[0] for x in tagged if x[1] == "RB"]
    noun = [word for word in nouns if len(word) >= 2]
    verb = [word for word in verbs if len(word) >= 2]
    adj = [word for word in adjective if len(word) >= 2]
    adv = [word for word in adverbs if len(word) >= 2]
    return noun + verb + adj + adv


class TextCleanUp:
    def __init__(self, textList, keywords):
        self.cleanedUpText = self.returnVN(textList)

    def __correct_sentence(self, sentence, keywords):
        new_sentence = []
        for word in ' '.join(sentence):
            budget = 2
            n = len(word)
            if n < 3:
                budget = 0
            elif 3 <= n < 6:
                budget = 1
            if budget:
                for keyword in keywords:
                    if damerau_levenshtein_distance(word, keyword) <= budget:
                        new_sentence.append(keyword)
                        break
                else:
                    new_sentence.append(word)
            else:
                new_sentence.append(word)
        return new_sentence

    def getCorrectedSentence(self):
        return self.cleanedUpText

    def returnVN(self, text):
        return findVN(text, True)


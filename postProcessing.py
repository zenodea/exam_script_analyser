import nltk
from pyxdameraulevenshtein import damerau_levenshtein_distance
from googleapiclient.discovery import build
from collections import Counter
import pprint


def findVN(wordList, boolean):
    tokenized = nltk.word_tokenize(' '.join(wordList))
    tagged = nltk.pos_tag(tokenized)
    nouns = [x[0] for x in tagged if x[1] == "NN"]
    verbs = [x[0] for x in tagged if x[1] == "VB"]
    if boolean:
        noun = [word for word in nouns if len(word) >= 2]
        verb = [word for word in verbs if len(word) >= 2]
        return noun + verb
    return nouns + verbs


class TextCleanUp:
    def __init__(self, textList, keywords):
        self.cleanedUpText = self.returnVN(self.__correct_sentence(textList, keywords))

    def __correct_sentence(self, sentence, keywords):
        new_sentence = []
        for word in sentence:
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

class quearyExpansion:
    def __init__(self, api_key, cse_id):
        self.my_api_key = api_key
        self.my_cse_id = cse_id

    def google_search(self, search_term, **kwargs):
        service = build("customsearch", "v1", developerKey=self.my_api_key)
        res = service.cse().list(q=search_term, cx=self.my_cse_id, **kwargs).execute()
        return res['items']

    def top_10_terms(self, search_term):
        results = self.google_search(search_term)
        temp = []
        for result in results:
            temp.append(result.get("snippet"))
        joinedSnippets = ' '.join(temp)

        listVN = findVN(joinedSnippets.split(" "), False)
        # Frequency and Top Terms
        wordFrequency = Counter(listVN)
        mostCommon = wordFrequency.most_common()[0:15]
        contextualQueryExpansionKeywords = []
        for x in mostCommon:
            contextualQueryExpansionKeywords.append(x[0])
        return contextualQueryExpansionKeywords

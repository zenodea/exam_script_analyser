from googleapiclient.discovery import build
from collections import Counter
import nltk

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

class QuearyExpansion:
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

import pyxdameraulevenshtein
from collections import Counter
from math import sqrt


def correct_sentence(sentence, keywords):
    new_sentence = []
    for word in sentence:
        budget = 2
        n = lewn(word)
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


def cleanUpList(wordList):
    temp = []
    for w in wordList:
        if wordnet.synsets(w):
            temp.append(w)
    return temp


def word2vec(word):
    from collections import Counter
    from math import sqrt

    # count the characters in word
    cw = Counter(word)
    # precomputes a set of the different characters
    sw = set(cw)
    # precomputes the "length" of the word vector
    lw = sqrt(sum(c * c for c in cw.values()))

    # return a tuple
    return cw, sw, lw


def cosdis(v1, v2):
    # which characters are common to the two words?
    common = v1[1].intersection(v2[1])
    # by definition of cosine distance we have
    return sum(v1[0][ch] * v2[0][ch] for ch in common) / v1[2] / v2[2]


def obtainSimilarity(list_A, list_B):
    overThreshold = 0
    overThresholdscore = 0

    threshold = 0.75  # if needed
    for key in list_A:
        for word in list_B:
            try:
                res = cosdis(word2vec(word), word2vec(key))
                if (res > threshold):
                    overThreshold += 1
                    overThresholdscore += res
            # if res > threshold:
            #     print("Found a word with cosine distance > 80 : {} with original word: {}".format(word, key))
            except IndexError:
                pass
    return overThresholdscore / overThreshold


def findVN(wordList):
    tokenized = nltk.word_tokenize(''.join(wordList))
    tagged = nltk.pos_tag(tokenized)
    nouns = [x[0] for x in tagged if x[1] == "NN"]
    verbs = [x[0] for x in tagged if x[1] == "VB"]
    return nouns + verbs
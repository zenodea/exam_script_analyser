import nltk
from pyxdameraulevenshtein import damerau_levenshtein_distance


def extract_meaningful_words(word_list):
    """Extract nouns, verbs, adjectives, and adverbs from word list."""
    tokenized = nltk.word_tokenize(' '.join(word_list))
    tagged = nltk.pos_tag(tokenized)
    
    nouns = [word for word, pos in tagged if pos == "NN" and len(word) >= 2]
    verbs = [word for word, pos in tagged if pos == "VB" and len(word) >= 2]
    adjectives = [word for word, pos in tagged if pos == "JJ" and len(word) >= 2]
    adverbs = [word for word, pos in tagged if pos == "RB" and len(word) >= 2]
    
    return nouns + verbs + adjectives + adverbs


class TextProcessor:
    """Text processing and cleanup utilities."""
    
    def __init__(self, text_list, keywords=None):
        self.keywords = keywords or []
        self.cleaned_text = self._extract_meaningful_words(text_list)

    def _correct_sentence(self, sentence, keywords):
        """Correct words in sentence using edit distance."""
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

    def get_corrected_text(self):
        """Get the corrected and cleaned text."""
        return self.cleaned_text

    def _extract_meaningful_words(self, text):
        """Extract meaningful words from text."""
        return extract_meaningful_words(text)

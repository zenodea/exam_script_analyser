import pyxdameraulevenshtein
from collections import Counter
from math import sqrt
from nltk.corpus import wordnet


def correct_sentence(sentence, keywords):
    """Correct words in sentence using edit distance with keywords."""
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
                if pyxdameraulevenshtein.damerau_levenshtein_distance(word, keyword) <= budget:
                    new_sentence.append(keyword)
                    break
            else:
                new_sentence.append(word)
        else:
            new_sentence.append(word)
    return new_sentence


def clean_word_list(word_list):
    """Filter words that exist in WordNet."""
    return [word for word in word_list if wordnet.synsets(word)]


def word_to_vector(word):
    """Convert word to character frequency vector."""
    char_count = Counter(word)
    char_set = set(char_count)
    vector_length = sqrt(sum(c * c for c in char_count.values()))
    return char_count, char_set, vector_length


def cosine_distance(vector1, vector2):
    """Calculate cosine distance between two word vectors."""
    common_chars = vector1[1].intersection(vector2[1])
    return sum(vector1[0][ch] * vector2[0][ch] for ch in common_chars) / vector1[2] / vector2[2]


def calculate_similarity(answer_words, question_words):
    """Calculate similarity score between answer and question word lists."""
    over_threshold = 0
    over_threshold_score = 0
    threshold = 0.75
    
    for answer_word in answer_words:
        for question_word in question_words:
            try:
                similarity = cosine_distance(
                    word_to_vector(question_word), 
                    word_to_vector(answer_word)
                )
                if similarity > threshold:
                    over_threshold += 1
                    over_threshold_score += similarity
            except (IndexError, ZeroDivisionError):
                pass
                
    return over_threshold_score / over_threshold if over_threshold > 0 else 0

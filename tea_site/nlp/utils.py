from collections import Counter, defaultdict
from string import punctuation

import pandas as pd
from nltk.stem.snowball import RussianStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from pymystem3 import Mystem
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

stop_words = set(stopwords.words("russian"))
tokenizer = RegexpTokenizer(r"\w+")
stemmer = RussianStemmer()
m = Mystem()


def preprocess_text(text):
    tokens = tokenizer.tokenize(str(text).lower())
    filtered_tokens = [
        token
        for token in tokens
        if token not in stop_words and token != " " and token not in punctuation
    ]
    return filtered_tokens


def stemmed_text(text):
    tokens = preprocess_text(text)
    stemmed = [stemmer.stem(token) for token in tokens]
    return stemmed


def lemmatized_text(text):
    tokens = preprocess_text(text)
    lemmas = m.lemmatize(" ".join(tokens))
    lemmatized_words = "".join(lemmas).split()
    return lemmatized_words


def get_jaccard_sim(str1, str2):
    a = set(str1)
    b = set(str2)
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))


def get_cosine_sim(str1, str2):
    str1 = " ".join(str1)
    str2 = " ".join(str2)
    vectors = [t for t in get_vectors(str1, str2)]
    return cosine_similarity(vectors)[0][1]


def get_vectors(*strs):
    text = [t for t in strs]
    vectorizer = CountVectorizer(text)
    vectorizer.fit(text)
    return vectorizer.transform(text).toarray()

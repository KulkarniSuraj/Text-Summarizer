#  import dependencies
from nltk.tokenize import word_tokenize, sent_tokenize, PunktSentenceTokenizer
from nltk.corpus import stopwords
import heapq
from bs4 import BeautifulSoup
import requests
import re


def filter_text(paragraph_list):
    article_text = ""
    for para in paragraph_list:
        article_text += para.text
    # removing brackets and replacing them with spaces
    article_text = re.sub(r'\[[0-9a-zA-Z]*\]', ' ', article_text)
    # removing extra spaces and replacing them with single space
    article_text = re.sub(r'\s+', ' ', article_text)
    return article_text


def sentence_tokenization(text_data):
    custom_sent_tokenizer = PunktSentenceTokenizer(train_text=text_data)
    tokenized_sent = []
    # tokenize sentences
    for line in custom_sent_tokenizer.tokenize(text_data):
        tokenized_sent.append(line)
    return tokenized_sent


def word_tokenization(text):
    tokenized_words = []
    # tokenize words
    for word in word_tokenize(text):
        tokenized_words.append(word)
    return tokenized_words


def calculate_word_frequencies(words):
    # finding the frequencies of words
    word_frequencies = {}
    for word in words:
        if word not in stop_words:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    return word_frequencies


def calculate_sent_scores(tokenized_sent, word_frequencies):
    sent_scores = {}

    # calculating sentence scores
    for sent in tokenized_sent:
        for word in word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sent_scores.keys():
                        sent_scores[sent] = word_frequencies[word]
                    else:
                        sent_scores[sent] += word_frequencies[word]

    return sent_scores


def normalize_word_freq(word_frequencies):
    # finding the maximum frequency
    maximum_frequncy = max(word_frequencies.values())
    # dividing each freq with max frequency
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

    return word_frequencies


def summarize(sent_scores):
    # finding top sentences based on their frequencies
    summary_sentences = heapq.nlargest(5, sent_scores, key=sent_scores.get)
    # joining the sentences to create summary
    summary = ' '.join(summary_sentences)
    return summary


def wiki_info(url):
    source = requests.get(url).text  # source code of given web page
    soup = BeautifulSoup(source, 'lxml')
    article = soup.find_all('p')  # list of all paragraphs on page
    return article


# driver code
stop_words = set(stopwords.words("english"))  # stop words collection


def get_summary(url="https://en.wikipedia.org/wiki/Ketosis"):
    article = wiki_info(url)
    article_text = filter_text(article)
    return summarize_text(article_text)


def summarize_text(article_text):
    tokenized_sents = sentence_tokenization(article_text)
    tokenized_words = word_tokenization(article_text)
    word_frequencies = calculate_word_frequencies(tokenized_words)
    sent_scores = calculate_sent_scores(tokenized_sents, word_frequencies)
    word_frequencies = normalize_word_freq(word_frequencies)
    summarized_text = summarize(sent_scores)
    return summarized_text


# print(summarized_text)
# print("\n", '~' * 20, 'original article', '~' * 20, "\n")
# print(article_text)

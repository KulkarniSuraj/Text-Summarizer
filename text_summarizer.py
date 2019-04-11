# dependencies
from nltk.tokenize import word_tokenize, sent_tokenize, PunktSentenceTokenizer
from nltk.corpus import stopwords
import heapq
from bs4 import BeautifulSoup
import requests
import re

# getting the source from url
source = requests.get("https://en.wikipedia.org/wiki/Ketosis").text
soup = BeautifulSoup(source, 'lxml')

# getting list of all paragraphs on page
article = soup.find_all('p')

article_text = ""
for para in article:
    article_text += para.text

# removing brackets and replacing them with spaces
article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
# removing extra spaces and replacing them with single space
article_text = re.sub(r'\s+', ' ', article_text)
train_data = article_text

custom_sent_tokenizer = PunktSentenceTokenizer(train_text=train_data)

tokenized_sent = []
tokenized_words = []

# tokenize sentences
for line in custom_sent_tokenizer.tokenize(article_text):
    tokenized_sent.append(line)

# tokenize words
for word in word_tokenize(article_text):
    tokenized_words.append(word)

# stop words collection
stop_words = stopwords.words("english")

# finding the frequencies of words
word_frequencies = {}  
for word in tokenized_words:  
    if word not in stop_words:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1

# finding the maximum frequency
maximum_frequncy = max(word_frequencies.values())

# dividing each freq with max frequency
for word in word_frequencies.keys():  
    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

# calculating sentence scores
sent_scores = {}
for sent in tokenized_sent:
    for word in word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 30:
                if sent not in sent_scores.keys():
                    sent_scores[sent]  = word_frequencies[word]
                else:
                    sent_scores[sent] += word_frequencies[word]

# finding top sentences based on their frequencies
summary_sentences = heapq.nlargest(5, sent_scores, key = sent_scores.get)

# joining the sentences to create summary
summary = ' '.join(summary_sentences)  
print(summary) 

print('~' * 20, 'original article', '~' * 20, "\n")
print(article_text)



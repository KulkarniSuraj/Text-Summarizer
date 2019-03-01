from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import heapq


file = open('./texts/good articles in wikipedia.txt')
text = file.read()

tokenized_sent = []
tokenized_words = []

#tokenize sentences
for line in sent_tokenize(text):
    tokenized_sent.append(line)

# tokenize words
for word in word_tokenize(text):
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

# joining the sentences to crate summary
summary = ' '.join(summary_sentences)  
print(summary) 

print('~' * 20, 'original article', '~' * 20)
print(text)



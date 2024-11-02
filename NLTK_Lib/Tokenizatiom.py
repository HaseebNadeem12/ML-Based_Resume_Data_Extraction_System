import nltk

# nltk.download()

text = """hello, this is my second month of learning python,
 and I am enjoying this field very much"""

"""Tokenization"""
# from nltk.tokenize import word_tokenize, sent_tokenize
# print(word_tokenize(text))
# print(sent_tokenize(text))
# print(text.split(" "))

"""Removing stop words"""
from nltk.corpus import stopwords
stop_word = stopwords.words('english')       # Prints all the stop words with dublicate
# print(set(stopwords.words('english')))       # Print unique stop words

from nltk.tokenize import word_tokenize
tokenize_word_with_stop_words = word_tokenize(text)
print(tokenize_word_with_stop_words)

# To remove stop word from the text
tokenize_word_without_stop_words = ''

for word in tokenize_word_with_stop_words:
    if word not in stop_word:
        # tokenize_word_without_stop_words.append(word)
        tokenize_word_without_stop_words = tokenize_word_without_stop_words + " " + word

print(tokenize_word_without_stop_words)
# # to see the stop word in the text, which we excluded
# print(set(tokenize_word_with_stop_words) - set(tokenize_word_without_stop_words))

"""Stemming & Leminization"""
#both convert the words into their original form
#Leminizer is more accurate
#
# nltk.download('wordnet')
# from nltk.stem import PorterStemmer , WordNetLemmatizer
#
# demowords = ['playing','happiness','going','go','doing','do','jumpping','yes','no','having','had','programming','code','programmer']
#
#
# Lemitizer = WordNetLemmatizer()
# Stemmer = PorterStemmer()
#
# for word in demowords:
#     print(word,Stemmer.stem(word),Lemitizer.lemmatize(word,'v'))
#     # print(Lemitizer.lemmatize(word,'v')) # v->verb



"""POS Tagging"""
# # It tell that the word in a sentance is a noun, verb or mau be adjuctive etc
#
# text = "NLTK is a leading platform for building Python programs to work with human language data."
#
# from nltk.tokenize import word_tokenize
# # Tokenize the text into words
# tokens = word_tokenize(text)
# print(tokens)
#
# pos_tags = nltk.pos_tag(tokens)
# print(pos_tags)


# Removing stop words
from nltk.corpus import stopwords

stop_words = stopwords.words('english')

from nltk.tokenize import word_tokenize

tokenize_word = word_tokenize(text)

text_without_stop_word = " "
for word in tokenize_word:
    if word not in stop_words:
        text_without_stop_word = text_without_stop_word + " " + word






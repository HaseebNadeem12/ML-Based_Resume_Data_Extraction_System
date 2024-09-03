import nltk

# nltk.download()

text = """hello, this is my second month of learning python, and I am enjoying this field very much"""

"""Tokenization"""
# from nltk.tokenize import word_tokenize, sent_tokenize
# print(word_tokenize(text))
# print(sent_tokenize(text))

"""Removing stop words"""
# from nltk.corpus import stopwords
# stop_word = stopwords.words('english')       # Contain some dublicate words
# print(set(stopwords.words('english')))       # set always contain unique words
#
# from nltk.tokenize import word_tokenize,sent_tokenize
# tokenize_word = word_tokenize(text)
#
# # To remove stop word from the text
# without_stop_tokenize_word = []
#
# for word in tokenize_word:
#     if word not in stop_word:
#         without_stop_tokenize_word.append(word)
#
# print(without_stop_tokenize_word)
# # to see the stop word in the text, which we excluded
# print(set(tokenize_word) - set(without_stop_tokenize_word))

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








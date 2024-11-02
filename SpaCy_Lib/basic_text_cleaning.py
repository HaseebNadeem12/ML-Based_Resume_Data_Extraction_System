import spacy

nlp = spacy.load("en_core_web_sm")

# import spacy
#
# # Check the available models
# print(spacy.util.get_installed_models())

# # Attempt to load the small English model
# try:
#     nlp = spacy.load("en_core_web_sm")
#     print("Model loaded successfully!")
# except Exception as e:
#     print(f"Error loading model: {e}")

"""Tokenization"""
# Tokenization is the process of breaking down text into individual words or tokens.

# Example text
text = "SpaCy is an open-source software library for advanced Natural Language Processing."

# Process the text with spaCy
doc = nlp(text)

# Tokenize the text
tokens = [token.text for token in doc]
print(tokens)


"""Removing Stop Words"""

# # Removing stop words
# filtered_tokens = [token.text for token in doc if not token.is_stop]
# print(filtered_tokens)


"""Leminization"""
# #Lemmatization reduces words to their base or dictionary form, called a lemma. For example, "running" becomes "run".
# lemmas = [token.lemma_ for token in doc]
# print(lemmas)

"""Stemming"""
#spaCy does not support stemming out of the box because it prioritizes lemmatization, which is generally more accurate.


"""POS Tagging"""
# # POS tagging assigns parts of speech to each word in the text (e.g., noun, verb, adjective).
#
# pos_tags = [(token.text, token.pos_) for token in doc]
# print(pos_tags)


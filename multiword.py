# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 19:59:54 2023

@author: msi
"""

import stanza
stanza.download('en')
from stanza.server import CoreNLPClient

# Procedure to parse text using Stanford CoreNLP
def parse_with_nlp(text):
    with CoreNLPClient(annotators=['tokenize','ssplit','pos','lemma','ner', 'parse', 'depparse'],
                       timeout=30000,
                       memory='4G') as client:
        ann = client.annotate(text)
        return ann.sentence[0]

# Procedure to count the number of children of a token
def count_children(token, dependency_parse):
    return len([dep for dep in dependency_parse.dependency if dep.governor == token.tokenIndex])

# Main procedure
def mac(aspect_sentence, main_sentence):
    # Parse the main sentence
    main_doc = parse_with_nlp(main_sentence)

    # Parse the aspect sentence
    aspect_doc = parse_with_nlp(aspect_sentence)

    # Create an empty dictionary for relation counts
    relation_counts = {}

    # Count relations for each token in the main doc
    for token in main_doc.token:
        relation_counts[token.word] = count_children(token, main_doc.basicDependencies)

    # Initialize variables for tracking the maximum relation
    max_aspect_relation_word = None
    max_aspect_relation_count = 0

    # Find the aspect token with the maximum relation count
    for aspect_token in aspect_doc.token:
        if aspect_token.word in relation_counts and relation_counts[aspect_token.word] > max_aspect_relation_count:
            max_aspect_relation_word = aspect_token.word
            max_aspect_relation_count = relation_counts[aspect_token.word]

    # Construct the main sentence without the aspect word
    main_sentence_without_aspect_word = " ".join([token.word for token in main_doc.token if token.word != max_aspect_relation_word])

    # Return the max relation word and the updated sentence
    print(max_aspect_relation_word, main_sentence_without_aspect_word)
    return max_aspect_relation_word, main_sentence_without_aspect_word

# Example usage
aspect_sentence = "camera of laptop"
main_sentence = "the camera of laptop is very clear"
result = mac(aspect_sentence, main_sentence)
print(result)

from vectorizer import vectorizer
from okt import translate

def target_vector_maker(target):
    target_tokens = [translate.morphs(row) for row in target]

    target_vectorize = []

    for content in target_tokens:
        sentence = ''
        for word in content: sentence += ' ' + word
        target_vectorize.append(sentence)

    # print(target_vectorize)

    new_post_vec = vectorizer.fit_transform(target_vectorize)
    return new_post_vec
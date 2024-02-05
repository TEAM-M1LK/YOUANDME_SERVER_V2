from okt import translate
from vectorizer import vectorizer

def model_vector_maker(models):
    models_tokens = [translate.morphs(row) for row in models]
    models_vecotrize = []

    for content in models_tokens:
        sentence = ''
        for word in content: sentence += ' ' + word
        models_vecotrize.append(sentence)

    # print(models_vecotrize)
    result = vectorizer.fit_transform(models_vecotrize)
    result_len, _ = result.shape
    return result, result_len
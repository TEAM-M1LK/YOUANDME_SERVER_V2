from sklearn.feature_extraction.text import CountVectorizer
from app.utils.dist_raw import dist_raw
vectorizer = CountVectorizer(min_df=1)

models = ['좋아해', '사랑해', '너 닮았다', '딱 자긴데', '너무 좋아', '보고 싶어']
target = ['나 너 정말 좋아해, 하늘만큼 땅만큼. 평생 너만 사랑하고 싶어.']

# X = vectorizer.fit_transform(models)
# print(X.toarray().transpose())
# '''
# [[0 0 0 0 1 0]
#  [0 0 1 0 0 0]
#  [0 0 0 0 0 1]
#  [0 1 0 0 0 0]
#  [0 0 0 0 0 1]
#  [0 0 0 1 0 0]
#  [0 0 0 0 1 0]
#  [1 0 0 0 0 0]]
# '''

# target_vector = vectorizer.transform(target)
# print(target_vector.toarray())
# ''' [[0 0 0 0 1 0 0 1]] '''

# import scipy as sp

# best_dist = 65535
# best_i = None
# for i in range(len(models)):
#     vector = X.getrow(i)
#     d = dist_raw(vector, target_vector)

#     print("== Post %i with dist=%.2f : %s"%(i, d, models[i]))

#     if d < best_dist: best_dist, best_i = d, i

# print("== Best %i with dist=%.2f : %s"%(best_i, best_dist, models[best_i]))

from konlpy.tag import Okt

translate = Okt()

models_tokens = [translate.morphs(row) for row in models]
models_tokens

models_for_vectorize = []

for model in models_tokens:
    sentence = ''
    for word in model: sentence += ' ' + word
    models_for_vectorize.append(sentence)

X2 = vectorizer.fit_transform(models_for_vectorize)
X2.toarray().transpose()

targets_for_vectorize = []
target_tokens = [translate.morphs(row) for row in target]

for target_token in target_tokens:
    sentence = ''
    for word in target_token: sentence += ' ' + word
    targets_for_vectorize.append(sentence)

t_vec = vectorizer.transform(targets_for_vectorize)
print(X2.toarray())

best_dist = 65535
best_i = None

for i in range(len(models)):
    vec = X2.getrow(i)

    d = dist_raw(vec, t_vec)

    print("== Post %i with dist=%.2f : %s"%(i, d, models[i]))

    if d < best_dist: best_dist, best_i = d, i
print("== Best %i with dist=%.2f : %s"%(best_i, best_dist, models[best_i]))
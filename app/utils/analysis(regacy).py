from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from cleaner import cleaner
from dist_raw import dist_raw
import scipy as sp
from konlpy.tag import Okt
import pandas as pd
import numpy as np
from model_vector_maker import model_vector_maker
from target_vector_maker import target_vector_maker

df = pd.read_csv('app/ml/model.csv')
couple, some, friend, business = cleaner(df['연인']), cleaner(df['썸']), cleaner(df['친구']), cleaner(df['비즈니스'])

couple_vector, couple_len = model_vector_maker(couple)
some_vector = model_vector_maker(some)
friend_vector = model_vector_maker(friend)
business_vector = model_vector_maker(business)

def analysis(model, model_vector, model_len, target):
    target_vector = target_vector_maker(target)
    best_dist = 65535
    best_i = None

    for i in range(0, model_len):
        vector = model_vector.getrow(i)
        # if vector
        print("===============vector==============")
        print(np.array(vector.toarray()))
        print(vector.shape[1])
        print("===================================")
        print("==============target===============")
        s = vector.shape[1] - target_vector.shape[1]
        print(target_vector.shape[1])
        # a = target_vector.toarray() + [0 for _ in range(s)]
        print(np.array(target_vector.toarray()))
        print("===================================")
        print("==============minus================")
        # print(target_vector - vector)
        # try: print(target_vector - vector)
        # except: print("error")
        print("===================================")
        # print(post_vec.shape[0], end=' +++++ ')
        # print(target_vector.shape[0], end=' ||||| \n')
        d = 0
        # d = dist_raw(vector, target_vector)
        # try: d = dist_raw(vector, target_vector)
        # except: pass
        # d = 0

        print("== Post %i with dist=%.6f : %s"%(i, d, model[i]))

        if d < best_dist:
            best_dist = d
            best_i = i

    print("==Best %i with Dist = %.6f : %s" %(best_i, best_dist, model[best_i]))

    print('-->', target)
    print('----->', model[best_i])


analysis(couple, couple_vector, couple_len, ["너가 너무 좋아"])
# analysis(some, some_vector, ["나는 좋아!"])
# analysis(friend, friend_vector, ["미쳤다"])
# analysis(business, business_vector, ["알겠습니다"])
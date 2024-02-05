from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from cleaner import cleaner
from dist_raw import dist_raw
import scipy as sp
from konlpy.tag import Okt
import pandas as pd
from model_vector_maker import model_vector_maker
from target_vector_maker import target_vector_maker

df = pd.read_csv('app/ml/model.csv')
couple, some, friend, business = cleaner(df['연인']), cleaner(df['썸']), cleaner(df['친구']), cleaner(df['비즈니스'])

couple_vector = model_vector_maker(couple)
some_vector = model_vector_maker(some)
friend_vector = model_vector_maker(friend)
business_vector = model_vector_maker(business)

def analysis(model, model_vector, target):
    target_vector = target_vector_maker(target)
    best_dist = 65535
    best_i = None

    for i in range(0, len(couple)):
        post_vec = model_vector.getrow(i)

        d = dist_raw(post_vec, target_vector)

        print("== Post %i with dist=%.6f : %s"%(i, d, model[i]))

        if d < best_dist:
            best_dist = d
            best_i = i

    print("==Best %i with Dist = %.6f : %s" %(best_i, best_dist, model[best_i]))

    print('-->', target)
    print('----->', model[best_i])


analysis(couple, couple_vector, ["니애미"])
# analysis(some, some_vector, ["나는 좋아!"])
# analysis(friend, friend_vector, ["미친"])
# analysis(business, business_vector, ["알겠습니다"])
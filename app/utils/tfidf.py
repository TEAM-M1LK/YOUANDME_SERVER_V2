import scipy as sp

def tfidf(t, d, D):
    tf = float(d.count(t)) / sum(d.count(w) for w in set(d))
    idf = sp.log(float(len(D)) / len([doc for doc in D if t in doc]))
    return tf, idf
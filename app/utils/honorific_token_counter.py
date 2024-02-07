import re
from konlpy.tag import Komoran

komoran = Komoran()
hon_tokens = [word.rstrip('\n') for word in open('app/ml/' + 'komoran_honorific_token.txt', 'r',encoding='utf-8')]

def honorific_token_counter(text):
    cnt = 0
    try:
        for i in komoran.pos(text):
            if str(i) in hon_tokens: cnt += 1
        return cnt
    except: return 0
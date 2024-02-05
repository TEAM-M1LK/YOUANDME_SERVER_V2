from sklearn.feature_extraction.text import TfidfVectorizer
from konlpy.tag import Okt
import time
import pandas as pd
from kss import split_sentences
from app.utils.cleaner import cleaner
from app.utils.dist_raw import dist_raw
from app.utils.honorific_token_counter import honorific_token_counter
from app.utils.percentage_calculator import percentage_calculator

df = pd.read_csv("app/ml/model.csv")
translate = Okt()

def honorific_analysis(target):
    target = ' '.join(target)
    tokens = honorific_token_counter(target)
    sentence = len(split_sentences(target, backend='pecab'))
    if not sentence: return [False, 1]
    average = 1 - tokens/sentence

    if average < 0: average = 0 
    if tokens > sentence//2: return [True, average]
    return [False, average]

    
def analysis(target, models):
    start_time = time.time()
    # TF-IDF vectorizer initialization
    vectorizer = TfidfVectorizer(min_df=1)

    # Sample models and target sentences
    # models = ['좋아해', '사랑해', '너 닮았다', '딱 자긴데', '너무 좋아', '보고 싶어']
    # models = cleaner(df['비즈니스'])
    # target = ['나 너 정말 좋아해, 하늘만큼 땅만큼. 평생 너만 사랑하고 싶어.']

    # Tokenization of models and target
    models_tokens = [translate.morphs(row) for row in models]
    models_for_vectorize = [' '.join(tokens) for tokens in models_tokens]

    # Vectorize models
    X2 = vectorizer.fit_transform(models_for_vectorize)

    # Tokenization of the target sentence
    target_tokens = [translate.morphs(row) for row in target]
    targets_for_vectorize = [' '.join(tokens) for tokens in target_tokens]

    # Vectorize the target sentence
    t_vec = vectorizer.transform(targets_for_vectorize)

    # Start time measurement
    s = []
    # Perform the distance calculation
    best_dist = 65535
    best_i = None
    for i in range(len(models)):
        vec = X2.getrow(i)
        d = dist_raw(vec, t_vec)
        print("== Post %i with dist=%.2f : %s"%(i, d, models[i]))
        if d < best_dist:
            best_dist, best_i = d, i
        
        s.append([d, i])

    # End time measurement
    end_time = time.time()

    # Print the best result
    print("== Best %i with dist=%.6f : %s"%(best_i, best_dist, models[best_i]))

    # Print the time taken for execution
    s = sorted(s, key=lambda x: x[0])
    print(s)
    value = [row[0] for row in s]
    clean_value = [number for number in value if number != 1]
    print(sum(clean_value))
    print("================================")
    print("Execution Time: %.6f seconds" % (end_time - start_time))

    return [clean_value, end_time - start_time]

def start_analysis(target, name, length):
    result = {}
    isBusiness, value = honorific_analysis(target)
    analysis_time = 0
    t1 = 0
    if isBusiness: result['business'] = [value]
    else: result['business'],t1 = analysis(target, cleaner(df['비즈니스']))

    result['some'],t2 = analysis(target, cleaner(df['썸']))
    result['friend'],t3 = analysis(target, cleaner(df['친구']))

    coup, t4 = analysis(target, cleaner(df['연인']))
    if len(coup): result['couple'] = [coup[0] - 0.6]
    else: result['couple'] =[1.2]
    analysis_time = t1 + t2 + t3 + t4
    return {
        "name": name,
        "final_relation": min(result, key=result.get),
        "analysis_time": analysis_time,
        "conversation_count": length,
        "result": percentage_calculator(result),
    }

# 연인
# run(['사랑해, 너무 많이 보고 싶어. 죽었다 깨어나도 난 네 연인이 되고 싶은걸. 평생 너의 곁에 누워 사랑스러운 눈빛으로 너를 바라보다 잠드는 그런 삶을 살아가고 싶어. 우리 같이 살자. 내가 꼭 잘해줄게.'])
# # 비즈니스 1.32, 썸 1.19, 친구 0.9, 연인 0.86

# # 비즈니스
# run(['안녕하세요. 보고서 제출 건과 관련하여 메일 드립니다. 금일 오후 3시에 있을 회의에 대한 보고서를 점심 식사 시간 전까지 제게 보고주시길 바랍니다. 답장 기다리겠습니다. 감사합니다.'])
# # 비즈니스 0.19, 썸 1.34, 친구 0.99, 연인 1

# # 썸
# run(['너랑 뭘 하든 다 좋아 ㅎㅎㅎ 너는 뭐 좋아해? 같이 못 노는게 완죤 아쉽다 그치만.. 그래두 나는 괜찮아 ㅋㅋㅋ 그럴 수도 있지'])
# # 비즈니스 1, 썸 1.05, 친구 1.2, 연인 1.202

# # 친구
# run(['ㅋㅋㅋ 약빤거 맞는거같노'])
# # 비즈니스 1, 썸 1.26, 친구 1.146, 연인 1

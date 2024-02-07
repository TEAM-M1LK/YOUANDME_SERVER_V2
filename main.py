from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import pandas as pd
import difflib
from typing import List
from datetime import date
from pydantic import BaseModel
import time
from app.utils.time_checker import time_checker
from konlpy.tag import Okt
translate = Okt()

app = FastAPI(openapi_prefix="/server")

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Contents(BaseModel):
    date: str
    sender: str
    content: str

class Request(BaseModel):
    my_name: str
    your_name: str
    guess_relation: str
    contents: List[Contents]

@app.post("/talk/analysis")
def talk_analysis(request: Request):
    # print(request.contents)
    return run(request)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


df = pd.read_csv('./app/ml/model.csv')

def cleaner(dataframe):
    return dataframe.dropna().astype(str).tolist()

def run(request: Request):
    start_time = time.time()
    client_conversation = []
    requester_conversation = []

    # for talk in request.contents:
    #     if talk.sender == request.my_name: 
    #         client_conversation.append(talk.content)
    #     elif talk.sender == request.your_name: requester_conversation.append(talk.content)

    # print(client_conversation)
    # print(requester_conversation)
    # client_result = start_analysis([' '.join(client_conversation)], request.my_name, len(client_conversation))
    # requester_result = start_analysis([' '.join(requester_conversation)], request.your_name, len(requester_conversation))

    times = time_checker(request.contents, request.my_name, request.your_name)
    # return {
    #     "my": client_result, 
    #     "you": requester_result,
    #     "time": times
    # }

    lover_conversation = []
    some_conversation = []
    friend_conversation = []
    business_conversation = []

    for talk in request.contents:
        if talk.sender == request.my_name: 
            s = bytes(talk.content, 'utf-8')
            client_conversation.append(s)
        elif talk.sender == request.your_name: 
            s = bytes(talk.content, 'utf-8')
            requester_conversation.append(s)

    print(client_conversation)
    print(requester_conversation)

    client = {'lover': 0, 'some': 0, 'friend': 0, 'business': 0}
    requester = {'lover': 0, 'some': 0, 'friend': 0, 'business': 0}
    
    for talk in cleaner(df['연인']):
        model = bytes(talk, 'utf-8')
        lover_conversation.append(model)

    for talk in cleaner(df['썸']):
        model = bytes(talk, 'utf-8')
        some_conversation.append(model)
    
    for talk in cleaner(df['친구']):
        model = bytes(talk, 'utf-8')
        friend_conversation.append(model)

    for talk in cleaner(df['비즈니스']):
        model = bytes(talk, 'utf-8')
        business_conversation.append(model)
    
    print(lover_conversation)

    client['lover'] += difflib.SequenceMatcher(None, lover_conversation, client_conversation).ratio()
    client['some'] += difflib.SequenceMatcher(None, some_conversation, client_conversation).ratio()
    client['friend'] += difflib.SequenceMatcher(None, friend_conversation, client_conversation).ratio()
    client['business'] += difflib.SequenceMatcher(None, business_conversation, client_conversation).ratio()

    requester['lover'] += difflib.SequenceMatcher(None, lover_conversation, requester_conversation).ratio()
    requester['some'] += difflib.SequenceMatcher(None, some_conversation, requester_conversation).ratio()
    requester['friend'] += difflib.SequenceMatcher(None, friend_conversation, requester_conversation).ratio()
    requester['business'] += difflib.SequenceMatcher(None, business_conversation, requester_conversation).ratio()

    def convert_to_percentage(dictionary):
        total = sum(dictionary.values())
        if total == 0: return dictionary
        percentage_dict = {key: (value / total * 100) for key, value in dictionary.items()}
        return percentage_dict
    print(client)

    more_faster_replier = ''
    more_alot_chatter = ''

    my_reply_time = abs(times['my_reply_time'].total_seconds()) / len(client_conversation)
    your_reply_time = abs(times['you_reply_time'].total_seconds()) / len(requester_conversation)
    if my_reply_time > your_reply_time: more_faster_replier = request.my_name
    elif my_reply_time == your_reply_time: more_faster_replier = 'same'
    else: more_faster_replier = request.your_name

    if len(client_conversation) > len(requester_conversation): more_alot_chatter = request.my_name
    elif len(client_conversation) == len(requester_conversation): more_alot_chatter = 'same'
    else: more_alot_chatter = request.your_name

    end_time = time.time()
    return {
        "analysis_time": end_time - start_time,
        "more_faster_replier": more_faster_replier,
        "more_alot_chatter": more_alot_chatter,
        "my": {
            "name": request.my_name,
            "final_relation": max(client, key=client.get),
            "result": convert_to_percentage(client),
            "conversation_count": len(client_conversation),
            "reply_time": abs(times['my_reply_time'].total_seconds()),
            "reply_time_average": my_reply_time
        }, 
        "you": {
            "name": request.your_name,
            "final_relation": max(requester, key=requester.get),
            "result": convert_to_percentage(requester),
            "conversation_count": len(requester_conversation),
            "reply_time": abs(times['you_reply_time'].total_seconds()),
            "reply_time_average": your_reply_time
        }, 
    }
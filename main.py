from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import pandas as pd
import difflib
from typing import List
from datetime import date
from pydantic import BaseModel

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
    print(request.contents)
    return run(request)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


df = pd.read_csv('./app/ml/model.csv')

def cleaner(dataframe):
    return dataframe.dropna().astype(str).tolist()

def run(request: Request):
    lover, some, friend, business = df['연인'], df['썸'], df['친구'], df['비즈니스']
    
    client = { '연인': 0, '썸': 0, '친구': 0, '비즈니스': 0 }
    requester = { '연인': 0, '썸': 0, '친구': 0, '비즈니스': 0 }
    
    client_conversation = []
    requester_conversation = []
    friend_conversation = []
    business_conversation = []

    lover_conversation = []
    some_conversation = []

    for talk in request.contents:
        model = bytes(talk.content, 'utf-8')

        if talk.sender == request.my_name: client_conversation.append(model)
        elif talk.sender == request.your_name: requester_conversation.append(model)

    for talk in cleaner(lover):
        model = bytes(talk, 'utf-8')
        lover_conversation.append(model)

    for talk in cleaner(some):
        model = bytes(talk, 'utf-8')
        some_conversation.append(model)
    
    for talk in cleaner(friend):
        model = bytes(talk, 'utf-8')
        friend_conversation.append(model)

    for talk in cleaner(business):
        model = bytes(talk, 'utf-8')
        business_conversation.append(model)

    client['연인'] += difflib.SequenceMatcher(None, lover_conversation, client_conversation).ratio()
    client['썸'] += difflib.SequenceMatcher(None, some_conversation, client_conversation).ratio()
    client['친구'] += difflib.SequenceMatcher(None, friend_conversation, client_conversation).ratio()
    client['비즈니스'] += difflib.SequenceMatcher(None, business_conversation, client_conversation).ratio()

    requester['연인'] += difflib.SequenceMatcher(None, lover_conversation, requester_conversation).ratio()
    requester['썸'] += difflib.SequenceMatcher(None, some_conversation, requester_conversation).ratio()
    requester['친구'] += difflib.SequenceMatcher(None, friend_conversation, requester_conversation).ratio()
    requester['비즈니스'] += difflib.SequenceMatcher(None, business_conversation, requester_conversation).ratio()

    return {"client": client, "requester": requester}
from modeling import summary_chatbot
import json
from modeling import query_id
import time
json_path="C:/Users/user/Desktop/final_summary/card_data_benefits.json"
with open(json_path,"r",encoding="utf-8") as file:
    card_name=json.load(file)



# cache에 json_data 저장하기 (key는 query, value는 json_data)


#cache에 해당 query가 있음 return, 아니면 새로 생성
def generate_json(query):
    cache={}
    if query in cache:
        return cache[query]
    else:
        llm_outputs=summary_chatbot(query)["result"]
        json_data=json.loads(llm_outputs)
        time.sleep(1)
        cache[query]=json_data
        return json_data


# query를 통해 json 데이터 생성하거나 불러오는 함수

# json_data return하는 함수
def input(query):
    return generate_json(query)



def cardId_data(json_data):
    cardid = [item["cardId"] for item in json_data]
    return cardid

def categoryid_data(json_data):
    categoryid = [item["categoryID"] for item in json_data]
    return categoryid

def benefitTitle_data(json_data):
    benefittitle = [item["benefitTitle"] for item in json_data]
    return benefittitle

def description_data(json_data):
    description = [item["description"] for item in json_data]

    return description



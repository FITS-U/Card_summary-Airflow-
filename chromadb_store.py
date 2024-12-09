from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import json
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
os.environ["OPENAI_API_KEY"]='SECRET-KEY'

# Chromadb 로드
file_path='C:/Users/user/Desktop/final_summary/card_data_benefits.json'
#파일 읽기
with open(file_path,'r',encoding='utf-8') as file:
    card_data=json.load(file)
    



    

#chromadb 구축, chronmadb 초기화
sum_db_path='C:/Users/user/Desktop/final_summary/chromadb'
embeddings=OpenAIEmbeddings()
vectorstore=Chroma(persist_directory=sum_db_path,embedding_function=embeddings)

for index,card in enumerate(card_data):
    document=f"cardId:{card['cardId']} \n Card Name:{card['Card Name']} \n Benefits:{(card['Benefits'])}"
    metadata={"cardId":card['cardId'],"Card Name":card['Card Name']}

    #벡터스토어에 저장 (새로 임베딩)
    vectorstore.add_texts([document],metadatas=[metadata])

# Benefits 필드를 JSON 형식으로 변환
# for index, card in card_data.items():
#     card_data[index]["Benefits"]=ast.literal_eval(card["Benefits"])

#저장
print("Chromadb 저장")



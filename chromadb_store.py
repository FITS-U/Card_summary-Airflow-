from dotenv import load_dotenv
load_dotenv()
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import json
from date_file import card_data_benefits
from date_file import db_path_card_summary
# Chromadb 로드
#파일 읽기
with open(card_data_benefits(),'r',encoding='utf-8') as file:
    card_data=json.load(file)



#chromadb 구축, chronmadb 초기화
sum_db_path=db_path_card_summary()

embeddings=OpenAIEmbeddings()
vectorstore=Chroma(persist_directory=sum_db_path,embedding_function=embeddings)

for index,card in enumerate(card_data):
    document=f"cardId:{card['cardId']} \n Card Name:{card['Card Name']} \n Benefits:{(card['Benefits'])}"
    metadata={"cardId":card['cardId'],"Card Name":card['Card Name']}

    #벡터스토어에 저장 (새로 임베딩)
    vectorstore.add_texts([document],metadatas=[metadata])

#저장
print("Chromadb 저장")



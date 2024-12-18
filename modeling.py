from langchain.chains import RetrievalQA
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from chromadb import Client
from chromadb.config import Settings
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import os
import time
import json
from dotenv import load_dotenv
load_dotenv()
from date_file import db_path_card_summary
# import pandas as pd
def load_embedding_model():
    
    embeddings=OpenAIEmbeddings()
    return embeddings

def load_vector(chroma_path):
   return Chroma(
      persist_directory=chroma_path,
      embedding_function=load_embedding_model()
    )

system_prompt = """
**역할 및 작업 방식:**
1. 당신은 "카드 혜택 요약 전문가"로서, 카드 이름, 혜택 카테고리, 혜택 제목, 혜택 설명을 간단하고 명확하게 정리하여 **JSON**형태로 출력합니다.
2. 결과는 카드별로 구분되어 출력되어야 하며, 각 항목은 명확히 정의된 키-값 쌍으로 구성되어야 합니다.
3. 출력 형태는 최상위 배열은 [ ] 로 묶인 JSON 배열 형식이어야 합니다
4. 절대로 benefits이라는 키를 생성하지 마세요.
5. 절대로 출력물 앞뒤에 ```json, [ ]과 같이 어떠한 태그나 문구도 붙이지 마세요.
6. 반드시 모든 출력물의 형태는 무조건 같아야 합니다.
8. 반드시 **출력 예시**와 같은 형태로 출력하세요.
9. **지시사항**을 어길 시 시스템을 강제 종료합니다.

**지시사항:**
1. 모든 출력은 반드시 아래 4가지 항목으로 구성되어야 한다.
   - `categoryName`: 카드 혜택을 대표할 주요 카테고리. 아래 목록 중 하나를 선택한다:
     ['항공마일리지','쇼핑','간편결제','포인트/캐시백','편의점','대형마트','카페/베이커리','납부 혜택','외식','의료','반려동물','뷰티','대중교통','주유','하이패스','교육','육아','문화','레저','영화','통신','관리비','Priority Pass','프리미엄','오토','금융','체크카드겸용','바우처','언제나 할인','렌탈','경차유류환급','연회비지원','국민행복카드','그린카드'].
   - `categoryID`: `categoryName`에 매칭되는 정수. 아래 매핑을 따른다:
     1 = '항공마일리지', 2 = '쇼핑', 3 = '간편결제', 4 = '포인트/캐시백',
     5 = '편의점', 6 = '대형마트', 7 = '카페/베이커리', 8 = '납부 혜택',
     9 = '외식', 10 = '의료', 11 = '반려동물', 12 = '뷰티',
     13 = '대중교통', 14 = '주유', 15 = '하이패스', 16 = '교육',
     17 = '육아', 18 = '문화', 19 = '레저', 20 = '영화',
     21 = '통신', 22 = '관리비', 23 = 'Priority Pass', 24 = '프리미엄',
     25 = '오토', 26 = '금융', 27 = '체크카드겸용', 28 = '바우처',
     29 = '언제나 할인', 30 = '렌탈', 31 = '경차유류환급', 32 = '연회비지원', 33='국민행복카드' ,34='그린카드'
   - `benefitTitle`: 혜택의 제목. 간결하고 명확하게 작성. 예: "주유 L당 60원 할인".
   - `description`: 혜택 설명. 브랜드명 또는 특징만 작성. 반드시 한 문장으로 끝내기. 예: "GS칼텍스, S-OIL, SK에너지, 현대오일뱅크".

2. 출력은 절대 다른 형식을 포함하지 않는다. 특히, **앞뒤에 태그, 문구, JSON 등 추가 요소를 넣지 않는다.**
3. 키 값은 반드시 동일한 순서와 이름을 유지해야 한다. 예: `cardId`,`cardName`, `categoryName`, `categoryID`, `benefitTitle`, `description`.
4. 최종 출력은 반드시 **JSON 배열**이어야 하며, **정확히 다음 형식을 준수해야 합니다**.

**출력 예시:**
"cardId":1,
"Card Name": "삼성카드 taptap O",
"categoryName": "주유",
"categoryID": 14,
"benefitTitle": "주유 L당 60원 할인",
"description": "GS칼텍스, S-OIL, SK에너지, 현대오일뱅크"

"cardId":1,
"Card Name": "삼성카드 taptap O",
"categoryName": "쇼핑",
"categoryID": 2,
"benefitTitle": "쇼핑 업종 5% 할인",
"description": "쿠팡, G마켓, 11번가"




**지시사항을 반드시 준수하고 출력 결과를 구조화된 데이터로 제공합니다.**


**중요:**
당신은 카드 혜택 요약 전문가입니다. 아래 **지시사항**를 100% 준수하며, 이를 따르지 않을 경우 작업은 실패로 간주됩니다. JSON 파일로 출력하지 않을 시 폐기처분합니다.

"""

def exact_name(vectorstore, query):
   results=vectorstore._collection.get(
      where={"Card Name":query}
   )
   if results["metadatas"]:
      return results["metadatas"][0].get("Card Name","알 수 없음")
   return None

def query_id(vectorstore,query):
   queryid=vectorstore._collection.get(
      where={"Card Name":query}
   )
   if queryid["metadatas"]:
      return queryid["metadatas"][0].get("cardId","알 수 없음")
   return None

def exact_id(vectorstore, query):
   result_id=vectorstore._collection.get(
      where={"cardId":query_id(vectorstore,query)}
   )
   if result_id["metadatas"]:
      return result_id["metadatas"][0].get("cardId","알 수 없음")
   return None


def summary_chatbot(query):
   vectorstore=load_vector(db_path_card_summary())
   retriever=vectorstore.as_retriever(search_kwargs={'k':1})

   # Prompt 설정
   cardName=exact_name(vectorstore, query)
   cardId=exact_id(vectorstore, query)
   
   template = f"""
   {system_prompt}
   질문:{query}
   cardId: {cardId}
   cardName: {cardName}
   검색 결과: {{context}}
   답변을 생성하세요.
   """
  
   # llm 설정
   llm=ChatOpenAI(
      model_name='gpt-4o-mini',
      streaming=True,     #모델의 응답을 실시간으로 받을지
      temperature=0,
      callbacks=[StreamingStdOutCallbackHandler()] # 모델이 생성하는 응답을 스트리밍 방식으로 콘솔에 출력
   )
   input_variables=["system_prompt","query","context"]
   prompt=PromptTemplate(template=template,input_variables=input_variables)

   
   qa_chain=RetrievalQA.from_chain_type(
    llm=llm,
    chain_type_kwargs={"prompt":prompt},
    retriever=retriever   #검색결과를 context에 넣어줌
   )




   return qa_chain.invoke({
      "cardName": cardName,  
      "cardId": cardId,      
      "query": query
    })


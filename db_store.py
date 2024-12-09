import psycopg2
import json
from data_for_pro import cardId_data
from data_for_pro import categoryid_data
from data_for_pro import benefitTitle_data
from data_for_pro import description_data
from data_for_pro import input
class Database():
    def __init__(self):
        #데이터베이스 연결
        self.db=psycopg2.connect(
            host='56.155.9.34',
            user='postgres',
            password='0714',
            port=5432,
            database='card'
            )
        # 클라이언트 인코딩 설정
        # self.db.set_client_encoding('UTF-8')
        self.cursor=self.db.cursor()
    
    def __del__(self):
        self.db.close()
        self.cursor.close()
        

    def execute(self,query,args={}):
        self.cursor.execute(query,args)
        #결과 가져오기
        # self.cursor.fetchall()
        

    def commit(self):
        self.db.commit()


mydb=Database()


insert_query="""
INSERT INTO benefit (card_id, category_id, benefittitle, description)
VALUES (%s, %s, %s, %s)
"""

json_path="C:/Users/user/Desktop/final_summary/card_data_benefits.json"
with open(json_path,"r",encoding="utf-8") as file:
    card_name=json.load(file)

len_card=len(card_name)
query_list=[]

#0부터 312까지 카드 이름 추출
for i in range(len_card):
    query=card_name[i]["Card Name"]
    query_list.append(query)
    
        

print(query_list)

for query in query_list:
    json_data=input(query)
    cardid_list=cardId_data(json_data)
    categoryid_list=categoryid_data(json_data)
    benefitTitle_list=benefitTitle_data(json_data)
    description_list=description_data(json_data)

    for j in range(len(json_data)):
        card_id=cardid_list[j]
        category_id=categoryid_list[j]
        benefittitle=benefitTitle_list[j]
        description=description_list[j]

        mydb.execute(insert_query,(card_id,category_id,benefittitle,description))
        mydb.commit()
        print("complete")



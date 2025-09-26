from datetime import datetime
import os




def cardinfo_json():
    date=datetime.now().strftime("%Y%m%d")
    return f"/home/ubuntu/card_recommendation/data/cardinfo_{date}.json"

def card_data_benefits():
    date=datetime.now().strftime("%Y%m%d")
    return f"/home/ubuntu/card_recommendation/data/card_data_benefits_{date}.json"


# db 파일 생성
def db_path_card_recommendation():
    date=datetime.now().strftime("%Y%m%d")
    return f"/home/ubuntu/card_recommendation/chromaDB_{date}"

def db_path_card_summary():
    date=datetime.now().strftime("%Y%m%d")
    return f"/home/ubuntu/card_recommendation/for_git_card_summary/chromadb_{date}"
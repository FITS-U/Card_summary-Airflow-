# Card_summary-Airflow-

# 💳 카드 혜택 요약 및 맞춤형 카드 추천 파이프라인
여러 카드사에 흩어져 있는 나의 카드 혜택을 한곳에 모아 요약하고, 소비 패턴에 맞춰 최적의 카드를 추천해주는 자동화 데이터 파이프라인입니다.

## 📖 프로젝트 소개
수많은 신용카드의 복잡한 혜택 정보를 일일이 파악하기는 어렵습니다. 이 프로젝트는 웹 크롤링으로 최신 카드 정보를 수집하고, **LLM(대규모 언어 모델)**을 활용하여 핵심 혜택을 구조화된 데이터로 요약합니다. 이 모든 과정을 Apache Airflow를 통해 주기적으로 자동화하여, 사용자가 언제나 최신 정보를 바탕으로 가장 적합한 카드를 추천받을 수 있도록 설계되었습니다.

### ✨ 주요 기능
- 웹 크롤링 자동화: Selenium을 사용하여 카드 정보 웹사이트에서 최신 카드 데이터(혜택, 연회비, 전월 실적 등)를 주기적으로 수집합니다.

- LLM 기반 혜택 요약 (RAG): LangChain과 OpenAI (GPT) 모델을 활용하여 비정형 텍스트로 된 카드 혜택 설명을 핵심만 담은 구조화된 JSON 데이터로 변환합니다.

- 벡터 데이터베이스 활용: ChromaDB를 벡터 저장소로 사용하여 카드 혜택 정보에 대한 의미 기반 검색 및 RAG 파이프라인의 기반을 마련합니다.

- 데이터 파이프라인 오케스트레이션: Apache Airflow를 사용하여 데이터 수집, 처리, 임베딩, 모델 추론, DB 저장까지의 전 과정을 자동화하고 모니터링합니다.

- 안정적인 데이터 관리: 최종적으로 처리된 구조화 데이터를 PostgreSQL 데이터베이스에 저장하여 안정적으로 관리하고 쉽게 조회할 수 있도록 합니다.

### 🛠️ 기술 스택
**Orchestration** : Apache Airflow

**Crawling**: Selenium

**LLM/AI**: LangChain, OpenAI (GPT-4o-mini)

**Vector DB**: ChromaDB

**Database**: PostgreSQL

**Libraries**: psycopg2, dotenv, json, datetime

-------
본 프로젝트는 다음과 같은 **파이프라인**을 가집니다.

`데이터 수집 (Crawling) ➡️ 벡터 임베딩 및 저장 ➡️ LLM 기반 혜택 요약 ➡️ 최종 데이터 DB 저장`

1. 데이터 수집 (`final_dags.py` -> `data_crawling.py`):

  final_project_dag가 실행되면, 가장 먼저 data_crawling.py 스크립트를 실행하여 웹에서 카드 정보를 크롤링하고 JSON 파일로 저장합니다.

2. 혜택 요약 및 저장 DAG 트리거 (`final_dags.py` -> `card_summary_dags.py`):

  크롤링이 완료되면 final_project_dag는 TriggerDagRunOperator를 통해 card_summary_dag를 실행시킵니다.

3. RAG 파이프라인 및 DB 저장 (`card_summary_dags.py`):

  Vector Store 생성 (`chromadb_store.py`): 크롤링된 카드 혜택 데이터를 OpenAI 임베딩 모델을 통해 벡터로 변환하고 ChromaDB에 저장합니다.

4. LLM 추론 (`modeling.py`, `data_for_pro.py`): 저장된 벡터를 기반으로 RAG 파이프라인을 구성합니다. 각 카드에 대해 LLM(GPT)이 핵심 혜택을 추출하여 구조화된 JSON으로 생성합니다.

  PostgreSQL 저장 (`db_store.py`): LLM이 생성한 최종 JSON 데이터를 PostgreSQL 데이터베이스에 삽입하여 영구적으로 저장합니다.

## 📂 프로젝트 구조
```
Card_summary-Airflow-/
├── dags/
│   ├── final_dags.py             # 메인 DAG
│   └── card_summary_dags.py      # 혜택 요약 및 저장 서브 DAG
│
├── scripts/
│   ├── data_crawling.py          # Selenium 웹 크롤러
│   ├── modeling.py               # LangChain, OpenAI 모델링 (RAG)
│   ├── chromadb_store.py         # ChromaDB 벡터 저장소 생성
│   ├── db_store.py               # PostgreSQL 데이터 저장
│   ├── data_for_pro.py           # 데이터 처리 유틸리티
│   └── date_file.py              # 날짜 기반 파일 경로 생성 유틸리티
│
├── data/
│   ├── card_data_benefits.json   # 크롤링된 카드 혜택 원본 데이터
│   ├── CardInfo.csv              # 크롤링된 카드 기본 정보
│   ├── CardImage.csv             # 크롤링된 카드 이미지 URL
│   └── chroma.sqlite3            # ChromaDB 데이터 파일
│
└── requirements.txt              # 파이썬 패키지 목록
```

   

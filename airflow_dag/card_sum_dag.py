from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
with DAG(
    dag_id="card_summary_dag",
    start_date=datetime(2025,1,1),
    schedule_interval='@monthly',
    catchup=True
) as dag:
    start=BashOperator(
        task_id="start",
        bash_command='echo "start"'
    )
    
    s1=BashOperator(
        task_id="card_sum_chroma",
        bash_command="python /home/ubuntu/card_recommendation/for_git_card_summary/card_sum_chromadb_store.py"
    )
    
    s2=BashOperator(
        task_id="card_sum_data_for",
        bash_command="python /home/ubuntu/card_recommendation/for_git_card_summary/card_sum_data_for_pro.py"
    )

    s3=BashOperator(
        task_id="card_sum_db_upload",
        bash_command="python /home/ubuntu/card_recommendation/for_git_card_summary/card_sum_db_store.py"
    )

    end=BashOperator(
        task_id="end",
        bash_command='echo "end"'
    )

    start>>s1>>s2>>s3>>end
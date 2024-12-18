from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.trigger_rule import TriggerRule

with DAG(
    dag_id="final_project_dag",
    start_date=datetime(2025,1,1),
    schedule_interval='@monthly',
    catchup=True
) as dag:
    
    start= BashOperator(
        task_id='start',
        bash_command='echo "start"'
    )   
    

    t1=BashOperator(
        task_id="data_crawling",
        bash_command="python /home/ubuntu/card_recommendation/datacrawling.py"
    )

    call_trigger = TriggerDagRunOperator(
        task_id='trigger',
        trigger_dag_id='card_summary_dag',  # 호출할 DAG ID
        reset_dag_run=False,
        wait_for_completion=False,
        poke_interval=60,
        allowed_states=["success"],
        failed_states=["failed"]
    )
    
    #실패했을 때도 continue
    next_trigger= BashOperator(
        task_id="continue_after_trigger",
        bash_command='echo "Continue DAG"',
        trigger_rule=TriggerRule.ALL_DONE
    )

    t2=BashOperator(
        task_id="embedding",
        bash_command="python /home/ubuntu/card_recommendation/embedding.py"
    )

    t3=BashOperator(
        task_id="postgre_db_attack",
        bash_command="python /home/ubuntu/card_recommendation/postgrattack.py"
    )


    complete=BashOperator(
        task_id="complete",
        bash_command='echo "complete"'
    )

    start>>t1>>call_trigger>>next_trigger>>t2>>t3>>complete
    
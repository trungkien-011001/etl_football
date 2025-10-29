from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="football_etl_test",
    start_date=datetime(2025,1,1),
    schedule_interval=None,
    catchup=False
) as dag:
    

    etl_test = BashOperator(
        task_id='run_etl_test_script',
        bash_command='python /opt/airflow/etl/etl_test.py'
    )

    etl_test
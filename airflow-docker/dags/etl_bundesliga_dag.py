from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="etl_bundesliga",
    start_date=datetime(2025,1,1),
    schedule_interval=None,
    catchup=False
) as dag:

    bundesliga_etl = BashOperator(
        task_id='run_etl_bundesliga_script',
        bash_command='python /opt/airflow/etl/etl_bundesliga.py'
    )
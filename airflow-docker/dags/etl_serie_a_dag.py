from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="etl_serie_a",
    start_date=datetime(2025,1,1),
    schedule_interval=None,
    catchup=False
) as dag:

    serie_a_etl = BashOperator(
        task_id='run_etl_serie_a_script',
        bash_command='python /opt/airflow/etl/etl_serie_a.py'
    )
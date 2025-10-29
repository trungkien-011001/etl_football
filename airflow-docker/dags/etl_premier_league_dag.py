from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="etl_premier_league",
    start_date=datetime(2025,1,1),
    schedule_interval=None,
    catchup=False
) as dag:

    premier_league_etl = BashOperator(
        task_id='run_etl_premier_league_script',
        bash_command='python /opt/airflow/etl/etl_premier_league.py'
    )
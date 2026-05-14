from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
from scripts.extract_crypto import extract_coins
from scripts.transform_crypto import transform_crypto_data
from scripts.load_crypto import load_coins_to_postgre

default_args = {
    'owner': "shweta",
    'retries': 3,
    "retry_delay": timedelta(minutes=5)
}

with DAG(
    default_args=default_args,
    dag_id="crypto_market_pipeline",
    description="Crypto Market Intelligence Pipeline",
    schedule='@daily',
    start_date=datetime(2026, 5, 13),
    catchup=False
) as dag:
    extract = PythonOperator(
        task_id='extract_coins',
        python_callable=extract_coins
    )

    transform = PythonOperator(
        task_id='transform_crypto_data',
        python_callable=transform_crypto_data
    )

    load = PythonOperator(
        task_id='load_coins_to_postgre',
        python_callable=load_coins_to_postgre
    )

extract >> transform >> load

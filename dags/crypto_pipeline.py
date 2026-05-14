from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
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

    create_view = SQLExecuteQueryOperator(
        task_id="create_market_cap_view",
        conn_id="crypto_postgres",
        sql="""
        CREATE OR REPLACE VIEW top_crypto_market_cap AS
        SELECT 
               coin_name, 
               max(market_cap) as highest_market_cap
        FROM crypto_market_data
        GROUP BY coin_name
        ORDER BY highest_market_cap DESC
        """
    )

extract >> transform >> load >> create_view

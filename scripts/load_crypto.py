import pandas as pd
from scripts.logger_crypto import logger
from airflow.providers.postgres.hooks.postgres import PostgresHook

def load_coins_to_postgre():
    try:
        hook = PostgresHook(postgres_conn_id='crypto_postgres')
        engine = hook.get_sqlalchemy_engine()

        df = pd.read_csv('data/processed/crypto_coins_clean.csv')

        df.to_sql('crypto_market_data', engine, if_exists='append', index=False)

        logger.info(f"{len(df)} records loaded successfully into PostgreSQL ✅")
    except Exception as e:
        logger.info("Data Loading to Postgre failed.❌")
        raise e

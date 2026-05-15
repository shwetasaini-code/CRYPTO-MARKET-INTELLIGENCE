from scripts.logger_crypto import logger
from datetime import datetime, timezone
import pandas as pd
import ast


def transform_crypto_data():
    logger.info('Transforming Crypto Data !!!!')
    df = pd.read_csv('data/raw/crypto_coins_raw.csv')

    selected_columns = [
        "name",
        'symbol',
        "current_price",
        "market_cap",
        "total_volume",
        "price_change_percentage_24h",
        "roi"
    ]
    df = df[selected_columns]
    df['stamp_time'] = datetime.now(
        timezone.utc).replace(second=0, microsecond=0)

    df['roi'] = df['roi'].apply(
        lambda x: ast.literal_eval(x) if pd.notna(x) else None)
    df['roi_times'] = df['roi'].apply(
        lambda x: round(x['times'], 2) if isinstance(x, dict) else None)
    df['roi_currency'] = df['roi'].apply(
        lambda x: x['currency'] if isinstance(x, dict) else None)
    df.drop(columns=['roi'], inplace=True)

    df.fillna({'roi_times': 0}, inplace=True)
    df.fillna({'roi_currency': 'usd'}, inplace=True)

    df.rename(columns={
        'name': 'coin_name',
        'price_change_percentage_24h': 'price_change_24h'
    }, inplace=True)

    df.drop_duplicates(inplace=True)

    df.to_csv('data/processed/crypto_coins_clean.csv', index=False)

    # print(df.info())

    logger.info("Data cleaning completed.. ✔️")

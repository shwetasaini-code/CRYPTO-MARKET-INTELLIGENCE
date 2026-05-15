import requests
from scripts.logger_crypto import logger
import pandas as pd

CRYPTO_COINS_API = ("https://api.coingecko.com/api/v3/coins/markets"
                    "?vs_currency=usd&ids=bitcoin&names=Bitcoin&symbols=btc&category=layer-1")


def extract_coins():
    try:
        logger.info('Extracting crypto coins !!!!')
        response = requests.get(CRYPTO_COINS_API)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            df.to_csv('data/raw/crypto_coins_raw.csv', index=False)
            logger.info(f'{len(df)} Coins Extracted Successfully... ✔️')
            print("PRINT TEST")
            return df

    except Exception as e:
        logger.info('Coins extraction failed... ❌')
        raise e

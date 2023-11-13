import datetime
import pandas as pd
import os
import requests
import time
from dotenv import load_dotenv
import logging

load_dotenv()

def api_call(**context):
    time.sleep(30)
    date=context['ds']
    if (0<= datetime.datetime.strptime(date,'%Y-%m-%d').date().weekday()<5):
        response = requests.get(f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{date}?adjusted=true&apiKey={os.getenv('API_KEY')}")
        if response.raise_for_status()!=None:
            raise Exception("api call problem")
        data = response.json()
        if (data["resultsCount"]>0): 
            df = pd.DataFrame(data["results"])
            df2=df[["T", "o","c","h","l"]]
            df2.rename(columns = {'T':'Ticker','o':'open','c':'close','h':'high','l':'low'}, inplace = True)
            df2.to_parquet(f'gcs://bucket_dev01/data/{date}.parquet')
            return {"msg":"Data loaded"}
        else: 
            logging.info('No market ops day')
    else: 
        logging.info('Weekend day')     
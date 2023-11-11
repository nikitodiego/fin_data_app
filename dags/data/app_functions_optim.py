import datetime
import pandas as pd
from google.cloud import bigquery
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
        try:
            response = requests.get(f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{date}?adjusted=true&apiKey={os.getenv('API_KEY')}")
            data = response.json()
        except: 
            logging.error(f'{response.status_code}')
        if (data["resultsCount"]>0): 
            df = pd.DataFrame(data["results"])
            df2=df[["T", "o","c","h","l"]]
            df2.rename(columns = {'T':'Ticker','o':'open','c':'close','h':'high','l':'low'}, inplace = True)
            df2.to_parquet(f'gcs://bucket_dev01/data/{date}.parquet')
            return {"msg":"Data loaded"}
        else: logging.info('No market ops day')
    else: logging.info('Weekend day')        


def bucket_to_bq(**context):
    date=context['ds']
    xcom_object= context['task_instance'].xcom_pull(task_ids='llamada_a_api')
    if xcom_object=={"msg":"Data loaded"}:
        client = bigquery.Client()
        df = pd.read_parquet(f'gcs://bucket_dev01/data/{date}.parquet')
        df["date"]=date
        table_id = "analog-provider-400614.dataset_dev.tickers_optim_named"

        job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("Ticker", "STRING"),
            bigquery.SchemaField("open", "FLOAT"),
            bigquery.SchemaField("close", "FLOAT"),
            bigquery.SchemaField("high", "FLOAT"),
            bigquery.SchemaField("low", "FLOAT"),
            bigquery.SchemaField("date", "STRING")
        ],)
        load_job = client.load_table_from_dataframe(df, table_id, job_config=job_config)  
        load_job.result() 
        return {"msg":"Data loaded in BigQuery"}
    else: return {"msg":"No file found"}


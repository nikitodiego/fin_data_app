from datetime import datetime
import pandas as pd
from google.cloud import storage
from google.cloud import bigquery
import os
import json
import requests
import gcsfs
import time
from dotenv import load_dotenv

load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'/opt/airflow/dags/data/credentials.json'

def api_call(**context):
    time.sleep(30)
    date=context['ds']
    try:
        response = requests.get(f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{date}?adjusted=true&apiKey={os.getenv('API_KEY')}")
        data = response.json()
        if (data["resultsCount"]>0): 
            df = pd.DataFrame(data["results"])
            df2=df[["T", "o","c","h","l"]]
            with open('/opt/airflow/dags/data/credentials.json') as jsonFile:
                jsonObject = json.load(jsonFile)
                df2.to_parquet(f'gcs://bucket_dev01/data/{date}.parquet',storage_options={"token": jsonObject})
                jsonFile.close()
            return {"msg":"Data loaded"}
        else:
            return {"msg":"No market ops day"}        
    except:
        print(f"Error code: {response.status_code}")


def bucket_to_bq(**context):
    # Construct a BigQuery client object.
    try:
        client = bigquery.Client()
        date=context['ds']
        df = pd.read_parquet(f'gcs://bucket_dev01/data/{date}.parquet')
        df["date"]=date
        # TODO(developer): Set table_id to the ID of the table to create.
        table_id = "analog-provider-400614.dataset_dev.tickers_optim"

        job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("T", "STRING"),
            bigquery.SchemaField("o", "FLOAT"),
            bigquery.SchemaField("c", "FLOAT"),
            bigquery.SchemaField("h", "FLOAT"),
            bigquery.SchemaField("l", "FLOAT"),
            bigquery.SchemaField("date", "STRING")
        ],
        #skip_leading_rows=1,
        )
        load_job = client.load_table_from_dataframe(
            df, table_id, job_config=job_config
        )  # Make an API request.
        load_job.result()  # Waits for the job to complete.
    except: return "No file to load"


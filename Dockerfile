FROM apache/airflow:2.7.1 
ADD requirements.txt . 
RUN pip install --no-cache-dir apache-airflow==${AIRFLOW_VERSION} -r requirements.txt

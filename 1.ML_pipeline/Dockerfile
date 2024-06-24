FROM apache/airflow:2.9.2
COPY requirements.txt /
COPY data/telco_data.csv /
COPY config/model_config.json /
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt
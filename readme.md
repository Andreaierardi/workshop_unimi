### commands
<code>
python -m venv airflow_venv
source airflow_venv/bin/activate
</code>


pip install apache-airflow

Initialize the Airflow database with
<code>airflow db init. </code>

Use airflow  to handle migrations.
<code>db upgrade</code>

<code> airflow users  create --role Admin --username admin --email admin --firstname admin --lastname admin --password admin
</code>



docker-compose build  
docker-compose up  

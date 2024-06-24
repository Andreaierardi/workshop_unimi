# Unimi Workshop

## Requirements
- Docker


## Task 1: ML Engineering Workflow with Apache Airflow

### Overview
Creation of a machine learning pipeline using Apache Airflow. We will go through the process of data extraction, preprocessing, model training, and evaluation using Python scripts and Airflow DAGs (Directed Acyclic Graphs).

1.	Data Extraction: function reads data from a CSV file and saves it to the output directory.
2.	Data Preprocessing:  function handles missing values, encodes categorical features, scales numerical features, and saves the preprocessed data.
3.	Model Training with RandomForestClassifier: function trains a RandomForest model, prints and saves feature importances, and saves the trained model.
4.	Model Evaluation: function evaluates the trained model on the entire dataset, prints accuracy and classification report, and saves the report.
5.	**TODO** Custom Model Training 
6.	**TODO** Custom Model Evaluation 


### How to run 

#### Set Up Docker containers
1.	Start the Airflow web server and scheduler:
   
```sh
docker-compose build
docker-compose up
```
2.	Access the Airflow UI at
```
http://localhost:8080/
```

3. Login:
```
user: airflow
password: airflow
```
4.	Trigger the training_pipeline DAG to run the complete ML workflow.

### Task
Implement the <code>train_model</code> and <code>evaluate_model</code> functions in the script <code>train_model.py</code> to define two new Airflow tasks. These tasks will be responsible for training and evaluating an additional machine learning model of your choice. Ensure that the new model’s training and evaluation processes are properly integrated into the existing Airflow DAG.



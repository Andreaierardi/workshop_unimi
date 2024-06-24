# Unimi Workshop

## Requirements
- Docker



## Tasks

- ### Task 1:

 
  <bold> Set Up Docker containers </bold>
  
  Set up the Airflow enrivonment:
  ```bash
  docker-compose build
  docker-compose up
  ```
  
  Wait till the server is running.
  Copy&Paste the following URL into your browser to access airflow:
  ```
  http://localhost:8080/
  ```
  
  Login:
  ```
  user: airflow
  password: airflow
  ```
  
  
  Complete the function <code>train_model</code> and <code>evaluate_model</code> that create two Airflow Tasks to train and evaluate a new Machine Learning model.

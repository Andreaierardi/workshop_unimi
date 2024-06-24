from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt

import pickle
import json

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}


dag = DAG(
    'training_pipeline',
    default_args=default_args,
    description='A simple ML engineering workflow',
    schedule_interval='@daily',
    start_date=days_ago(1),
)

config_path = 'config/model_config.json'
def load_config(config_path):
    with open(config_path, 'r') as file:
        config = json.load(file)
    return config
    
def extract_data(**kwargs):
    CONFIG = load_config(config_path)
    # Simulating data extraction
    df = pd.read_csv('data/telco_data.csv', index_col=0)
    df.to_csv('output/extracted_data.csv', index=False)


def preprocess_data(**kwargs):
    CONFIG = load_config(config_path)
    df = pd.read_csv('output/extracted_data.csv')
    # Simulating data preprocessing
    df = df.dropna()
    
    # Transform target to boolean column
    df[CONFIG['target_column']] = df[CONFIG['target_column']].apply(lambda x: 1 if x == 'Yes' else 0)

    # Identify numerical and categorical columns
    df_no_target = df.drop(columns=[CONFIG['index_column'], CONFIG['target_column']])
    numerical_features = df_no_target.drop([]).select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = df_no_target.select_dtypes(include=['object']).columns.tolist()

    # One-hot encode categorical features
    onehot_encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    X_encoded = pd.DataFrame(onehot_encoder.fit_transform(df_no_target[categorical_features]), columns=onehot_encoder.get_feature_names_out(categorical_features))

    # Scale numerical features
    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(df_no_target[numerical_features]), columns=numerical_features)

    # Combine numerical and categorical features
    X_processed = pd.concat([X_scaled, X_encoded, df[[CONFIG['index_column'], CONFIG['target_column']]]], axis=1)
    print(X_processed.shape)
    print(X_processed.columns)
    X_processed.to_csv('output/preprocessed_data.csv', index=False)

def train_rf_model(**kwargs):
    CONFIG = load_config(config_path)
    df = pd.read_csv('output/preprocessed_data.csv')
    X = df.drop(columns=[CONFIG['index_column'], CONFIG['target_column']])
    y = df[CONFIG['target_column']]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=CONFIG['random_state'])

    model = RandomForestClassifier(**CONFIG['hyperparameters'])
    model.fit(X_train, y_train)

    # Print feature importances
    feature_importances = pd.DataFrame(model.feature_importances_,
                                    index = X_train.columns,
                                    columns=['importance']).sort_values('importance', ascending=False)
    print(feature_importances)
    # Plot feature importances
    plt.figure(figsize=(10, 8))
    plt.barh(feature_importances.index, feature_importances['importance'])
    plt.xlabel('Importance')
    plt.ylabel('Feature')
    plt.title('Feature Importance')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('output/feature_importance.png')

    # Save the model
    with open('output/model.pkl', 'wb') as f:
        pickle.dump(model, f)


def evaluate_rf_model(**kwargs):
    CONFIG = load_config(config_path)
    # Load the model
    with open('output/model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    df = pd.read_csv('output/preprocessed_data.csv')
    X = df.drop(columns=[CONFIG['index_column'], CONFIG['target_column']])
    y = df[CONFIG['target_column']]
    y_pred = model.predict(X)
    accuracy = accuracy_score(y, y_pred)
    print(f"Final Model Train Accuracy: {accuracy}")
    clf_report = classification_report(y, y_pred, output_dict=True)
    print(clf_report)

    clf_report_df = pd.DataFrame(clf_report).transpose()
    clf_report_df.to_csv('output/classification_report.csv')


def train_model(**kwards):
    ## INSERT CODE HERE ##
    pass

def evaluate_model(**kwards):
    ## INSERT CODE HERE ##
    pass

start = DummyOperator(
    task_id='start',
    dag=dag,
)

extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag,
)

preprocess_task = PythonOperator(
    task_id='preprocess_data',
    python_callable=preprocess_data,
    dag=dag,
)

train_rf_task = PythonOperator(
    task_id='train_rf_model',
    python_callable=train_rf_model,
    dag=dag,
)

evaluate_rf_task = PythonOperator(
    task_id='evaluate_rf_model',
    python_callable=evaluate_rf_model,
    dag=dag,
)
train_task = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    dag=dag
)
evaluate_task = PythonOperator(
    task_id='evaluate_model',
    python_callable=evaluate_model,
    dag=dag
)
end = DummyOperator(
    task_id='end',
    dag=dag,
)

start >> extract_task >> preprocess_task >> [train_rf_task, train_task]
train_rf_task >>  evaluate_rf_task  >> end
train_task >> evaluate_task >> end
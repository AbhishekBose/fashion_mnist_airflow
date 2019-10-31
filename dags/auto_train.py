#%%
import datetime as dt
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
import sys
sys.path.append('dags/')
from train import train
#%%

def check_for_dataset():
    print('Checking for dataset')
    # return 1

#%%
def start_training():
    print('Dataset found.Going to start training.')
    # return 1

#%%
dag = DAG('fetch_dataset_from_db',description='DAG to check untrainied dataset',schedule_interval='*/3 * * * *',
            start_date= dt.datetime(2019,10,31),catchup=False)

# dag2 = DAG('start trainig with fetched dataset',description='DAG to start training',schedule_interval='*/3' * * * *,
#             start_date= dt.datetime(2019,10,31),catchup=False)

#%%

dataset_fetch_operator = PythonOperator(task_id='check if dataset is present', python_callable=check_for_dataset, dag=dag)
training_start_operator = PythonOperator(task_id='start training with fetched dataset', python_callable=start_training, dag=dag)
#%%


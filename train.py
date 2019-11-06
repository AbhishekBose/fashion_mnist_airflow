#%%
import os
# os.environ['KERAS_BACKEND'] = 'tensorflow'
from keras import backend as K
import keras
# import tensorflow as tf
import numpy as np
import sys
sys.path.append('model/')
sys.path.append('db/')
from model import model_2
import json
from db_ops import mongoQueue
import mlflow



#%%
print('LOADING TRANING PARAMS FROM JSON...')
with open('train_config.json') as f:
    data = json.load(f)

print('Current training params are::')
print(data)

#%%
class LossHistory(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.losses = []

    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs.get('loss'))
#%%
def train(trainX,trainY,testX,testY,model):
    history = LossHistory()
    model.fit(trainX,trainY, batch_size=data['batch_size'], epochs=data['epochs'], verbose=data['verbose'],validation_split=0.3,shuffle=data['shuffle'],callbacks=[history])
    print(history)
    return model
#%%
if __name__ == "__main__":

    coll_name = 'dataset'
    mq = mongoQueue(coll_name)
    parent_path = '/home/abhishek/fashion_mnist_airflow/'
    dataset_count = 0
    with mlflow.start_run(run_name='fashion_mnist'):
        while mq.Dequeue !=None:
            dataset_info = mq.Dequeue()
            dataset_id = dataset_info['dataset_id']
            # with mlflow.start_run():
            mq.setAsProcessing(dataset_id)
            model = model_2(data['opt'])
            train_X_path = dataset_info['path']
            train_Y_path = train_X_path.replace('X','Y')
            trainX = np.load(parent_path+train_X_path)
            trainY = np.load(parent_path+train_Y_path)
            # trainX = np.load('/home/abhishek/fashion_mnist_airflow/data/0000/X_train.npy')
            # trainY = np.load('/home/abhishek/fashion_mnist_airflow/data/0000/Y_train.npy')

            testX = np.load('/home/abhishek/fashion_mnist_airflow/data/testing/X_test.npy')
            testY = np.load('/home/abhishek/fashion_mnist_airflow/data/testing/Y_test.npy')
            trained_model = train(trainX,trainY,testX,testY,model)
            scores = model.evaluate(testX,testY,verbose=1)
            print(scores)
            X_train_dim = trainX.shape
            Y_train_dim = trainY.shape

            X_test_dim = testX.shape
            Y_test_dim = testY.shape

            mlflow.log_param("alpha",0.001)
            mlflow.log_param("epochs",data['epochs'])
            mlflow.log_param('optimizer',data['opt'])
            mlflow.log_param("batch_size",data['batch_size'])
            mlflow.log_metric("eval_loss",scores[0])
            mlflow.log_metric("eval_acc",scores[1])
            mlflow.log_metric("eval_precision",scores[2])
            mlflow.log_metric("eval_recall",scores[3])
            mlflow.log_metric(key="accuracy", value=scores[1], step=dataset_count)
            dataset_count+=1
            mq.setAsProcessed(dataset_id)
    
        
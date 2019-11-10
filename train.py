#%%
import os
from keras import backend as K
import keras
import tensorflow as tf
import numpy as np
import sys
sys.path.append('model/')
sys.path.append('db/')
from model import model
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
def train(trainX,trainY,model):
    history = LossHistory()
    model.fit(trainX,trainY, batch_size=data['batch_size'], epochs=data['epochs'], 
                verbose=data['verbose'],validation_split=0.3,
                        shuffle=data['shuffle'],callbacks=[history])
    return model
#%%
if __name__ == "__main__":

    coll_name = 'dataset'
    mq = mongoQueue(coll_name)
    model = model(data['opt'])
    print(os.getcwd())
    
    dataset_count = 0
    with mlflow.start_run(run_name='fashion_mnist'):
        while mq.Dequeue !=None:
            try:
                dataset_info = mq.Dequeue()
                dataset_id = dataset_info['dataset_id']
                mq.setAsProcessing(dataset_id)
                train_X_path = dataset_info['path']
                train_Y_path = train_X_path.replace('X','Y')
                trainX = np.load(train_X_path)
                trainY = np.load(train_Y_path)

                testX = np.load('data/testing/X_test.npy')
                testY = np.load('data/testing/Y_test.npy')
                trained_model = train(trainX,trainY,model)
                scores = model.evaluate(testX,testY,verbose=1)
                print(scores)
                break
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
            except Exception as e:
                print('Exception encountered is:: ',str(e))
                break
        mlflow.log_artifact('model/model.py')
        mlflow.log_artifact('db/db_ops.py')
    
        
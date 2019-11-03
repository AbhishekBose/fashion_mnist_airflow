#%%
import os
# os.environ['KERAS_BACKEND'] = 'tensorflow'
from keras import backend as K
import keras
# import tensorflow as tf
import numpy as np
import sys
sys.path.append('model/')
from model import model_2
import json
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
    with mlflow.start_run():
        model = model_2(data['opt'])
        trainX = np.load('/home/abhishek/fashion_mnist_airflow/data/0000/X_train.npy')
        trainY = np.load('/home/abhishek/fashion_mnist_airflow/data/0000/Y_train.npy')

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
        
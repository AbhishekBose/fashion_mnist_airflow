#%%
from keras import backend as K
import keras
import numpy as np
import sys
sys.path.append('model/')
from model import model_2
import json
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
def train(trainX,trainY,testX,testY):
    model = model_2()
    history = LossHistory()
    model.fit(trainX,trainY, batch_size=data['batch_size'], epochs=data['epochs'], verbose=data['verbose'],validation_data=(testX,testY),shuffle=data['shuffle'],callbacks=[history])
    print(history)
#%%
if __name__ == "__main__":
    trainX = np.load('/home/abhishek/fashion_mnist_airflow/data/0000/X_train.npy')
    trainY = np.load('/home/abhishek/fashion_mnist_airflow/data/0000/Y_train.npy')

    testX = np.load('/home/abhishek/fashion_mnist_airflow/data/testing/X_test.npy')
    testY = np.load('/home/abhishek/fashion_mnist_airflow/data/testing/Y_test.npy')
    train(trainX,trainY,testX,testY)

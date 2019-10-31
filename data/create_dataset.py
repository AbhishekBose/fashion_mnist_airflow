#%%
import numpy as np
import os
from keras.datasets import fashion_mnist
from keras.utils import np_utils
import sys
sys.path.append('data/')
#%%
print("[INFO] loading Fashion MNIST...")
((trainX, trainY), (testX, testY)) = fashion_mnist.load_data()

# %%
trainX = trainX.reshape((trainX.shape[0], 28, 28, 1))
testX = testX.reshape((testX.shape[0], 28, 28, 1))

# scale data to the range of [0, 1]
trainX = trainX.astype("float32") / 255.0
testX = testX.astype("float32") / 255.0
 
# one-hot encode the training and testing labels
trainY = np_utils.to_categorical(trainY, 10)
testY = np_utils.to_categorical(testY, 10)
# %%
def split_datasets(X,Y):
    X_split = np.split(X,12)
    Y_split = np.split(Y,12)
    return X_split,Y_split

#%%
def save_dataset(X,Y,test_X,test_Y):
    for i in range(0,len(X)):
        dir_path = 'data/000'+str(i)
        os.mkdir(dir_path)
        np.save(dir_path+'/'+'X_train.npy',X[i])
        np.save(dir_path+'/'+'Y_train.npy',Y[i])
    os.mkdir('data/testing')
    np.save('data/testing/'+'X_test.npy',test_X)
    np.save('data/testing/'+'Y_test.npy',test_Y)
    return 1

# %%
if __name__ == "__main__":
    X,Y = split_datasets(trainX,trainY)
    save_dataset(X,Y,testX,testY)
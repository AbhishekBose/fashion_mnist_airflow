#%%
import numpy as np
import os
from keras.datasets import fashion_mnist
from keras.utils import np_utils
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
    X_split = np.split(X,6)
    Y_split = np.split(Y,6)
    return X_split,Y_split

#%%
def save__dataset(X,Y,test_X,test_Y):
    for i in range(0,len(X)):
        dir_path = '000'+str(i)
        os.mkdir(dir_path)
        np.save(dir_path+'/'+'X_train.npy',X[i])
        np.save(dir_path+'/'+'Y_train.npy',Y[i])
    os.mkdir('testing')
    np.save('testing/'+'X_test.npy',test_X)
    np.save('testing/'+'Y_test.npy',test_Y)
    return 1

# %%
if __name__ == "__main__":
    X,Y = split_datasets(trainX,trainY)
    save__dataset(X,Y,testX,testY)
#%%
import pymongo
from pymongo import MongoClient
import sys
import os
import numpy as np
sys.path.append('data/')
# from settings import MONGO_DB_URL,MONGO_DB_NAME, DB

MONGO_DB_NAME = 'fashion_mnist'
MONGO_DB_URL = 'localhost'
CLIENT = MongoClient(MONGO_DB_URL, 27017)
DB = CLIENT[MONGO_DB_NAME]

#%%
class mongoQueue:
    def __init__(self,coll_name):
        self.coll = DB[coll_name]
        self.coll_name = coll_name

    def Enqueue(self,query):
        self.eq_id = self.coll.insert(query,check_keys=False)
        print('Enqueued for object ID:::',self.eq_id)

    def Dequeue(self):
        print(self.coll_name)
        fetch_query = {'status':'Not Processed'}
        self.results = self.coll.find_one(fetch_query)
        return self.results

    def getAllDatasets(self):
        print(self.coll_name)
        fetch_query = {}
        dataset_list =[]
        self.results = self.coll.find(fetch_query)
        for i in self.results:
            dataset_list.append(i['dataset_id'])
        # print(self.results)
        return dataset_list

    def getAllProcessing(self):
        print(self.coll_name)
        fetch_query = {'status':'Processing'}
        self.results = self.coll.find(fetch_query)
        return self.results
    
    def getAllProcessed(self):
        print(self.coll_name)
        fetch_query = {'status':'Processed'}
        self.results = self.coll.find(fetch_query)

        return self.results
    
    # def get_vehicle_detector_status(self):
    #     print('Status collection is::: ',self.status_coll)
    #     status_query = {'Process_Name':'Vehicle_Detection'}
    #     self.status_result = self.status_coll.find(status_query)
    #     return self.status_result

        
    def setAsProcessing(self,objectId):
        print('ObjectId to be set as Processing::',objectId)
        # self.results = self.coll.find_one_and_update(query={"_id":objectId},update={"$set": {"process_state": "Processing"}})
        self.results = self.coll.find_one_and_update({"_id":objectId},{"$set": {"status": "Processing"}})
        # self.results = self.coll.update_one({"_id": objectId}, {"$set": {"process_state": "Processing"}})
        print(self.results)
        return self.results  


    def setAsProcessed(self,objectId):
        print('ObjectId to be set as Processed::',objectId)
        self.results = self.coll.find_one_and_update({"_id":objectId},{"$set": {"status": "Processed"}})
        return self.results        



def insert_into_db(data_set_path,db,set_id,test=False):
    if test:
        x_test = np.load(data_set_path+'/'+set_id+'/'+'X_test.npy')
        size = x_test.shape[0]
        query = {'dataset_id':set_id,'num_of_images':str(size),'status':'Not Processed','path':data_set_path+'/'+set_id+'/'+'X_test.npy','datatype':'testing'}

    else:
        x_train = np.load(data_set_path+'/'+set_id+'/'+'X_train.npy')
        size = x_train.shape[0]
        query = {'dataset_id':set_id,'num_of_images':str(size),'status':'Not Processed','path':data_set_path+'/'+set_id+'/'+'X_train.npy','datatype':'training'}
    print(query)
    mq.Enqueue(query)


#%%
coll_name = 'dataset'
mq = mongoQueue(coll_name)
# x =mq.Dequeue()


#%%
if __name__ == "__main__":
    data_folder_path = 'data'
    coll_name = 'dataset'
    mq = mongoQueue(coll_name)
    all_datasets = mq.getAllDatasets()
    for i in os.listdir(data_folder_path):
        if i not in all_datasets:
            print(i)
            if i=='testing':
                testing = True
                insert_into_db(data_folder_path,mq,i,testing)
            elif i.endswith('.py'):
                testing = False
                continue
            else:
                testing = False
                insert_into_db(data_folder_path,mq,i,testing)
    # for i in os.listdir(data_folder_path):
        # if i
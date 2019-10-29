#%%
import pymongo
from pymongo import MongoClient
import sys
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

    def Enqueue(self,coll,query):
        self.eq_id = coll.insert(query,check_keys=False)
        print('Enqueud for object ID:::',self.eq_id)

    def Dequeue(self):
        print(self.coll_name)
        fetch_query = {'status':'Not Processed'}
        self.results = self.coll.find_one(fetch_query)
        return self.results

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




#%%
# coll_name = 'fetch_list'
# mq = mongoQueue(coll_name)
# x =mq.Dequeue()
# y = mq.getAllProcessing()




#%%

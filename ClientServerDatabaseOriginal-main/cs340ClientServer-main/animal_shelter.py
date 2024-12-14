from pymongo import MongoClient
import pymongo
from bson.objectid import ObjectId

class AnimalShelter(object):
    '''CRUD operations for Animal collection in MongoDB'''

    def __init__(self, username, password):
        # Initializing the MongoClient. This helps to
        # access the MongoDB databases and collections.
        # Connection Variables
        #
        USER = username
        PASS = password
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 31541
        DB = 'AAC'
        COL = 'animals'
        #
        # Initialize Connection
        #
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER, PASS, HOST, PORT))
        self.database = self.client['%s' % (DB)]
        self.collection = self.database['%s' % (COL)]

# Complete this create method to implement the C in CRUD.
# Commented out print statement per feedback on 8-4-2024
    def create(self, data): # Modified by Buddy Marcey 7-28-2024
        
        # Created bool to mark successful creation
        success = False
        if data is not None:
            self.database.animals.insert_one(data) # data should be dictionary
            success = True
        else:
            raise Exception("Nothing to save, because data parameter is empty")
        
        # print statement to show success or not (not necessary, but makes it
        # a little more obvious when running the script)
        # if (success):
            # print("Document Created Successfully")
            
        return success
        

# Create method to implement the R in CRUD
# Removed print statement per feedback on 8-4-2024
    def read(self, data): # Modified by Buddy Marcey 7-28-2024
        
        # if data isn't empty, generate a list of query results
        if data is not None:
            returnedDocument = self.database.animals.find(data)
            
            return returnedDocument
        else:
            raise Exception("Document not found, please try again")
            
# Create method to implement the U in CRUD
# Method derived from examples at w3schools.com/python/python_mongodb_update.asp
    def update(self, data, updatedData): # Written by Buddy Marcey 8-4-2024
        
        # make sure data arguments are provided, else throw exception
        if data is not None and updatedData is not None:
            updateCount = self.database.animals.update_many(data, {"$set": updatedData})
            
            return updateCount.modified_count # from official pymongo documentation
        else:
            raise Exception("Not enough information to update")
            
        
# Create method to implement the D in CRUD
# Method derived from examples at w3schools.com/python/python_mongodb_delete.asp
    def delete(self, data): # Written by Buddy Marcey 8-4-2024
        
        # make sure data argument is provided, else throw exception
        if data is not None:
            deleteCount = self.database.animals.delete_many(data)
            
            return deleteCount.deleted_count # from official pymongo documentation
        else:
            raise Exception("No data specified")
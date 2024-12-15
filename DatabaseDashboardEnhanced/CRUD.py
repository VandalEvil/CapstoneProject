#############################################################################
# Name: Capstone Enhancement Dashboard
# Course: CS499 Computer Science Capstone
# Student: Buddy Marcey
# Date: 11-17-2024
#############################################################################

'''
The purpose of this program is to provide an end user with a dashboard
to access data stored in a MongoDB database. This MongoDB instance is running
in an EC2 instance on AWS. This file defines the CRUD operations needed to bridge
the dashboard and the database and provides the mechanism for starting the database
for use by the script found in dashboard.ipynb
'''

from pymongo import MongoClient


class AnimalShelter(object):

    def __init__(self, username, password):

        # values defining the Amazon EC2 instance where database is running
        USER: str = username
        PASS: str = password
        HOST: str = 'ec2-54-160-131-66.compute-1.amazonaws.com'
        PORT: int = 27017
        DB: str = 'AAC'
        COL: str = 'animals'

        # database initialization
        self.client = MongoClient('mongodb://%s:%s@%s:%s' % (USER, PASS, HOST, PORT))
        self.database = self.client['%s' % DB]
        self.collection = self.database['%s' % COL]

    # function to create new data entry
    def create(self, data):

        success: bool = False
        if data is not None:
            self.database.animals.insert_one(data)
            success = True
        else:
            raise Exception("Nothing to save, data parameter is empty")

        return success

    # function to retrieve data from database
    def read(self, data):

        if data is not None:
            returnedDocument = self.database.animals.find(data)

            return returnedDocument

        else:
            raise Exception("Document not found, please try again")

    # function to update an entry in the database
    def update(self, data, updatedData):

        if data is not None and updatedData is not None:
            updateCount = self.database.animals.update_many(data, {"$set": updatedData})

            return updateCount.modified_count

        else:
            raise Exception("Not enough information to update")

    # function to remove an item from the database
    def delete(self, data):

        if data is not None:
            deleteCount = self.database.animals.delete_many(data)

            return deleteCount.deleted_count

        else:
            raise Exception("No data specified")





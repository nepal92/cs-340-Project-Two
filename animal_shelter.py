"""
animal_shelter.py
CRUD Python module for the Grazioso Salvare project (CS-340 Project One / Two).
Provides create, read, update, and delete operations against the 'animals'
collection in the 'aac' MongoDB database.
"""

from pymongo import MongoClient
from bson.objectid import ObjectId


class AnimalShelter(object):
    """ CRUD operations for Animal shelter database in MongoDB """

    def __init__(self, username='aacuser', password='SNHU1234'):
        USER = username
        PASS = password
        HOST = '127.0.0.1'
        PORT = 27017
        DB = 'aac'
        COL = 'animals'

        # Connect targeting authSource=aac
        self.client = MongoClient(f"mongodb://{USER}:{PASS}@{HOST}:{PORT}/?authSource=aac")
        self.database = self.client[DB]
        self.collection = self.database[COL]

    def create(self, data):
        """ Inserts a document into MongoDB """
        if data is not None:
            if isinstance(data, dict):
                try:
                    insert_result = self.collection.insert_one(data)
                    return True if insert_result.inserted_id else False
                except Exception as e:
                    print(f"An error occurred during insert: {e}")
                    return False
            else:
                raise TypeError("Data parameter must be a dictionary")
        else:
            raise ValueError("Nothing to save, because data parameter is empty")

    def read(self, query=None, raise_on_error=False):
        """ Queries documents in MongoDB """
        # Default query to empty dict if None to allow fetching all documents
        if query is None:
            query = {}

        if isinstance(query, dict):
            try:
                cursor = self.collection.find(query)
                return list(cursor)
            except Exception as e:
                # By default errors are printed and an empty list is returned,
                # but the dashboard sets raise_on_error=True so a failed
                # connection is never mistaken for a legitimate empty result.
                if raise_on_error:
                    raise
                print(f"An error occurred during read: {e}")
                return []
        else:
            raise TypeError("Query parameter must be a dictionary")

    def update(self, query, update_data):
        """ Queries for and modifies document(s) in MongoDB """
        if query is not None and update_data is not None:
            if isinstance(query, dict) and isinstance(update_data, dict):
                try:
                    # Check if update_data already contains $ operators (e.g., $set)
                    if not any(k.startswith('$') for k in update_data.keys()):
                        update_payload = {"$set": update_data}
                    else:
                        update_payload = update_data

                    result = self.collection.update_many(query, update_payload)
                    return result.modified_count
                except Exception as e:
                    print(f"An error occurred during update: {e}")
                    return 0
            else:
                raise TypeError("Parameters must be dictionaries")
        else:
            raise ValueError("Parameters cannot be empty")

    def delete(self, query):
        """ Queries for and removes document(s) from MongoDB """
        if query is not None:
            if isinstance(query, dict):
                try:
                    result = self.collection.delete_many(query)
                    return result.deleted_count
                except Exception as e:
                    print(f"An error occurred during delete: {e}")
                    return 0
            else:
                raise TypeError("Query parameter must be a dictionary")
        else:
            raise ValueError("Query parameter cannot be empty")

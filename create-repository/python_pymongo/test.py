from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint

from datetime import datetime


# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient("mongodb://localhost:27017")
db = client.sirene_app

""" # Issue the serverStatus command and print the results
serverStatusResult=db.command("serverStatus")
pprint(serverStatusResult) """


collectiontest = db.collectiontest

""" post = {
    "author": "Cyrille LEDEAN",
    "id": "788",
    "tags": ["mongodb", "python", "pymongo"],
    "date": datetime.utcnow()
}

post_id = collectiontest.insert_one(post).inserted_id """



collectiontest.update_one(

    { "id": "788" },
    { "$set": { "author": "Eric SOLEILLAND" } },
    upsert= True
)
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import CollectionInvalid
import pandas as pd
import json
from time import time

client = MongoClient()
db = client.Project_BDA

def get_collection(name: str) -> Collection:
    try:
        collection = db.create_collection(name)
    except CollectionInvalid:
        collection = db[name]
    return collection   

def get_json(name : str) -> list or dict:
    with open(name, "r") as f:
        data = json.load(f)
        f.close()
    return data

col_tags = get_collection("Tags")
ids = col_tags.find({}, {"tag":0, "timestamp":0, "userId":0})
print("Tags")
with open("../data/tag_ids.json", "w") as f:
    json.dump(list(map(lambda x: {"_id" : str(x["_id"]), "movieId":x["movieId"]}, ids)), f)
    f.close()

col_genome = get_collection("Genome_Scores")
ids = col_genome.find({}, {"relevance":0,"tag":0})

print("Genomes")
with open("../data/genome_ids.json", "w") as f:
    json.dump(list(map(lambda x: {"_id":str(x["_id"]), "movieId":x["movieId"]}, ids)), f)
    f.close()

col_ratings = get_collection("Ratings")
ids = col_ratings.find({}, {"timestamp":0,"ratings":0, "userId":0})
print("Ratings")
with open("../data/ratings_ids.json", "w") as f:
    json.dump(list(map(lambda x: {"_id":str(x["_id"]), "movieId":x["movieId"]}, ids)), f)
    f.close()
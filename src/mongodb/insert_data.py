from pymongo import MongoClient
from bson import ObjectId
from pymongo.collection import Collection
from pymongo.errors import CollectionInvalid
import pandas as pd
import json
from time import time

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

def insert_documents(col : Collection, docs : list):
    MAX_SIZE = 5000000
    if len(docs) < MAX_SIZE:
        print(f"Collection is Small")
        col.insert_many(docs)
    else:
        print(f"Collection is Big")
        N = len(docs)
        i = 0
        while i * MAX_SIZE < N :
            print(f"Iteration {i}")
            start = i*MAX_SIZE
            end = (i+1) * MAX_SIZE
            col.insert_many(docs[start:end])
            i+=1

client = MongoClient()
db = client.Project_BDA

print("Start Inserting Genome")
col_genome = get_collection("Genome_Scores")
temp = get_json("data/genomes.json")
start = time()
insert_documents(col_genome, temp)
print(time() - start)

print("Start Inserting Tags")
col_tags = get_collection("Tags")
temp = get_json("data/tags.json")
start = time()
insert_documents(col_tags, temp)
print(time() - start)

print("Start Inserting Ratings")
col_ratings = get_collection("Ratings")
temp = get_json("data/ratings.json")
start = time()
insert_documents(col_ratings, temp)
print(time() - start)


col_movies = get_collection("Movies")
temp = get_json("data/movies.json")
print("Start Inserting Movies")
start = time()
col_movies.insert_many(temp)
print(time() - start)

### The code after this block is to create references 
### from movies to other objects that reference the movie.
### Not necessary for now , at least
# movies = col_movies.find({}, {"title":0, "genres":0, "imdbId":0, "genomes":0, "ratings":0, "tags":0})

# col_genome = get_collection("Genome_Scores")
# col_tags = get_collection("Tags")
# col_ratings = get_collection("Ratings")

# genome_ids = pd.read_json("data/genome_ids.json", orient="records")
# tag_ids = pd.read_json("data/tag_ids.json", orient="records")
# ratings_ids = pd.read_json("data/ratings_ids.json", orient="records")

# print("Starting References")
# start = time()
# for movie in movies:
#     movieid = movie["_id"]
#     current_gen = genome_ids[genome_ids.movieId == movieid]._id.apply(lambda x: ObjectId(x)).tolist()
#     current_tag = tag_ids[tag_ids.movieId == movieid]._id.apply(lambda x: ObjectId(x)).tolist()
#     current_rat = ratings_ids[ratings_ids.movieId==movieid]._id.apply(lambda x: ObjectId(x)).tolist()
#     col_movies.update_one({"_id":movieid}, 
#                           {"$set" : {
#                                 "genomes" : current_gen,
#                                 "tags": current_tag,
#                                 "ratings" : current_rat 
#                             }
#                         })

# print(time() - start)

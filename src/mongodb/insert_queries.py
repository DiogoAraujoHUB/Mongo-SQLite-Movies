from pymongo import MongoClient
from time import time

client = MongoClient()
db = client.Project_BDA

coll_gen = db["Genome_Scores"]
coll_ratings = db["Ratings"]
coll_movies = db["Movies"]
coll_tags = db["Tags"]

#Insere um filme na base de dados
movieid = 999999
title = "\'Rise of the Fallen Lizards (2022)\'"
genres = "\'Action|Horror|Lizard\'"
imdb = 999999
tmdb = 999999
query1 = { "movieid": movieid,
           "title": title,
           "genres": genres,
           "imdbid": imdb,
           "tmdbid": tmdb }

#Insere um rating na base de dados
userid = 134
rating = 3.5
ts = 999999
query2 = { "userid": userid,
           "movieid": movieid,
           "rating": rating,
           "ts": ts }

#Insere uma tag na base de dados
tagid = 9999999
tag = "\'Lizard\'"
ts = 1000000
query3 = { "userid": userid,
           "movieid": movieid,
           "tag": tag,
           "ts": ts,
           "tagid": tagid }


#Inserts queries into different collections (uncomment others to add them aswell)
start = time()
coll_movies.insert_one(query1)
#coll_ratings.insert_one(query2)
#coll_tags.insert_one(query3)
print(time() - start)

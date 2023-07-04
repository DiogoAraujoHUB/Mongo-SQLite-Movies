import sqlite3
from time import time

# Three insert queries that have data related to each other
db = sqlite3.connect("./database/Project_BDA.db")

#Insere um filme na base de dados
movieid = 999999
title = "\'Rise of the Fallen Lizards (2022)\'"
genres = "\'Action|Horror|Lizard\'"
imdb = 999999
tmdb = 999999
query1 = """INSERT INTO 
            Movies(movieid,title,genres,imdbid,tmdbid) 
            VALUES(%d,%s,%s, %d, %d)
""" % (movieid, title, genres, imdb, tmdb)

#Insere um rating na base de dados
userid = 134
rating = 3.5
ts = 999999
query2 = """INSERT INTO 
            Ratings(userid,movieid,rating,ts) 
            VALUES(%d,%d,%f, %d)
""" % (userid, movieid, rating, ts)

#Insere uma tag na base de dados
tagid = 9999999
tag = "\'Lizard\'"
ts = 1000000
query3 = """INSERT INTO 
            Tags(userid,movieid,tag,ts,tagid) 
            VALUES(%d,%d,%s, %d, %d)
""" % (userid, movieid, tag, ts, tagid)

try:
    cur = db.cursor()
    start = time()
    cur.execute(query3) #Change this to execute different queries
    print(time() - start)

    cur.close()
    db.commit()
    
except Exception as e:
    db.rollback()
    print(e)
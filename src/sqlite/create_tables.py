import sqlite3

#Has to be ran initially so that we can create the tables in the database
db = sqlite3.connect("./database/Project_BDA.db")

movies_query = """CREATE TABLE movies (
                movieid INTEGER PRIMARY KEY,
                title	 VARCHAR(512) NOT NULL,
                genres	 VARCHAR(512) NOT NULL,
                imdbid	 INTEGER,
                tmdbid	 INTEGER
            )"""

tags_query = """CREATE TABLE tags (
                    userid	 INTEGER NOT NULL,
                    movieid	 INTEGER NOT NULL,
                    tag		 VARCHAR(512),
                    ts		 DATETIME NOT NULL,
                    tagid INTEGER PRIMARY KEY,
                    FOREIGN KEY (movieid) REFERENCES Movies(movieId)
                )"""

ratings_query = """CREATE TABLE ratings (
        userid	 INTEGER,
        movieid	 INTEGER,
        rating	 FLOAT(2) NOT NULL,
        ts		 DATETIME NOT NULL,
        PRIMARY KEY(userid,movieid),
        FOREIGN KEY (movieid) REFERENCES Movies(movieId)
    )"""

genome_tags = """CREATE TABLE genome_tags (
        tagid INTEGER PRIMARY KEY,
        tag	 TEXT(512) UNIQUE
    )"""

genome_scores = """CREATE TABLE genome_scores (
	movieid		 INTEGER NOT NULL,
	tagid		 INTEGER NOT NULL,
	relevance	 FLOAT(8),
	PRIMARY KEY(movieid,tagid),
	FOREIGN KEY (movieid) REFERENCES Movies(movieId),
	FOREIGN KEY (tagid) REFERENCES Genome_Tags(tagId)
)"""
try:
    cur = db.cursor()
    #create movies table
    cur.execute(movies_query)
    #create tags table
    cur.execute(tags_query)
    #create ratings table
    cur.execute(ratings_query)
    #create genome_tags table
    cur.execute(genome_tags)
    #create genome_scores table
    cur.execute(genome_scores)
    
    db.commit()
    print("Operation succesfull")
except Exception as e:
    db.rollback()
    print("An error ocurred")
    print(e)

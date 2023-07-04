import sqlite3
import pandas as pd
import time

#Have to change this variable depending on where your .csv files are at
DATA_PATH = "../../Dataset/"

#Connect to the database in the folder (its location)
db = sqlite3.connect("./database/Project_BDA.db")
TIMEIT = False

def insert_dataframe(df : pd.DataFrame, 
                    table_name: str, columns: str or list, 
                    con: sqlite3.Connection,
                    timeit : bool):

    if type(columns) is list: columns = ','.join(columns)
    question_marks = ','.join(['?']*len(columns.split(',')))

    query = f"INSERT INTO {table_name} ({columns}) values({question_marks})"
    data = df.itertuples(index=False, name=None)
    print(f"Inserting into {table_name}")
    try:
        cur = con.cursor()
        if timeit: 
            tic=time.time()
        cur.executemany(query, data)
        cur.close()
        con.commit()
        if timeit: 
            toc=time.time()
            print(toc-tic)
        print("Operation successfull!")
    except Exception as e:
        con.rollback()
        print("Error ocurred")
        print(e)
    print()

### Insert Movies Table ###
movies = pd.read_csv(DATA_PATH + "movies.csv", header=0).merge(
           pd.read_csv(DATA_PATH + "links.csv", header=0), 
       on="movieId"
   )
insert_dataframe(movies, "movies", movies.columns.tolist(), db, TIMEIT)

### Insert Tags Table ###
tags = pd.read_csv(DATA_PATH + "tags.csv", header = 0)
insert_dataframe(tags, "tags", ["userid", "movieid", "tag", "ts"], db, TIMEIT)

### Create Ratings Table ###
ratings = pd.read_csv(DATA_PATH+ "ratings.csv", header=0)
insert_dataframe(ratings, "ratings", ["userid", "movieid", "rating", "ts"], db, TIMEIT)

### Create Genome_Scores Table ###
genome_scores = pd.read_csv(DATA_PATH + "genome-scores.csv", header = 0)
insert_dataframe(genome_scores, "genome_scores", genome_scores.columns.tolist(), db, TIMEIT)

### Create Genome_Tags Table ###
genome_tags = pd.read_csv(DATA_PATH + "genome-tags.csv", header = 0)
insert_dataframe(genome_tags, "genome_tags", genome_tags.columns.to_list(), db, TIMEIT)
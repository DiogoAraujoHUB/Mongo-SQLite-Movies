import sqlite3
from time import time

#Connect to database in folder
db = sqlite3.connect("./database/Project_BDA.db")

#Subqueries used in query 1
tagid = 2
subquery1 = """ SELECT gs.movieid, gs.tagid
                            FROM Genome_Scores gs
                            INNER JOIN (
                                SELECT movieid, MAX(relevance) relevance
                                FROM Genome_scores
                                GROUP BY movieid
                            ) gs_max_relevance
                            ON gs.movieid = gs_max_relevance.movieid
                                AND gs.relevance = gs_max_relevance.relevance
                                AND gs.tagid = %d """ % (tagid)

#Selecionar os filmes com maior 'rating' relevantes a uma tag (tagid).
#Os filmes em consideração para a pesquisa 
#são que têm uma certa tag como a mais relevante
query1 = """ SELECT Movies.title, AVG(rating) AS avg_rating
             FROM Ratings
             INNER JOIN MOVIES
             ON Movies.movieid=Ratings.movieid
             GROUP BY Ratings.movieid
                HAVING COUNT(Ratings.movieid)>=100
                    AND Movies.movieid in (
                        SELECT movieid
                        FROM (
                            %s
                        )
                    )
             ORDER BY avg_rating DESC
         """ % (subquery1)

# Adicionar tabela com as tags mais relevantes de cada filme(*)
# adicionar indice na tabela ratings, na coluna "movieId"
# adicionar indice na tabela (*) sob o camp tagid
# Versão optimizada da query 1
query1_2 = """
    SELECT m.title, matches.avg_rating
    FROM movies m
    INNER JOIN (
        SELECT r.movieid, avg(rating) avg_rating, COUNT(*) counts
        FROM Movie_genome_tags_max_relevance tbl, Ratings r
        WHERE tbl.tagid = %d
            AND tbl.movieid = r.movieid
        GROUP BY r.movieid
        HAVING counts>100
        ) matches
    ON m.movieid = matches.movieid
    ORDER BY avg_rating
""" % (tagid)

#Create extra table for query 1_2
query1_2_create_table = """CREATE TABLE Movie_genome_tags_max_relevance (
	movieid INT,
	tagid INT,
	PRIMARY KEY(movieid, tagid)
)"""

#Insert into extra table for query 1_2
query1_2_insert_into_table = """INSERT INTO Movie_genome_tags_max_relevance
                SELECT gs.movieid, gs.tagid
                FROM Genome_Scores gs
                INNER JOIN (
                    SELECT movieid, MAX(relevance) relevance
                    FROM Genome_scores
                    GROUP BY movieid
                ) gs_max_relevance
                ON gs.movieid = gs_max_relevance.movieid
                    AND gs.relevance = gs_max_relevance.relevance
"""

#Subqueries used in query 2
subsubquery2 = """SELECT m.movieid movieid, m.title title, 
                            TRIM(LOWER(t.tag)) tag, 
                            COUNT(TRIM(LOWER(t.tag))) counts
                    FROM Movies m, Tags t
                    WHERE m.movieid = t.movieid
                    GROUP BY m.movieid, TRIM(LOWER(t.tag))"""
subquery2 = """SELECT counts_table.movieid, counts_table.title, counts_table.tag
                FROM (
                    %s
                    ) counts_table
                INNER JOIN (
                    SELECT movieid, title, tag, MAX(counts) counts
                    FROM (
                        %s
                    ) 
                    GROUP BY movieid 
                ) counts_max
                ON counts_table.movieid = counts_max.movieid
                    AND counts_table.counts = counts_max.counts
""" % (subsubquery2, subsubquery2)


#Obter os filmes cujas tags por
# utilizador mais frequentes
# coincidem com as de um
# certo filme escolhido à priori
## ** Procurar por filmes semelhantes ao selecionado **
movieid = 1
query2 = """
            SELECT tbl.movieid, tbl.title, t.movieid, t.title
            FROM (
                %s
            ) tbl
            LEFT JOIN (
                %s
            ) t
            ON tbl.tag = t.tag
                AND tbl.movieid!=t.movieid
            WHERE tbl.movieid=%d
            ORDER BY t.movieid
""" % (subquery2, subquery2, movieid)

# Obter o average rating de um filme
movieid = 200
query3 = """SELECT m.movieid, m.title, AVG(rating)
            FROM Movies m, Ratings r
            WHERE m.movieid = r.movieid
            GROUP BY m.movieid 
            HAVING m.movieid=%d
""" % (movieid)

# Igual à query anterior, só que utilizando um agrupamento dos ratings em vez dos movies (resultado igual)
query3_2 = """SELECT r.movieid, m.title, AVG(rating)
            FROM Movies m, Ratings r
            WHERE m.movieid = r.movieid
            GROUP BY r.movieid 
            HAVING r.movieid=%d
""" % (movieid)


#Mostrar os indexes
show_indexes = "Select * from SQLite_master"

#Created indexes for above queries
index_movies_movieid = ("CREATE UNIQUE INDEX index_movies_movieid ON Movies (movieid);") #Made for query 3, works well
index_tags_movieid = ("CREATE INDEX index_tags_movieid ON Tags (movieid);") #Made for query 2, doesnt change
index_ratings_movieid = ("CREATE INDEX index_ratings_movieid ON Ratings (movieid);") #Made for query 1_2 and 3_2, works well
index_extra_tagid = ("CREATE INDEX index_extra_tagid ON Movie_genome_tags_max_relevance (tagid);") #Made for query 1_2, works wells

#Drop an index (title change depending on index we wish to remove)
drop_index = ("DROP INDEX index_tags_movieid")

try:
    cur = db.cursor()
    start = time()
    cur.execute(query3) #Change this to execute which query / index you wish to execute
    print(time() - start)

    input() #Requires an input (intermediary step) to show result
    result = cur.fetchall()
    for item in result:
        print(item)
except Exception as e:
    print(e)
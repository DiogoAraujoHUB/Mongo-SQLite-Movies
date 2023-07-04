import sqlite3
from time import time

db = sqlite3.connect("./database/Project_BDA.db")

# Mostrar os filmes que sejam do "genre" ação
userid = 27
query1 = """
    SELECT title
    FROM movies
    WHERE genres like '%Action%'
"""

# Mostrar as tags, e o utilizador que as criou, que tenham sido criadas entre 2007 e 2008
query2 = """SELECT userid, tag
            FROM Tags
            WHERE ts BETWEEN 
                    CAST(strftime('%s', '2007-01-01') AS integer)
                AND
                    CAST(strftime('%s', '2008-01-01') AS integer)
"""

try:
    cur = db.cursor()

    start=time()
    cur.execute(query2) #Execute query here (change name to change query executed)
    print(time() - start)

    input()
    results = cur.fetchall()
    for item in results:
        print(item)
except Exception as e:
    print(e)
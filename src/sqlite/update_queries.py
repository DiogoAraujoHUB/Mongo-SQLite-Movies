import sqlite3
from time import time

db = sqlite3.connect("./database/Project_BDA.db")

# Update ao rating que um utilizador deu
userid = 134
rating = 3.5
query = """UPDATE Ratings
           SET rating=%f
           WHERE userid=%d
""" % (rating, userid)

try:
    cur = db.cursor()
    start = time()
    cur.execute(query)
    print(time() - start)

    cur.close()
    db.commit()
    
except Exception as e:
    db.rollback()
    print(e)
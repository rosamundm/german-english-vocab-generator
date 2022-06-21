import datetime
import sqlite3
from constants import DB_PATH


sqliteConnection = sqlite3.connect(DB_PATH)
cursor = sqliteConnection.cursor()

sqlite_select_Query = ("SELECT * FROM vocab")
cursor.execute(sqlite_select_Query)
records = cursor.fetchall()

with open("db_output.txt", "w") as f:
    f.write("%s\n\n" % str(datetime.datetime.now()))
    for r in records:
        f.write("%s\n" % str(r))
        print(r)

cursor.close()



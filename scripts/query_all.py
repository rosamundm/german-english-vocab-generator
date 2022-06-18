import pprint
import sqlite3


sqliteConnection = sqlite3.connect("vocab.db")
cursor = sqliteConnection.cursor()

sqlite_select_Query = ("SELECT * FROM vocab")
cursor.execute(sqlite_select_Query)
records = cursor.fetchall()

with open("db_output.txt", "w") as f:
    for r in records:
        f.write("%s\n" % str(r))

cursor.close()


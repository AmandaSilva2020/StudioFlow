import sqlite3

con = sqlite3.connect('studioflow.db')
cur = con.cursor()

with open('schema.sql', 'r') as file_handle:
    schema_sql = file_handle.read()
    cur.executescript(schema_sql)

con.commit()
con.close()

print("DB updated.")
from __future__ import with_statement
import sqlite3
from contextlib import closing
import time






if __name__ == "__main__":
  con = sqlite3.connect("my_first_db.sqlite")
  cur = con.cursor()

  cur.execute("insert into my_table_2 values (?,?,?)", (10, "hello", "qwer"))
  con.commit()
  con.close()

  
'''
  with closing(sqlite3.connect(":memory:") as db:
    with open("schema.sql", "r") as f:
      db.cursor().executescript(f.read())
    db.commit()
'''





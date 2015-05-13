from __future__ import with_statement
import sqlite3
from contextlib import closing
import time






if __name__ == "__main__":
  con = sqlite3.connect(":memory:")
  cur = con.cursor()
  f = open("schema.sql", "r")
  cur.executescript(f.read())

  cur.excute("insert into light value (?)", (0))

  
'''
  with closing(sqlite3.connect(":memory:") as db:
    with open("schema.sql", "r") as f:
      db.cursor().executescript(f.read())
    db.commit()
'''





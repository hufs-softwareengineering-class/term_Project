import sqlite3

con = sqlite3.connect("testdb.sqlite-journal")
c = con.cursor()

c.execute("select count(*) from light where room1 == 1 and room3 == 1")

result = []
result.append(c.fetchone())

print result

from Root import *
import sqlite3
import os, time, sys
from multiprocessing import Process, Queue

sqlite_file = 'our_db.sqlite'    # name of the sqlite database file
lighttable = 'light'
tempertable = 'temper'
humidtable = 'humid'
usertemper_setting = 'setting'
current_person = 'cur_person'
pipe_name = "pipefile"
Time = datetime.datetime.now()
timeList = []

if __name__ == "__main__":

  if not os.path.exists(pipe_name):
    os.mkfifo(pipe_name)

  pipein = open(pipe_name, 'r')
  conn = sqlite3.connect(sqlite_file)
  c = conn.cursor()


  # Make Queeue
  que = Queue()
  queue = []
  root = Root(c)
  '''
  lightSensingThread = myThread(root, "light", queue)
  temperSensingThread = myThread(root, "temper", queue)
  humidSensingThread = myThread(root, "humid", queue)
  magnetSensingThread = myThread(root, "magnet", queue)
  infraredSensingThread = myThread(root, "infrared", queue)
  lightSensingThread.start()
  temperSensingThread.start()
  humidSensingThread.start()
  magnetSensingThread.start()
  '''
  root.makeDAG()
  
  c.execute('CREATE TABLE {tn} ({nf} {ft})'\
      .format(tn = lighttable, nf = "ID", ft="INTEGER"))
  
  c.execute('CREATE TABLE {tn} ({nf} {ft})'\
      .format(tn = tempertable, nf = "ID", ft="INTEGER"))
  
  c.execute('CREATE TABLE {tn} ({nf} {ft})'\
      .format(tn = humidtable, nf = "ID", ft="INTEGER"))
  
  #intialize the temeperr setting
  c.execute('CREATE TABLE {tn} ({nf} {ft})'\
      .format(tn = usertemper_setting, nf = "ID", ft="INTEGER"))
  c.execute("ALTER TABLE {tn} ADD COLUMN '{nf}' {ft}"\
      .format(tn = usertemper_setting, nf = "HIGH", ft = "INTEGER"))
  c.execute("ALTER TABLE {tn} ADD COLUMN '{nf}' {ft}"\
      .format(tn = usertemper_setting, nf = "LOW", ft = "INTEGER"))
  c.execute("insert into setting values (?,?,?)", [1, 18, 28])

  c.execute('CREATE TABLE {tn} ({nf} {ft})'\
      .format(tn = current_person, nf = "ID", ft="INTEGER"))

  c.execute("ALTER TABLE {tn} ADD COLUMN '{nf}' {ft}"\
      .format(tn = current_person, nf = "sum", ft="INTEGER"))
  c.execute('insert into cur_person values (?,?)', [1, 0])


  for i in range(0, root.gettotalnum()):
    roomnum = "room" + str(i+1)
    c.execute("ALTER TABLE {tn} ADD COLUMN '{nf}' {ft}"\
        .format(tn = lighttable, nf = roomnum, ft="INTEGER"))
  
    c.execute("ALTER TABLE {tn} ADD COLUMN '{nf}' {ft}"\
        .format(tn = tempertable, nf = roomnum, ft="INTEGER"))
  
    c.execute("ALTER TABLE {tn} ADD COLUMN '{nf}' {ft}"\
        .format(tn = humidtable, nf = roomnum, ft="INTEGER"))
  num = ""
  baselist = []
  for i in range(0, root.gettotalnum()):
    num+="?,"
    baselist.append(0)
  baselist.append(0)
  num+="?)"
  lightquery = "insert into light values("+num
  temperquery = "insert into temper values("+num
  humidquery = "insert into humid values("+num
  c.execute(lightquery, baselist)
  c.execute(temperquery, baselist)
  c.execute(humidquery, baselist)

  p = Process(target = magnetSensin, args(que,))
  p.start()
  #need to add the pipe module
  while 1:
    line = pipein.readline()[:-1]
    magmessage = ""
    magmessage = que.get(timeout = 1)
    if magmessage =="":
      pass
    else :
      queue.append(magmessage)
    if line!="": # need to modify
      #need to parsing the json and make meassage , then enqueue the message to the queue
      #need to parsing the mode 
      if schema == "prevenmode":
        #prevalue = #parsing the json 
        #root.setPrevention(prevalue)
        continue
      message = 0 #parisng the jsonand make the message (need to access the DB data) 
      queue.append(message)

    elif len(queue) == 0: #need to modify
      root.getData(queue)
    else :
      
      text = queue.pop()
      root.putData(text)
      




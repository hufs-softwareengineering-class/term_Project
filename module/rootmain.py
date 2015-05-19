from Root import *
import sqlite3
import os, time, sys, Queue

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

  pipein = os.open(pipe_name, 'r')

  # Make Queeue
  queue = []
  root = Root()
  lightSensingThread = myThread(root, "light", queue)
  temperSensingThread = myThread(root, "temper", queue)
  humidSensingThread = myThread(root, "humid", queue)
  magnetSensingThread = myThread(root, "magnet", queue)
  infraredSensingThread = myThread(root, "infrared", queue)
  lightSensingThread.start()
  temperSensingThread.start()
  humidSensingThread.start()
  magnetSensingThread.start()
  root.makeDAG()
  
  conn = sqlite3.connect(sqlite_file)
  c = conn.cursor()

  c.execute('CREATE TABLE {tn} ({nf} {ft})'\
      .format(tn = lighttable, nf = "room1", ft="INTEGER"))
  
  c.execute('CREATE TABLE {tn} ({nf} {ft})'\
      .format(tn = tempertable, nf = "room1", ft="INTEGER"))
  
  c.execute('CREATE TABLE {tn} ({nf} {ft})'\
      .format(tn = humidtable, nf = "room1", ft="INTEGER"))
  
  c.execute('CREATE TABLE {tn} ({nf} {ft})'\
      .format(tn = usertemper_setting, nf = "HIGH", ft="INTEGER"))
  c.execute('ALTER TABLE {tn} ADD CLOUMN ({nf} {ft})'\
      .format(tn = usertemper_setting, nf = "LOW", ft = "INTEGER"))
  c.execute('CREATE TABLE {tn} ({nf} {ft})'\
      .format(tn = current_person, nf = "sum", ft="INTEGER"))


  for i in range(0, root.gettotalnum()-1):
    roomnum = "room" + str(i+2)
    c.execute('ATRER TABLE {tn} ADD CLOUMN ({nf} {ft})'\
        .format(tn = lighttable, nf = roomnum, ft="INTEGER"))
  
    c.execute('ALTER TABLE {tn} ADD CLOUMN ({nf} {ft})'\
        .format(tn = tempertable, nf = roomnum, ft="INTEGER"))
  
    c.execute('ALTER TABLE {tn} ADD CLOUMN ({nf} {ft})'\
        .format(tn = humidtable, nf = roomnum, ft="INTEGER"))
  

  
  #need to add the pipe module
  while 1:
    if ~pipein.empty(): # need to modify
      line = pipein.readline()[:-1]
      #need to parsing the json and make meassage , then enqueue the message to the queue
      #need to parsing the mode 
      if schema == "prevenmode":
        prevalue = #parsing the json 
        root.setPrevention(prevalue)
        continue
      message = #parisng the jsonand make the message (need to access the DB data) 
      queue.append(message)

    else if queue.len() == 0: #need to modify
      root.getData()
    else :
      text = queue.pop()
      root.putData(text)
      




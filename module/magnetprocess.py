import sqlite3
import os, time, sys
from GPIOmagnetread import *
from GPIOdistance import *
from multiprocessing import Process, Queue
from pipeprocess2 import *
def magnetSensing(que, total_num, conn):
  tempolight = ""
  magnet_state = 0
  distance_flag = 0
  human_num = 0
  prevention_Mode = 0
  prique = []
  sqllite_file = "our_db.sqlite"
  pipe_name = "pipefile2"
  line = ""
  con = sqlite3.connect("our_db.sqlite", check_same_thread = False)
  cursor = con.cursor()
  webpipeque = Queue()
  webpipe = Process(target = pipeprocess2, args = (webpipeque, pipe_name))
  webpipe.start()
  
 

  
  prevention_Mode = 1
  
  while 1:
    line = ""
    try:
      line = webpipeque.get(block = False, timeout = 1)
    except:
      pass
    if line != "":
      print line + "from web"

      # need to parse
      # setting prevention_Mode
    magnet_state = GPIOmagnetRead() 
    distance_flag = GPIOdistance()
    # read distance_flag
    if distance_flag == 0 and magnet_state == 1:
      human_num += 1
      cur_num = []
      cursor.execute("SELECT ID FROM cur_person order by ID DESC limit 1")
      result = int(cursor.fetchone()[0])+1
      cur_num.append(result)
      cur_num.append(human_num)
      cursor.execute("insert into cur_person values (?, ?)", cur_num)
      if human_num == 1:
        print "what the fuck"
        tempolight = ""

        prique = []
        for i in range(total_num):
          prique.append([])
          for j in range(total_num):
            prique[i].append(0)
        totalsum = 0
        for i in range(total_num - 1):
          for j in range(i +1, total_num):
            print "before query@@@@@"
            query = "select count (*) from light where room%d == 1 and room%d == 1" %(i+1, j+1)
	    print "after query@@@@@@"
            cursor.execute(query)
	    print "after1 query@@@@@@"
            prique[i][j] = int(cursor.fetchone()[0])
	    print "after2 query@@@@@@"
            totalsum += prique[i][j]
	    print "after3 query@@@@@@"
        basenum = totalsum /((total_num*(total_num -1)) /2)
	print "after4 query@@@@@@"
        temparr = []
        for i in range(total_num):
          temparr.append(0)
	print "debug1 @@@@@@@@@@@@@ "
        for i in range(total_num -1 ):
          for j in range(i+1, total_num):
            if prique[i][j]>=basenum:
              temparr[i] = 1
              temparr[j] = 1

	print "debug2 @@@@@@@@@@@@@ "

        templight = ""
        for i in temparr:
          if i ==1:
            templight +="1"
          else:
            templight += "0"
	print "debug3 @@@@@@@@@@@@@ "

        message = "put/%s/%s/%s" %(templight, "?", "?")
        print message + "====================="
        print "\n"
        que.put(message)
    elif distance_flag == 1 and magnet_state == 1:
      human_num = human_num -1
      cur_num = []
      cursor.execute("SELECT ID FROM cur_person order by ID DESC limit 1")
      result = int(cursor.fetchone()[0])+1
      cur_num.append(result)
      cur_num.append(human_num)
      cursor.execute("insert into cur_person values (?, ?)", cur_num)
      
      templight = ""
      if human_num == 0:
        for i in range(total_num):
          tempolight +='0'
        message = "put/%s/%s/%s" %(tempolight, "?", "?")
        que.put(message)
    conn.commit()




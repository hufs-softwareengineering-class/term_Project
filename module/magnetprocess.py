import sqlite3
def magnetSensing(que, total_num):
  tempolight = ""
  magnet_state = 0
  distance_flag = 0
  human_num = 0
  prevention_Mode = 0
  prique = []
  sqllite_file = "our_db.splite"
  con = sqlite3.connect(sqllite_file)
  cursor = con.cursor()
  while 1:
    magnet_state = GPIOmagnetRead()
    if distance_flag == 0 && magnet_state == 1:
      human_num += 1
      if human_num == 1:
        tempolight = ""

        prique = []
        for i in range(total_num):
          prique.append([])
          for j in range(total_num):
            prique[i].append(0)
        totalsum = 0
        for i in range(total_num - 1):
          for j in range(i +1, self.total_num-1):
            query = "select count (*) from light where room%d == 1 and room%d == 1" %(i, j)
            cursor.execute(query)
            prique[i][j] = int(cursor.fetchone[0])
            totalsum += prique[i][j]
        basenum = totalsum /(total_num*(total_num -1) /2)
        temparr = []
        for i in range(total_num):
          temparr.append(0)

        for i in range(total_num -1 ):
          for j in range(i+1, total_num -1 ):
            if prique[i][j]>basenum:
              temparr[i] = 1
              temparr[j] = 1


        templight = ""
        for i in temparr:
          if i ==1:
            templight +="1"
          else:
            templight += "0"

        message = "put/%s/%s/%s" %(templight, "?", "?")
        que.put(message)
    elif distance_flag == 1 && magnet_state == 1:
      human_num = human_num -1
      templight = ""
      if human_num == 0:
        for i in total_num:
          tempolight +='0'
        message = "put/%s/%s/%s" %(tempolight, "?", "?")
        que.put(message)




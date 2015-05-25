from test_inquiry import *
import bluetooth
from clientmodule import *
from servermodule import *
import sys
import time
import datetime
import Queue
import threading
from GPIOlightread import *
from GPIOtemperread import *
from GPIOhumidread import *
from GPIOmagnetread import *

class myThread(threading.Thread):
  def __init__(self, node, sensingType, que):
    threading.Thread.__init__(self)
    self.node = node
    self.sensingType = sensingType
    self.que = que
    self.dictionary = {
        "light" : self.node.lightSensing,
        "temper" : self.node.temperSensing,
        "humid" : self.node.humidSensing,
        "magnet" : self.node.magnetSensing,
        "infrared" : self.node.infraredSensing,
        }

  def run(self):
    self.dictionary[self.sensingType](self.que)

class Root():
  addr = []
  dic_addr ={}
  child = []
  number = -1
  light_state = 0
  magnet_state = 0
  humid_state = 0
  temperature_state = 0
  search_index = 0
  total_num = 0
  count = 0
  autoMode = 0 #initial autoMode bit zero
  human_num = 0
  distance_flag = 0 # if distance is less than 50, distance_flag 1
  prevention_Mode = 0

  #construcotr
  def __init__(self, c):
    self.addr=getaddr_rssi()
    self.number = 0
    self.cursor = c
    
  def gettotalnum(self):
    return self.total_num

  def setAutoMode(self):
    self.autoMode = 1

  def clearAutoMode(self):
    self.autoMode = 0

  def getAutoMode(self):
    return self.autoMode

  #make DAG 
  def makeDAG(self):
    message = "search/%d/%d" %(0, self.number)
    clientmodule(message, self.addr[self.search_index].getaddr())
    self.search_index = self.search_index + 1
    while 1:
      print "==================>debug point"
      data = servermodule()
      dataparse = data.split('/')
      address = dataparse[len(dataparse)-1]

      if dataparse[0] == "search":
        response = "searchres/%s" %(dataparse[1])
        clientmodule(response, address)

      elif dataparse[0] == "searchres":
        if self.count != int(dataparse[1]):
          self.child.append(self.count+1)
          self.dic_addr[self.count+1] = address
          self.count = int(dataparse[1])

        if self.search_index is len(self.addr):
          self.total_num = int(dataparse[1])
          break
        else:
          message = "search/%d/%d" %(int(dataparse[1]), self.number)
          clientmodule(message, self.addr[self.search_index].getaddr())
          self.search_index = self.search_index +1


  def getData(self, que):
    print "child : ", self.child
    lightarr = []
    temperarr = []
    humidarr = []
    for i in range(0, self.total_num):
      lightarr.append(0)
      temperarr.append(0)
      humidarr.append(0)

    print "---------------get------------"
    num_index = 0
    while 1:
      if num_index == self.total_num + 1:
        break
      if num_index == self.number:
        #get the state of root's light & temperature...
        num_index = num_index + 1
        continue
        
      child_num = 0
      while 1:
        message = "%s/%d" %("get", num_index)
        clientmodule(message, self.dic_addr[self.child[child_num]])
        child_num= child_num +1
        data = servermodule()
        dataparse = data.split('/')

        if dataparse[1] == "success":
          lightarr[num_index]=int(database[2])
          temperarr[num_index]=int(database[3])
          humidarr[num_index]=int(database[4])
          break
        #if dataparse[1] is fail, then send getMessage to  other chiled 

      num_index=num_index+1
    # after getting the humid & temper state, put   
    self.cursor.execute("SELECT ID FROM lighttable order by ID DESC limit 1")
    result = int(self.cursor.fetchone()[0])
    lightarr.insert(0, result+1)
    temperarr.insert(0, result+1)
    humidarr.insert(0, result+1)

    lightquery = 'insert into light values ('
    temperquery = 'insert into temper values ('
    humidquery = 'insert into humid values ('
    endquery = ''
    for i in range(0, self.total_num ):
      endquery += '?,'
    endquery += '?)'
    lightquery+= endquery
    temperquery+= endquery
    humidquery+= endquery
    self.cursor.execute(lightquery, lightarr)
    self.cursor.execute(temperquery, temperarr)
    self.cursor.execute(humidquery, humidarr)

    self.cursor.execute("SELECT *FROM usertemper_setting order by ID DESC limit 1")
    result = self.cursor.fetchone()
    base_high = result[1]
    base_row = result[2]

    tempTemper = ""
    tempHumid = ""
    
    for i in range (0, self.total_num):
      if tempearr[i] > base_high :
        tempTemper += "1"
      elif tempearr[i] < base_row :
        tempTemper += "0"
      else :
        tempTemper += "-1"

      if tempHumid[i] > 75:
        tempHumid += "0"
      else:
        tempHumid += "1"


    message = "put/%s/%s/%s" %("?", tempTemper, tempHumid)
  
  def putData(self, message):
    dataparse = message.split('/')
    print dataparse[1][0], dataparse[2][0], dataparse[3][0]
    
    for i in self.child:
      clientmodule(message, self.dic_addr[i])

    time.sleep(5)
  
  def setPrevention(self, value):
    self.prevention_Mode = value


  def lightSensing(self, que):
    while 1:
      '''data = GPIOlightRead()
      #we need to add mutex(the critical section is light_state)
      if data >= 0.6:
        self.light_state = 1
      else:
        self.light_state = 0'''

      if self.light_state == 0:
        self.light_state = 1
      else:
        self.light_state = 0

      time.sleep(3)

  def temperSensing(self, que):
    self.temper_state = 34
    while 1:
      '''data = GPIOtemperRead()
      #we ned to add mutex(the critical section is temper_state)
      self.temper_state = data'''

      if self.temper_state == 34:
        self.temper_state = 20
      else:
        self.temper_state = 34

      time.sleep(3)


  def humidSensing(self, que):
    self.humid_state = 90
    while 1:
      '''data = GPIOhumidRead()
      #we need to add mutex(the criticla section is humid_state)
      self.humid_state = data'''

      if self.temper_state == 90:
        self.temper_state = 30
      else:
        self.temper_state = 90

      time.sleep(3)

  def magnetSensing(self, que):
    tempolight = ""
    '''while 1:
      self.magnet_state = GPIOmagnetRead()
      if self.distance_flag == 0 && self.magnet_state == 1: # enter the room
        if self.prevention_Mode == 1:
          # turn on the speaker
          continue

        self.human_num = self.human_num + 1
        if self.human_num == 1:
          tempolight = ""
          
          # need to DB info
          prique = []
          for i in range(self.total_num):
            prique.append([])
            for j in range(self.total_num):
              prique[i].append(0)
          totalsum = 0
          for i in range(self.total_num -1):
            for j in range(i+1, self.total_num-1):
           
              query = "select count (*) from light where room%d == 1 and room%d == 1" %(i, j)
              self.cursor.execute(query)
              prique[i][j] = int(self.cursor.fetchone[0])
              totalsum+= prique[i][j]
          basenum = totalsum /(self.total_num*(self.total_num-1) /2)
          temparr = []
          for i in range(self.total_num):
            temparr.append(0)

          for i in range(self.total_num -1):
            for j in range(i+1, self.total_num-1):
              if prique[i][j]>basenum:
                temparr[i] = 1
                temparr[j] = 1
           
          # tomorrow 
          # db get oneline humid, temper
          templight = ""
          for i in temparr:
            if i == 1:
              templight += "1"
            else:
              templight += "0"

          message = "put/%s/%s/%s" %(templight, "?", "?")
          que.append(message)
      elif self.distance_flag == 1 && self.magnet_state == 1:
        self.human_num = self.human_num - 1
        tempolight = ""
        if self.human_num == 0:
          for i in total_num:
            tempolight +='0'
          #from DB get temper, window state and insert the message
          messages = "put/%s/%s/%s" %(tempolight,"?" ,"?" )
'''
    self.magnet_state = 0

  def infraredSensing(self, que):
    self.distance_flag = 0
    '''while 1:
      if GPIOtemperRead() < 50:
        self.distance_flag = 1
      else
        self.distance_flag = 0

'''

  



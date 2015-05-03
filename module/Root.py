from test_inquiry import *
import bluetooth
from clientmodule import *
from servermodule import *
import sys
import time
import datetime
import Queue

class Root():
  addr = []
  dic_addr ={}
  child = []
  number = -1
  light_state = 0
  magnet_state = 0
  window_state = 0
  temperature_state = 0
  search_index = 0
  total_num = 0
  count = 0
  autoMode = 0 #initial autoMode bit zero

  #construcotr
  def __init__(self):
    self.addr=getaddr_rssi()
    self.number = 0

  def setAutoMode(self):
    self.autoMode = 1

  def clearAutoMode(self):
    self.autoMode = 0

  def getAutoMode():
    return self.autoMode

  #make DAG 
  def makeDAG():
    message = "search/%d/%d" %(0, number)
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


  def getData():
    print "child : ", self.child
    
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
          #need to fill 
          #make algorithm
          #transport light state of numindex to DB
          if self.autoMode == 1:
            if int(dataparse[3]) < 18:
              # put the temper 22 to num_index
            elif int(dataparse[3]) > 30  :
              # put the temper 26 to num_index

          break
        #if dataparse[1] is fail, then send getMessage to  other chiled 

      num_index=num_index+1
    
  def FirstOpenDoor():
    # get the state from DB
    # put the light










  



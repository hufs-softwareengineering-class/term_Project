from test_inquiry import *
import bluetooth
from clientmodule import *
from servermodule import *
import sys
import time
import threading
import GPIOlightread
import GPIOtemperread
import GPIOhumidread

class myThread(threading.Thread):
  def __init__(self, node, sensingType):
    super.__init__(self)
    self.node = node
    self.sensingType = sensingType
    self.dictionary = {
        "light" : lightSensing,
        "temper" : temperSensing,
        "humid" : humidSensing, 
        }

  def run(self):
    self.dictionary[self.sensingType]()


class Node():
  addr = [] #list of address and rssi
  dic_addr = {} #address dictionary
  parent = [] #parent of myNode
  child = [] #child of myNOde
  number = -1 #myNumber

  get_target = -1 #store targetnumber
  indexflag = 0 #need to change when all child visit(get)
  light_state = 0 #store light state
  humid_state = 0 #store humid state
  temperature_state = 0 #store temperature state
  search_index = 0 #need to change when all child visit(search)
  
  count = 0 #current the number of node's of dag

  def __init__(self):
    self.addr = getaddr_rssi()

  def search(self, dataparse, address):
    if len(parent) is not 0:
      response = "searchres/%s" %(dataparse[1])
      clientmodule(response, address)
    else:
      self.parent.append(int(dataparse[2]))
      self.count = int(dataparse[1]) + 1
      self.number = self.count
      self.dic_addr[self.parent[0]] = address

      if len(addr) != 0:
        message = "search/%d/%d" %(self.count, self.number)
        clientmodule(message, self.addr[self.search_index].getaddr())
        self.search_index = self.search_index + 1

      else:
        message = "searchres/%d" %(self.count)
        clientmodule(message, address)


  def searchres(self, dataparse, address):
    if self.count != int(dataparse[1]) :
      self.child.append(self.count + 1)
      self.dic_addr[self.count + 1] = address
      self.count = int(dataparse[1])

    if self.search_index == len(self.addr):
      print "number", self.number
      print "parent : ", self.parent
      print "child : ", self.child
      message = "searchres/%d" %(int(dataparse[1]))
      clientmodule(message, self.dic_addr.get(int(self.parent[0])))

    else:
      message = "search/%d/%d" %(int(dataparse[1]), self.number)
      clientmodule(message, self.addr[self.search_index].getaddr())
      self.search_index = self.search_index + 1



  def get(self, dataparse, address):
    self.get_target = int(dataparse[1])
    if int(dataparse[1]) is self.number:
      message = "%s/%s/%d/%d/%d" %("getres","success",self.light_state,self.temperature_state, self.humid_state)

      clientmodule(message,self.dic_addr[self.parent[0]])

    elif len(self.child) is 0:
      #if this node is leaf node and incorrent number node
      #send fail message to parent
      message = "%s/%s/%d/%d/%d" %("getres", "fail", -1, -1, -1)

      clientmodule(message, self.dic_addr[self.parent[0]])

    elif int(dataparse[1]) in child:
      #if the target in child array
      child_index = self.child.index(int(dataparse[1]))
      message = "%s/%s" %(dataparse[0], dataparse[1])
      clientmodule(message, self.dic_addr[self.child[child_index]])


    else:
      #check the index flag
      #and then send message
      message = "%s/%s" %(dataparse[0], dataparse[1])
      clientmodule(message, self.dic_addr[self.child[self.indexflag]])
      self.indexflag = self.indexflag + 1



  def getres(self, dataparse, address):
    if dataparse[1] is "success":
      #if data is success
      message = "%s/%s/%s/%s/%s" %(dataparse[0], dataparse[1], dataparse[2], dataparse[3], dataparse[4])
      clientmodule(message, self.dic_addr[self.parent[0]])
      self.indexflag = 0

    else:
      #if data is fail
      if self.indexflag < len(self.child):
        #send get message other childs
        message = "%s/%d" %("get", self.get_target)
        clientmodule(message, self.dic_addr[self.child[self.indexflag]])
        self.indexflag = self.indexflag + 1

      else:
        #send fail(getres) message to parent, because already check all child
        message = "%s/%s/%s/%s/%s" %(dataparse[0], dataparse[1], dataparse[2], dataparse[3], dataparse[4])
        clientmodule(message, self.dic_addr[self.parent[0]])
        self.indexflag = 0


  def put(self, dataparse, address):
    # if state == -1, then current state maintain
    if dataparse[1] != "?":
      if dataparse[1][self.number] is "1":
        #turn on the light
      elif dataparse[1][self.number] is "0":
        #turn off the light
    # temperature state = {-1(unchange), 0(up temperature), 1(down temperature)}
    if dataparse[2] != "?":
      if dataparse[2][self.number] is "0":
        #turn on the temperature light blue

      elif dataparse[2][self.number] is "1":
        #turn on the temperature light red

    if dataparse[3] != "?":
      if dataparse[3][self.number] is "1":
        #open the window
      elif dataparse[3][self.number] is "0":
        #close the window

    
    message = "%s/%s/%s/%s" %(dataparse[0], dataparse[1], dataparse[2], dataparse[3])
    
    for i in child:
      clientmodule(message, dic_addr[i])
    #append


  def lightSensing(self):
    while 1:
      data = GPIOlightRead()
      #we need to add mutex(the critical section is light_state)
      if data >= 0.6:
        self.light_state = 1
      else:
        self.light_state = 0
      time.sleep(3)

  def temperSensing(self):
    while 1:
      data = GPIOtemperRead()
      #we ned to add mutex(the critical section is temper_state)
      self.temper_state = data

    time.sleep(3)


  def humidSensing(self):
    while 1:
      data = GPIOhumidRead()
      #we need to add mutex(the criticla section is humid_state)
      self.humid_state = data

    time.sleep(3)

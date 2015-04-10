from test_inquiry import *
import bluetooth
from clientmodule import *
from servermodule import *
import sys
import time

class Node():
  addr = [] #list of address and rssi
  dic_addr = {} #address dictionary
  parent = [] #parent of myNode
  child = [] #child of myNOde
  number = -1 #myNumber

  indexflag = 0 #need to change when all child visit(get)
  light_state = 0 #store light state
  window_state = 0 #store window state
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

  def get(self, dataparse, address):

  def getres(self, dataparse, address):

  def put(self, dataparse, address):

    

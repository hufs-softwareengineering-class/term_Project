import threading
import time


class myThread(threading.Thread):
  def __init__ (self, node):
    threading.Thread.__init__(self)
    self.node = node

  def run(self):
    print "starting"
    self.node.sensing()
    print "Exiting"


class Node():
  def __init__(self, name):
    self.name = name
    self.lightstate = 0

  def setlightstate(self, state):
    self.lightstate = state

  def getligtstate(self):
    return self.lightstate


  def sensing(self):
    while 1:
      self.lightstate = 1
      time.sleep(5)
      self.lightstate = 0
      time.sleep(5)
      print "sensing"

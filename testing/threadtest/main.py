from Node import *
import time , Queue

qu = []

if __name__ == "__main__":

  node = Node("Node1")
  qu.append('A')
  qu.append('B')
  qu.append('C')
  thread1 = myThread(node, qu)
  thread1.start()
  while 1:
    print "ligtstate : ", node.getligtstate()
    time.sleep(3)
    print qu


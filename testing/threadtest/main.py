from Node import *
import time


if __name__ == "__main__":

  node = Node("Node1")
  thread1 = myThread(node)
  thread1.start()
  while 1:
    print "ligtstate : ", node.getligtstate()
    time.sleep(3)


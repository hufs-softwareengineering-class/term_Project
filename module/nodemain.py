from Node import *
import sys
import time
import threading
from test_inquiry import *
from servermodule import *
from clientmodule import *

schemas = {
    "search" : search,
    "searcheres" : searchres,
    "get" : get,
    "getres" : getres,
    "put" : put
    }

if __name__ == "__main__":
  node = Node()
  lightSensingThread = myThread(node, "light")
  temperSensingThread = myThread(node, "temper")
  humidSensingThread = myThread(node, "humid")
  lightSensingThread.start()
  temperSensingThread.start()
  humidSensingThread.start()

  while 1:
    data = servermodule()
    dataparse = data.split('/')
    schema = dataparse[0]
    address = dataparse[len(dataparse)-1]
    node.schemas[schema](dataparse, address)


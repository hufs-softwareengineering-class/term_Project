import Node
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
node = Node()
th=threading.Thread(target = node.run())
th.start()
while 1:
  data = servermodule()
  dataparse = data.split('/')
  schema = dataparse[0]
  address = dataparse[len(dataparse)-1]
  node.schemas[schema](dataparse, address)


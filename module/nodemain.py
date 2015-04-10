import Node
import sys
import time
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

while 1:
  data = servermodule()
  dataparse = data.split('/')
  schema = dataparse[0]
  address = dataparse[len(dataparse)-1]
  node.schemas[schema](dataparse, address)


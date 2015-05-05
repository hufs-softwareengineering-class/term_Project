import threading

def hello():
  count = 100000
  while count>0:
    print "helloworld! %d" %count
    count = count -1

def hello2():
  count = 100000

  while count>0:
    count = count -1
    print "mainthread %d" %count

th = threading.Thread(target = hello())
th2 = threading.Thread(target = hello2())
th.run()
#th.start()
#th2.start()
th2.run()

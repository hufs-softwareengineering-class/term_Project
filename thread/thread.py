import thread

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


if __name__ == "__main__":
  thread.start_new_thread(hello, ())
  thread.start_new_thread(hello2, ())
  while 1:
    pass

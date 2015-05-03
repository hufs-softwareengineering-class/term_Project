from Root import *
import os, time, sys, Queue

pipe_naem = "pipefile"
Time = datetime.datetime.now()
timeList = []

if __name__ == "__main__":


  pipein = os.open(pipe_name, 'r')

  # Make Queeue
  queue = Queue()
  root = Root()
  root.makeDAG()
  
  #need to add the pipe module
  while 1:
    line = pipein.readline()[:-1]
    if ~pipe.empty(): # need to modify
      queue.put(line)
    else if pipe.empty(): #need to modify
      root.getData()
    else :
      text = queue.get()




from Root import *
import os, time, sys, Queue

pipe_naem = "pipefile"
Time = datetime.datetime.now()
timeList = []

if __name__ == "__main__":

  if not os.path.exists(pipe_name):
    os.mkfifo(pipe_name)

  pipein = os.open(pipe_name, 'r')

  # Make Queeue
  queue = Queue()
  root = Root()
  lightSensingThread = myThread(root, "light")
  temperSensingThread = myThread(root, "temper")
  humidSensingThread = myThread(root, "humid")
  magnetSensingThread = myThread(root, "magnet")
  root.makeDAG()
  
  #need to add the pipe module
  while 1:
    if ~pipein.empty(): # need to modify
      line = pipein.readline()[:-1]
      queue.put(line)
    else if pipein.empty(): #need to modify
      root.getData()
    else :
      text = queue.get()




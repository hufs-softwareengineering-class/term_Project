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
  lightSensingThread = myThread(root, "light", queue)
  temperSensingThread = myThread(root, "temper", queue)
  humidSensingThread = myThread(root, "humid", queue)
  magnetSensingThread = myThread(root, "magnet", queue)
  lightSensingThread.start()
  temperSensingThread.start()
  humidSensingThread.start()
  magnetSensingThread.start()
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




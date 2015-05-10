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
  queue = []
  root = Root()
  lightSensingThread = myThread(root, "light", queue)
  temperSensingThread = myThread(root, "temper", queue)
  humidSensingThread = myThread(root, "humid", queue)
  magnetSensingThread = myThread(root, "magnet", queue)
  infraredSensingThread = myThread(root, "infrared", queue)
  lightSensingThread.start()
  temperSensingThread.start()
  humidSensingThread.start()
  magnetSensingThread.start()
  root.makeDAG()
  
  #need to add the pipe module
  while 1:
    if ~pipein.empty(): # need to modify
      line = pipein.readline()[:-1]
      #need to parsing the json and make meassage , then enqueue the message to the queue
      #need to parsing the mode 
      if schema == "prevenmode":
        prevalue = #parsing the json 
        root.setPrevention(prevalue)
        continue
      message = #parisng the jsonand make the message (need to access the DB data) 
      queue.append(message)

    else if queue.len() == 0: #need to modify
      root.getData()
    else :
      text = queue.pop()
      root.putData(text)
      




import os, time, sys

def pipeprocess(ipcque, pipe_name):
  if not os.path.exists(pipe_name):
    os.mkfifo(pipe_name)

  pipein = open(pipe_name , 'r')

  while True:
    line = pipein.readline()[:-1]
    print "pipe got message from web"
    ipcque.put(line)

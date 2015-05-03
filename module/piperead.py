import os, time, sys
pipe_name = 'pipefile'
if not os.path.exists(pipe_name):
  os.mkfifo(pipe_name)

pipein = open(pipe_name, 'r')
while True:
  line = pipein.readline()
  print "pipe got %s at %s " %(line, time.time())




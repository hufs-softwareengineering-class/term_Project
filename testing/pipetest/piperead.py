import os, time, sys
pipe_name = 'pipefile'
if not os.path.exists(pipe_name):
  os.mkfifo(pipe_name)

pipein = open(pipe_name, 'r')
print "hello"
while True:
  line = pipein.readline()[:-1]
  if line == "":
    print "nothing"
    time.sleep(3)
  print "pipe got %s at %s " %(line, time.time())



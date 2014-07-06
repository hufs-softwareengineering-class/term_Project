import os, time, sys
pipe_name = 'pipefile'
if not os.path.exists(pipe_name):
  os.mkfifo(pipe_name)

pipein = os.open(pipe_name, os.O_NONBLOCK | os.O_RDONLY)
print "hello"
while True:
  line = pipein.readline()[:-1]
  if line == "":
    print "nothing"
    time.sleep(3)
  print "pipe got %s at %s " %(line, time.time())



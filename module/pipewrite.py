import os, time, sys
pipe_name = 'pipefile'
if not os.path.exists(pipe_name):
  os.mkfifo(pipe_name)


pipeout = os.open(pipe_name, os.O_WRONLY)

print "hello"
'''
counter = 0

while True:
  time.sleep(1)
  os.write(pipeout, 'Number %03d\n' % counter)
  counter = (counter + 1) %5
'''


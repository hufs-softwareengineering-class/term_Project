from flask import Flask
import os 
pipe_name = 'pipefile'


app =Flask(__name__)



@app.route('/')
def hello_world():
  os.write(pipeout, 'hello wold\n')
  return 'hello wotld!'

if __name__ == '__main__' :
  if not os.path.exists(pipe_name):
    os.mkfifo(pipe_name)

  pipeout = os.open(pipe_name, os.O_WRONLY)
  app.run()

from Root import *
import os, time, sys, Queue


if __name__ == "__main__":


  # Make Queeue
  queue = Queue()
  root = Root()
  root.makeDAG()


  #need to add the pipe module


  if ~pipe.empty(): # need to modify
    queue.put(text)
  else if pipe.empty(): #need to modify
    root.getData()
  else :
    text = queue.get()




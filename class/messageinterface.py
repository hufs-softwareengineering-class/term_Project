#interface for message
from abc import ABCMeta, abstractmethod

class messageinterface(object):
  __metaclass__ = ABCMeta
 
  def __init__(self):

  @abstractmethod #abstract method
  def Doing_search(self): pass

  @abstractmethod #abstract method
  def Doing_searchres(self): pass

  @abstractmethod #abstract method
  def Doing_get(self): pass
   
  @abstractmethod #abstract method
  def Doing_getres(self): pass
  
  @abstractmethod #abstract method
  def Doing_put(self): pass

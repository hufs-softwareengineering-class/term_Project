#client class
import sys
import bluetooth
import time

class clientClass(self):
  sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
  port = 0x1001
  message = " "
  bt_addr = " "
  def __init__ (self):
    
  def setmessage(self, message):
    self.message = message
  def setbt_addr(self, addr):
    self.bt_addr = addr
  
  def sendmessage(self ):
    time.sleep(1)
    self.sock.connect((self.bt_addr, self.port))
    print ("connected. type stuff")
    self.sock.send(self.message)
    print ("send message : %s " %self.message)
    self.sock.close()


    

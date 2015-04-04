class BTaddr():
  addr = " "
  rssi = 0
  def __init__(self, in_addr, in_rssi):
    self.addr = in_addr
    self.rssi = in_rssi
  def setaddr(self,in_addr):
    self.addr = in_addr
  
  def setrssi(self,in_rssi):
    self.rssi = in_rssi
  
  def getaddr(self ):
    return self.addr
  
  def getrssi(self):
    return self.rssi


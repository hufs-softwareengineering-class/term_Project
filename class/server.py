import bluetooth

class serverClass(self):
  server_sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
  port = 0x1001
  recive =" "

  def __init__(self):

  def listenServer(self):
    server_sock.bind(("",port))
    server_sock.listen(1)
    client_sock,address = server_sock.accept()
    print("Accepted connection form ",address)
    data = client_sock.recv(1024)
    print("Data received:", data)
    recive = "%s/%s" %(data, str(address[0]))
    setrecive(recive)

  def setrecive(self,recivemsg):
    self.reive = recivemsg

  def getrecive(self)
    print("Return data is : ",self.recive)
    return self.recive
  


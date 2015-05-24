import bluetooth

def servermodule ():
  
  server_sock=bluetooth.BluetoothSocket( bluetooth.L2CAP )

  port = 0x1001

  server_sock.bind(("",port))
  server_sock.listen(1)

  client_sock,address = server_sock.accept()
  print("Accepted connection from ",address)

  data = client_sock.recv(1024)
  print("Data received:", data)
  recive = "%s/%s" %(data, str(address[0]))
  return recive

if __name__ == "__main__":
    servermodule()

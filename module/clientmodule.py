# file: l2capclient.py
# desc: Demo L2CAP client for bluetooth module.
# $Id: l2capclient.py 524 2007-08-15 04:04:52Z albert $

import sys
import bluetooth
import time
def clientmodule(message, addr):
  time.sleep(3)
  if sys.version < '3':
    input = raw_input

  sock=bluetooth.BluetoothSocket(bluetooth.L2CAP)
  bt_addr=addr
  print bt_addr
  port = 0x1001

  print("trying to connect to %s on PSM 0x%X" % (bt_addr, port))

  sock.connect((bt_addr, port))

  print("connected.  type stuff")
  sock.send(message)
  print("send message : %s "%message)
  sock.close()


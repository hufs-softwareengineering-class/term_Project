# performs a simple device inquiry, followed by a remote name request of each
# discovered device

import os
import sys
import struct
import bluetooth
import bluetooth._bluetooth as bluez
from btaddr import BTaddr

mac_info = []

def printpacket(pkt):
    for c in pkt:
        sys.stdout.write("%02x " % struct.unpack("B",c)[0])
    print 


def read_inquiry_mode(sock):
    """returns the current mode, or -1 on failure"""
    # save current filter
    old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)

    # Setup socket filter to receive only events related to the
    # read_inquiry_mode command
    flt = bluez.hci_filter_new()
    opcode = bluez.cmd_opcode_pack(bluez.OGF_HOST_CTL, 
            bluez.OCF_READ_INQUIRY_MODE)
    bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
    bluez.hci_filter_set_event(flt, bluez.EVT_CMD_COMPLETE);
    bluez.hci_filter_set_opcode(flt, opcode)
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, flt )

    # first read the current inquiry mode.
    bluez.hci_send_cmd(sock, bluez.OGF_HOST_CTL, 
            bluez.OCF_READ_INQUIRY_MODE )

    pkt = sock.recv(255)

    status,mode = struct.unpack("xxxxxxBB", pkt)
    if status != 0: mode = -1

    # restore old filter
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, old_filter )
    return mode

def write_inquiry_mode(sock, mode):
    """returns 0 on success, -1 on failure"""
    # save current filter
    old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)

    # Setup socket filter to receive only events related to the
    # write_inquiry_mode command
    flt = bluez.hci_filter_new()
    opcode = bluez.cmd_opcode_pack(bluez.OGF_HOST_CTL, 
            bluez.OCF_WRITE_INQUIRY_MODE)
    bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
    bluez.hci_filter_set_event(flt, bluez.EVT_CMD_COMPLETE);
    bluez.hci_filter_set_opcode(flt, opcode)
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, flt )

    # send the command!
    bluez.hci_send_cmd(sock, bluez.OGF_HOST_CTL, 
            bluez.OCF_WRITE_INQUIRY_MODE, struct.pack("B", mode) )

    pkt = sock.recv(255)

    status = struct.unpack("xxxxxxB", pkt)[0]

    # restore old filter
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, old_filter )
    if status != 0: return -1
    return 0

def device_inquiry_with_with_rssi(sock):
    # save current filter
    old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)

    # perform a device inquiry on bluetooth device #0
    # The inquiry should last 8 * 1.28 = 10.24 seconds
    # before the inquiry is performed, bluez should flush its cache of
    # previously discovered devices
    flt = bluez.hci_filter_new()
    bluez.hci_filter_all_events(flt)
    bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, flt )

    duration = 4
    max_responses = 255
    cmd_pkt = struct.pack("BBBBB", 0x33, 0x8b, 0x9e, duration, max_responses)
    bluez.hci_send_cmd(sock, bluez.OGF_LINK_CTL, bluez.OCF_INQUIRY, cmd_pkt)

    results = []

    done = False
    while not done:
        pkt = sock.recv(255)
        ptype, event, plen = struct.unpack("BBB", pkt[:3])
        if event == bluez.EVT_INQUIRY_RESULT_WITH_RSSI:
            pkt = pkt[3:]
            nrsp = struct.unpack("B", pkt[0])[0]
            for i in range(nrsp):
                addr = bluez.ba2str( pkt[1+6*i:1+6*i+6] )
                rssi = struct.unpack("b", pkt[1+13*nrsp+i])[0]
                results.append( ( addr, rssi ) )
                print "[%s] RSSI: [%d]" % (addr, rssi)
                BTinfo = BTaddr(addr, rssi)
                mac_info.append(BTinfo)
        elif event == bluez.EVT_INQUIRY_COMPLETE:
            done = True
        elif event == bluez.EVT_CMD_STATUS:
            status, ncmd, opcode = struct.unpack("BBH", pkt[3:7])
            if status != 0:
                print "uh oh..."
                printpacket(pkt[3:7])
                done = True
        elif event == bluez.EVT_INQUIRY_RESULT:
            pkt = pkt[3:]
            nrsp = struct.unpack("B", pkt[0])[0]
            for i in range(nrsp):
                addr = bluez.ba2str( pkt[1+6*i:1+6*i+6] )
                results.append( ( addr, -1 ) )
                print "[%s] (no RRSI)" % addr
        else:
            print "unrecognized packet type 0x%02x" % ptype
	    print "event ", event


    # restore old filter
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, old_filter )

    return results
def inquriy_run():
  dev_id = 0
  try:
      sock = bluez.hci_open_dev(dev_id)
  except:
      print "error accessing bluetooth device..."
      sys.exit(1)

  try:
      mode = read_inquiry_mode(sock)
  except Exception, e:
      print "error reading inquiry mode.  "
      print "Are you sure this a bluetooth 1.2 device?"
      print e
      sys.exit(1)
  print "current inquiry mode is %d" % mode

  if mode != 1:
      print "writing inquiry mode..."
      try:
          result = write_inquiry_mode(sock, 1)
      except Exception, e:
          print "error writing inquiry mode.  Are you sure you're root?"
          print e
          sys.exit(1)
      if result != 0:
          print "error while setting inquiry mode"
      print "result: %d" % result

  device_inquiry_with_with_rssi(sock)
#  for info in mac_info:
#    print "addr : %s rssi : %s " %(info.getaddr(), info.getrssi())
  return mac_info

def getaddr_rssi():
  listmac = inquriy_run()
  sortmac = sorted(listmac, key=lambda x: x.rssi)

  newmac = []
  newmac.append(sortmac.pop())
  while 1:
    if len(sortmac) is 0:
      break
    infopop =sortmac.pop()
    if infopop.getaddr() == newmac[len(newmac)-1].getaddr():
      continue
    else: 
      newmac.append(infopop)
  lastmac =[]
  flag = 0
  for info in newmac:
    name = bluetooth.lookup_name(info.getaddr(), 10)
    print "addr -> %s, name -> %s" %(info.getaddr(), name)
    for info2 in lastmac:
      if info2.getaddr() == info.getaddr():
        flag = 1
        break
      else:
        flag = 0
    if flag == 1:
      continue

    if name == "arm-0":
      if info.getrssi() >= -80:
        lastmac.append(info)

  for info in lastmac:
    print "addr : %s rssi : %s " %(info.getaddr(), info.getrssi())

  return lastmac
  

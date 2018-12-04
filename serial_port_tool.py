# A simple tool for test uart

import argparse
import serial
import binascii
import threading
import time
import re,sys
import signal

__version__ = "1.0.0"


def sigint_handler(signum, frame):
    global is_sigint_up
    is_sigint_up = True
    print 'catched interrupt signal!'

signal.signal(signal.SIGINT, sigint_handler)
#signal.signal(signal.SIGHUP, sigint_handler)
signal.signal(signal.SIGTERM, sigint_handler)
is_sigint_up = False

def print_opcode_info(packet):
    returnValue = []
	
    print packet
    return returnValue


def read_from_port(serPort):
    global cmInfoOutPut
    while True:
        if is_sigint_up:
            print "Exit"
            break
        if (serPort.inWaiting()):
            opCode = 0
            status = 'NULL'
            incoming_packet = []
            rtn_value = []
            print "--------------------- Rx Host Msg --------------------------"
            while (serPort.inWaiting()):
                data_str = str(serPort.read(serPort.inWaiting()).encode('hex'))
                data_str = [data_str[i:i + 2] for i in range(0, len(data_str), 2)]
                incoming_packet += data_str

                time.sleep(0.01)

            rtn_value = print_opcode_info(incoming_packet)
            if (rtn_value != []):
                cmInfoOutPut = rtn_value
            print "-----------------------------------------------"

  

def sendMsg(com, txMsg):

    msg = bytearray(txMsg)
    print "Outgoing: "+binascii.hexlify(msg)
    com.write(msg)


def main():
    print '\n##### Now You Can Start to Debug The Serial Port! #####'
    while (1):
        try:
            txStr = [int(n,0) for n in raw_input().encode(encoding='UTF-8',errors='strict').split()]
            sendMsg(host1, txStr)
            if is_sigint_up:
                print "Exit"
                break
        except ValueError:
            print 'Input Value Error! Useage: [0x01 0x1d 0xfc 0x01 0x00] or [01 128 255 13]'
    time.sleep(.1)



def parse_args():
    script_description = "Serial Port Debug Tool for Windows"
    parser = argparse.ArgumentParser(prog='serial_cmd_host',
                                                                     description=script_description)
    parser.add_argument("-v", "--version", action="version",
                                            version="%(prog)s " + __version__)
    parser.add_argument("host_port", default='', nargs='?', help="ComPort of Host_Test Device")

    args = parser.parse_args()

    return args

def version_control():
    print sys.version
    if sys.version[:3] != "2.7":
            raise Exception("Must be using Python 2.7!")

if __name__ == '__main__':
    version_control()
    rtn_args = parse_args()

    if(len(sys.argv) < 2):
        print '\nUsing Default Hardcoded Values: '
        print 'or enter 1 default(host_port) arguments.'
        print 'See -h help.\n'
        #set your own hard coded com ports
        host_port = 'COM8'

        print "Host comport is: "+host_port

    else:
        host_port = rtn_args.host_port
 
        print "\nHost comport is: "+host_port


    #Kick off a thread for each com to monitor Rx data over UART
    host1 = serial.Serial(port=host_port,baudrate=115200)
    thread1 = threading.Thread(target=read_from_port, args=(host1,))
    thread1.start()

    main()

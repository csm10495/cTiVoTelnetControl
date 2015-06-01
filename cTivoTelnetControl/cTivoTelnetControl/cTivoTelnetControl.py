"""
cTivoTelnetControl - a solution for controlling a TiVo over the internet
Converts a single key press into a command for a TiVo box
Charles Machalow - MIT License
"""

import telnetlib  #for telnet connection
import os         #for os.linesep (\n vs \r\n)
import sys        #for args
import getch      #local file for getch in Windows and Unix
import socket     #for socket.error


#makes connection to the given TiVo ip, port on default TiVo port
#returns the telnetlib.Telnet object, used to hold the connection
def connect(ip, port=31339):
    tn = telnetlib.Telnet(ip, str(port))
    return tn

#returns a dictionary from keychar to telnet command
#expects a RemoteToKeyMappings.txt
def getKeyToTelnet():
    d = {}
    with open('RemoteToKeyMappings.txt', 'r') as file:
        for line in file: 
            vals = line.split('\t')
            #vals[0] is the remote button, not used by code
            #makes the file more human readable
            d[vals[1]] = vals[2].rstrip()
    return d

#main
if __name__ == "__main__":
    port = 31339
    ip = -1
    
    #args handling
    if len(sys.argv) == 3:
        port = sys.argv[2]
        ip = sys.argv[1]
        tn = connect(ip, port)
    elif len(sys.argv) == 2:
        ip = sys.argv[1]
        tn = connect(ip)
    else:
        print("Incorrect script args")
        print("usage: python cTivoTelnetControl.py ip <port=31339>")
        sys.exit(0)

    keydict = getKeyToTelnet()

    print("listening for keypresses...")

    #go in key listening loop, send command as needed
    while True:
        try:
            c = getch.getch().decode("ascii")
        except UnicodeDecodeError:
            print("Can't decode that key into binary, not usable")
            #get one more key because arrows may be two seperate getch calls
            getch.getch().decode("ascii")
            continue

        if c not in keydict:
            print(c + " not in keydict, exiting...")
            break

        telnet_cmd = keydict[c] + os.linesep
        print ("recv'd \"" + c + "\" sending:" + telnet_cmd + " to " + str(ip) + ":" + str(port))

        try:
            tn.write(str.encode(telnet_cmd))
        except socket.error:
            print ("lost connection, reconnecting")
            tn = connect(ip, port) 
            tn.write(str.encode(telnet_cmd))

    tn.close()

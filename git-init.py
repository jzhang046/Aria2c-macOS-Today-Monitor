import xmlrpclib
import socket
import sys
from pprint import pprint

#This script is used to show aria2c download progress at macOS notification today. 
#To be run in Today-Scripts, https://github.com/falkvw/Today-Scripts. 
#Today-Scripts does not support real time update of scripts, 
#thus, the output of this script is static. 
#It will be run everytime when notification center is actived. 

def printProgressBar(progress):
    #This function is used to print a progress bar. 
    #This bar is static. 
    l = 37
    #Total length changed to 37 due to font changed to Menlo-Regular 11. 
    for i in range(0, int(round(l*progress))):
        sys.stdout.write('#')
    for i in range(int(round(l*progress)) + 1, l + 1):
        sys.stdout.write('-')

    sys.stdout.write('\n')


def printItems(type, source):
    #This function is to print a certain type of missions. 
    for item in type:
        gid = item['gid']
    
        speed = source.aria2.tellStatus(token, gid, ['downloadSpeed'])
        speed = speed['downloadSpeed']

        progress = source.aria2.tellStatus(token, gid, ['totalLength', 'completedLength'])
        ttL = int(progress['totalLength'])
        cpltL = int(progress['completedLength'])    

        filess = source.aria2.tellStatus(token, gid, ['files']) 
        filess = filess['files']
        filess = filess[0]
        path = filess['path']
        name = path[26:]

        print(name[-36:])
        print('Speed: %.2fKB/s' % (float(speed)/1024))
        if ttL != 0:
            print('Completed: %.2f%%' % (float(cpltL)/ttL*100))
            printProgressBar(float(cpltL)/ttL)
        else:
            print('ERROR!')
        print(' ')


s = xmlrpclib.ServerProxy('http://localhost:port/rpc')
token = 'token:$$token$$’
socket.setdefaulttimeout(0.5)

try:
    tmp=s.aria2.getGlobalStat(token)
except socket.error: 
    print('Connection FAILED')
    socket.setdefaulttimeout(None)
    sys.exit()

socket.setdefaulttimeout(None)
active = s.aria2.tellActive(token, ['gid'])
waiting = s.aria2.tellWaiting(token, -1, 2, ['gid'])
stopped = s.aria2.tellStopped(token, -1, 2, ['gid'])

print('-----------------Active-----------------\n')
printItems(active, s)
print('\n-----------------Waiting----------------\n')
printItems(waiting, s)
print('\n-----------------Stopped----------------\n')
printItems(stopped, s)

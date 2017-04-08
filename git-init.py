import xmlrpclib
import socket
import sys
import math
#from pprint import pprint

#This script is used to show aria2c download progress at macOS notification today. 
#To be run in Today-Scripts, https://github.com/falkvw/Today-Scripts. 
#Today-Scripts does not support real time update of scripts, 
#thus, the output of this script is static. 
#It will be run everytime when notification center is actived. 

def printProgressBar(progress):
    #This function is used to print a progress bar. 
    #This bar is static. 
    l = 37
    for i in range(0,int(round(l*progress))):
        sys.stdout.write('\033[100m \033[0m')
        #Dark grey. This will look darker than black ([40m). 

    for i in range(int(round(l*progress)) + 1, l + 1):
        sys.stdout.write('\033[44m \033[0m')
        #Blue. 

    sys.stdout.write('\n')
    #Today scripts only supports ASCII characters and ANSI colors. 


def convSign(length):
    #To limit the int part to occupy less than 4 places, 
    #use this instead of '< math.pow(1024, *)'

    if length < 1000:
        #less than 1000B
        rtn = '%.2fB' % float(length)
    elif length < math.pow(1024, 1) * 1000:
        #less han 1000KB
        rtn = '%.2fKB' % (float(length) / math.pow(1024, 1))
    elif length < math.pow(1024, 2) * 1000:
        #less than 1000MB
        rtn = '%.2fMB' % (float(length) / math.pow(1024, 2))
    elif length < math.pow(1024, 3) * 1000:
        #less than 1000GB
        rtn = '%.2fGB' % (float(length) / math.pow(1024, 3))
    else:
        rtn = 'TooLarge' 
    
    return rtn


def printItems(type, source, token):
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
        #Omit the front part of the path, only leave filename. 
        
        status = source.aria2.tellStatus(token, gid, ['status'])
        status = status['status']
        #Get donwload status, e.g. paused, complete. 

        print(name[-36:])#Limit the filelength. 
        sys.stdout.write('Speed: \033[1m%.2fKB/s\033[0m  ' % (float(speed)/1024))
        sys.stdout.write('%s\n' % status)
        #Blod font for speed. 

        #Error handling for file length. 
        #To avoid devided by 0. 
        if ttL != 0:
            sys.stdout.write('Completed: \033[1m%.2f%%\033[0m' % (float(cpltL)/ttL*100))
            #Bold font for completed percentage. 
            sys.stdout.write('  %(cpltlC)s/%(ttlC)s\n' % {'ttlC':convSign(ttL), 'cpltlC':convSign(cpltL)});
            printProgressBar(float(cpltL)/ttL)
        else:
            print('ERROR!')

        print(' ')#Print a new line. 


def resetAndExit():
    socket.setdefaulttimeout(None)
    sys.exit()

s = xmlrpclib.ServerProxy('http://localhost:port/rpc')
token = 'token:$$token$$’
socket.setdefaulttimeout(2)
#timeout too short will result in frequent timeout error. 

try:
    tmp=s.aria2.getGlobalStat(token)
except socket.error: 
    print('Connection FAILED')
    resetAndExit()
except xmlrpclib.Fault as err:
    print(err.faultString)
    resetAndExit()
except:
    print('Unknown Error')
    resetAndExit()

socket.setdefaulttimeout(None)
active = s.aria2.tellActive(token, ['gid'])
waiting = s.aria2.tellWaiting(token, -1, 2, ['gid'])
stopped = s.aria2.tellStopped(token, -1, 2, ['gid'])

print('-----------------Active-----------------\n')
printItems(active, s, token)
print('\n-----------------Waiting----------------\n')
printItems(waiting, s, token)
print('\n-----------------Stopped----------------\n')
printItems(stopped, s, token)

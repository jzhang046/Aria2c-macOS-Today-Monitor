import xmlrpclib
import sys
from pprint import pprint

def printProgressBar(progress):
    l = 40
    for i in range(0, int(round(l*progress))):
        sys.stdout.write('#')
    for i in range(int(round(l*progress)) + 1, l + 1):
        sys.stdout.write('-')

    sys.stdout.write('\n')

s = xmlrpclib.ServerProxy('http://localhost:port/rpc')
token = 'token:$$token$$’

active = s.aria2.tellActive(token, ['gid'])

for item in active:
    gid = item['gid']
    
    speed = s.aria2.tellStatus(token, gid, ['downloadSpeed'])
    speed = speed['downloadSpeed']

    progress = s.aria2.tellStatus(token, gid, ['totalLength', 'completedLength'])
    ttL = int(progress['totalLength'])
    cpltL = int(progress['completedLength'])    

    filess = s.aria2.tellStatus(token, gid, ['files']) 
    filess = filess['files']
    filess = filess[0]
    path = filess['path']
    name = path[26:]

    print(name)
    print('Speed: %.2fKB/s' % (float(speed)/1024))
#    pprint(filess)
#    print(cpltL)
#    print(ttL)
    print('Completed: %.2f%%' % (float(cpltL)/ttL*100))
    printProgressBar(float(cpltL)/ttL)



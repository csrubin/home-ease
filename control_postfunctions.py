import serial
import time, datetime
from gpiozero import LED

rfid = serial.Serial('/dev/ttyUSB0', 9600)
ledB = LED(21)
ledY = LED(16)
ledG = LED(15)
ledR = LED(14)


def main():

    tag = ''
    bluet = '\x025500E1BFEAE1\r\n\x03'
    #greent =
    yellowt = '\x025500E0FCE1A8\r\n\x03'
    greent = '\x025500E0FCE1A8\r\n\x03'
    redt = '\x025500E0FCE1A8\r\n\x03'


    rfidtags = ['\x025500E1BFEAE1\r\n\x03', '\x025500E0FCE1A8\r\n\x03', 'filler', 'filler']
    rfidPins= [ledB,ledY,ledG,ledR]
    rfidName = ['blue', 'yellow', 'green', 'red']
    TimeIn = [0,0,0,0]
    TimeOut = [0,0,0,0]
    TimeHomeTotal = [0,0,0,0]
    TimeAwayTotal = [0,0,0,0]
    TimeHome = [0,0,0,0]
    TimeAway = [0,0,0,0]
    home = [0,0,0,0]

    while True:
        print('Havent read\n')
        while True:
            data = rfid.read()
            tag = tag + data.decode('utf-8')
            for i in range (0,3):
##                print('check if tag =' + rfidtags[i])
                if (tag == rfidtags[i]):
                    rfidSeen(i,home,TimeOut,TimeHome,TimeHomeTotal,rfidPins,TimeIn,TimeAway,TimeAwayTotal)
                    if home[i] == True:
                        print(rfidName[i] + ' is Home \n \n')
                        
                    else:
                        print(rfidName[i] + ' is Away \n \n')
                        
                    tag=''
                    break
        

def rfidSeen(tag,home,TimeOut,TimeHome,TimeHomeTotal,rfidPins,TimeIn,TimeAway,TimeAwayTotal):
    #am leaving home rn
    if home[tag] == True:
        TimeOut[tag] = time.time()
        TimeHome[tag] = TimeOut[tag]-TimeIn[tag]
        TimeHomeTotal[tag] = TimeHomeTotal[tag] + TimeHome[tag]
        home[tag] = 0
            #just got home rn    
    else:
        TimeIn[tag] = time.time()
        TimeAway[tag] = TimeIn[tag]-TimeOut[tag]
        TimeAwayTotal[tag] = TimeAwayTotal[tag] + TimeAway[tag]
        home[tag] = 1
    rfidPins[tag].toggle()
    return;
        
def printPerson(tag):

    if home[tag] == True:
        print(rfidName[tag] + ' is Home \n \n')
    else:
        print(rfidName[tag] + ' is Away \n \n')
    
    print('TimeHomeTotal' + TimeHomeTotal[tag] + '\n')
    print('TimeAwayTotal' + TimeAwayTotal[tag] + '\n')
    print('TimeHome' + TimeHome[tag] + '\n')
    print('TimeAway' + TimeAway[tag] + '\n')
    return;

if __name__=='__main__':
    main()
    
    

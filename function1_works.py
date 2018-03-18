import serial
import time, datetime
from gpiozero import LED
import RPi.GPIO as IO
import requests


url = 'http://makeohio2018.kevinbartchlett.com/collectData.php'
rfid = serial.Serial('/dev/ttyUSB0', 9600)
ledB = LED(21)
ledY = LED(16)
ledG = LED(15)
ledR = LED(12)
#Initially no one is home
initTime = time.time()

def main():

    tag = ''
    bluet = '\x025500E1BFEAE1\r\n\x03'
    yellowt = '\x025500E0FCE1A8\r\n\x03'
    greent = '\x025500E0FCE1A8\r\n\x03'
    redt = '\x025500E0FCE1A8\r\n\x03'


    rfidtags = ['\x025500E1BFEAE1\r\n\x03', '\x025500E0FCE1A8\r\n\x03', 'filler', 'filler']
    rfidPins= [ledB,ledY,ledG,ledR]
    rfidName = ['Logan Whitaker', 'Kevin Bartchlett', 'Trever Vogel', 'Bemberg']
    TimeIn = [initTime,initTime,initTime,initTime]
    TimeOut = [initTime,initTime,initTime,initTime]
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
#                print('check if tag =' + rfidtags[i])
                if (tag == rfidtags[i]):
                    rfidSeen(i,rfidName,home,TimeOut,TimeHome,TimeHomeTotal,rfidPins,TimeIn,TimeAway,TimeAwayTotal,rfidtags)             
                    tag=''
                    break
##                else:
##                    for j in range (0,6):
##                        for h in range (0,3):
##                            rfidPins[h].toggle()
##                            time.sleep(.25)
                
        

def rfidSeen(tag,rfidName,home,TimeOut,TimeHome,TimeHomeTotal,rfidPins,TimeIn,TimeAway,TimeAwayTotal,rfidtags):
    #am leaving home rn
    if home[tag] == True:
        print('fuck')
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
    sendPHP(rfidtags, rfidName,home,tag)
    printPerson(tag,rfidName, home,TimeHome,TimeHomeTotal,TimeAway,TimeAwayTotal)
    return;
        
def printPerson(tag,rfidName, home,TimeHome,TimeHomeTotal,TimeAway,TimeAwayTotal):

    if home[tag] == True:
        print('\n' + rfidName[tag] + ' is Home \n')
    else:
        print('\n' + rfidName[tag] + ' is Away \n')
    
    print('TimeHomeTotal: ' + str(TimeHomeTotal[tag]))
    print('TimeAwayTotal: ' + str(TimeAwayTotal[tag]))
    print('TimeHome: ' + str(TimeHome[tag]))
    print('TimeAway: ' + str(TimeAway[tag]))
    return;

def sendPHP(rfidtags, rfidName,home,tag):
    payload = {'name': rfidName[tag],'rfidID': rfidtags[tag], 'status': home[tag]}
    r = requests.post(url,data=payload)
    return;

if __name__=='__main__':
    main()
    
    


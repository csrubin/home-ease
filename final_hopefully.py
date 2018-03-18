#!/usr/bin/python3

import serial
import time, datetime
import requests
from RPLCD import *
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[40,38,36,32,33,31,29,15])
url = 'http://makeohio2018.kevinbartchlett.com/collectData.php'
rfid = serial.Serial('/dev/ttyUSB0', 9600)
ledB = GPIO.setup(22,GPIO.OUT)
ledY = GPIO.setup(16,GPIO.OUT)
ledG = GPIO.setup(18,GPIO.OUT)
ledR = GPIO.setup(12,GPIO.OUT)
buzzer = GPIO.setup(7,GPIO.OUT)
Buzz=GPIO.PWM(7,440)
#Initially no one is home
initTime = time.time()

def main():

    tag = ''
    counter = 0
    rfidtags = ['\x025500E1BFEAE1\r\n\x03', '\x025500E0FCE1A8\r\n\x03', '\x025500E175CB0A\r\n\x03', '\x025500E0C78BF9\r\n\x03']
    rfidPins= [22,16,18,12]
    rfidName = ['Logan Whitaker', 'Kevin Bartchlett', 'Connor Rubin', 'Bemberg']
##  fidName = ['blue', 'yellow', 'green', 'Black']
    rfidNick = ['LW', 'KB', 'CR', 'BM']
    TimeIn = [initTime,initTime,initTime,initTime]
    TimeOut = [initTime,initTime,initTime,initTime]
    TimeHomeTotal = [0,0,0,0]
    TimeAwayTotal = [0,0,0,0]
    TimeHome = [30000,3000,200,7000]
    TimeAway = [30000,3000,200,7000]
    home = [0,0,0,0]

    while True:
        GPIO.output(rfidPins[0],GPIO.LOW)
        GPIO.output(rfidPins[1],GPIO.LOW)
        GPIO.output(rfidPins[2],GPIO.LOW)
        GPIO.output(rfidPins[3],GPIO.LOW)
        lcd.write_string('READY TO GO!')
        while True:
            data = rfid.read()
            tag = tag + data.decode('utf-8')
            
            for i in range (0,4):                
                if (tag == rfidtags[i]):
                    rfidSeen(i,rfidName,home,TimeOut,TimeHome,TimeHomeTotal,rfidPins,TimeIn,TimeAway,TimeAwayTotal,rfidtags,rfidNick)             
                    tag=''
                    counter=0
                    break
                counter=counter+1
                if (tag != '') & (int(counter)>63):
                    tag=''
                    lcd.clear()
                    lcd.write_string('ERROR RFID NOT  VALID')
                    counter=0
                    Buzz.start(50)
                    for j in range (0,2):
                        for h in range (0,4):
                            GPIO.output(rfidPins[h],GPIO.HIGH)
                            time.sleep(.25)
                            GPIO.output(rfidPins[h],GPIO.LOW)
                            time.sleep(.25)
                    Buzz.stop() 
                    for i in range (0,4):
                        if home[i]:
                            GPIO.output(rfidPins[i],GPIO.HIGH)   
                        else:
                            GPIO.output(rfidPins[i],GPIO.LOW)
                    printPerson(home,TimeHome,TimeAway,rfidNick)
                    break
                
                    
        

def rfidSeen(tag,rfidName,home,TimeOut,TimeHome,TimeHomeTotal,rfidPins,TimeIn,TimeAway,TimeAwayTotal,rfidtags,rfidNick):
    #am leaving home rn
    if home[tag] == True:
        TimeOut[tag] = time.time()
        TimeHome[tag] = TimeOut[tag]-TimeIn[tag]
        TimeHomeTotal[tag] = TimeHomeTotal[tag] + TimeHome[tag]
        home[tag] = 0
        GPIO.output(rfidPins[tag],GPIO.LOW)
            #just got home rn    
    else:
        TimeIn[tag] = time.time()
        TimeAway[tag] = TimeIn[tag]-TimeOut[tag]
        TimeAwayTotal[tag] = TimeAwayTotal[tag] + TimeAway[tag]
        home[tag] = 1
        GPIO.output(rfidPins[tag],GPIO.HIGH)
    sendPHP(rfidtags, rfidName,home,tag)
    printPerson(home,TimeHome,TimeAway,rfidNick)
    return;
        
def printPerson(home,TimeHome,TimeAway,rfidNick):
    lcd.clear()
    for i in range (0,4):
        if home[i]:
            status='H'
            time=str(round(TimeHome[i]/3600.,1))
        else:
            status='A'
            time=str(round(TimeAway[i]/3600.,1))
        lcd.write_string(rfidNick[i] +' '+ status + time + ' ')
    return;

def sendPHP(rfidtags, rfidName,home,tag):
    if home[tag]:
        status='home'
    else:
        status='away'
    payload = {'name': rfidName[tag],'rfidID': rfidtags[tag], 'status': status}
    r = requests.post(url,data=payload)
    return;

if __name__=='__main__':
    main()
    
    





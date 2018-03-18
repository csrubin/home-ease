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

lcd.clear()
lcd.write_string('kevin suck my   cock')
    
'''
    for i in range (0,4):
        if home[i]:
            status='H'
            time=str(round(TimeHome[i]/3600.,1))
        else:
            status='A'
            time=str(round(TimeAway[i]/3600.,1))
        lcd.write_string(rfidNick[i] +' '+ status + time + ' ')
'''


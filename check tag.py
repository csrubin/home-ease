import serial
import time, datetime
##from gpiozero import LED
##import RPi.GPIO as IO
import requests
from RPLCD import *
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[40,38,36,32,33,31,29,15])
tag = ''

url = 'http://makeohio2018.kevinbartchlett.com/collectData.php'
rfid = serial.Serial('/dev/ttyUSB0', 9600)
ledB = GPIO.setup(21,GPIO.OUT)
ledY = GPIO.setup(16,GPIO.OUT)
ledG = GPIO.setup(18,GPIO.OUT)
ledR = GPIO.setup(12,GPIO.OUT)
#Initially no one is home
initTime = time.time()

while True:
    data = rfid.read()
    tag = tag + data.decode('utf-8')
    print(tag)

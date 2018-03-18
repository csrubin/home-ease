##from RPLCD import ChartLCD
from RPLCD import *
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

##lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[40,38,36,32,33,31,29,23])
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[40,38,36,32,33,31,29,15],numbering_mode=GPIO.BOARD)
##lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33,31,29,15])
##lcd = CharLCD(cols=16, rows=2, pin_rs=26, pin_e=19, pins_data=[21,20,16,12,13,6,5,22])


lcd.write_string('Hello World!')
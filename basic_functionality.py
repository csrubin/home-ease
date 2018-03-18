from gpiozero import LED
import serial
import time

rfid = serial.Serial('/dev/ttyUSB0', 9600)
#ledY = LED(19)
ledB = LED(21)
tag = ''

blue = '5500E1BFEAE1'
#yellow = '\x025500E0FCE1A8\r\n\x03'

#ledY.off()
ledB.off()
#Forever on
while True:
    print('Havent read')

    data = rfid.read()
    tag = tag + data.decode('utf-8')
    card = tag[1:13]
    print('After read')
    print('tag  ' + tag)
    #print('data  ' + data)
    print('card  ' + card)
    break
    while True:
        if (card == blue):
            ledB.toggle()
            card = ''
            data = ''
            tag = ''
            time.sleep(1.)
            break
        
        time.sleep(.1)

    
    
    
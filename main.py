#add the extra code we need to the pico
import machine
import time
import utime
from machine import I2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd

#we set the pins of the Pico that we need
relay = machine.Pin(17, machine.Pin.OUT)
switch = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)

#set the first values of the variables
last = time.ticks_ms()
count = 0

#needed for the LCD screen
I2C_ADDR     = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

#main code
while True:
    logic_state = switch.value()
    #check if the switch is on or off
    if logic_state == False:
        #check that it has been over 2 seconds since the last time the siwtch was clicked
        if time.ticks_diff(time.ticks_ms(), last) > 2100:
            #turn the relay on
            relay.on()
            #wait 2 seconds
            time.sleep(2)
            #add one to the bowl count variable
            count = count + 1
            i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
            lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
            #print the result on the LCD screen
            lcd.putstr("DOG BOWL REFILL COUNT: " + str(count))
            last = time.ticks_ms()    
    #if the switch if off, turn off the relay
    elif logic_state == True:
        relay.off()

import machine
import time
import utime
from machine import I2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd

led = machine.Pin(17, machine.Pin.OUT)
btn = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)

last = time.ticks_ms()
count = 0

I2C_ADDR     = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

def button_handler(pin):
    global last, btn, count
      
    if pin is btn:
        if time.ticks_diff(time.ticks_ms(), last) > 1100:
            led.on()
            time.sleep(1)
            count = count + 1
            i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
            lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
            lcd.putstr("DOG BOWL REFILL COUNT: " + str(count))
            last = time.ticks_ms()
            led.off()
    
led.value(0)
btn.irq(trigger = machine.Pin.IRQ_RISING, handler = button_handler)

import utime
from PicoGo_Code.Motor import PicoGo
from machine import Pin

M = PicoGo()
DSR = Pin(2, Pin.IN, Pin.PULL_DOWN)
DSL = Pin(3, Pin.IN)

while True:
    DR_status = DSR.value()
    DL_status = DSL.value()

    print(DR_status, DL_status)

    utime.sleep_ms(10)
    # if((DL_status == 0) and (DR_status == 0)):
    #     print("both")
    #     #M.left(10)
    # elif((DL_status == 0) and (DR_status == 1)):
    #     print("right")
    #     M.right(10)
    # elif((DL_status == 1) and (DR_status == 0)):
    #     print("left")
    #     M.left(10)
    # else:
    #     print("forward")
    #     M.forward(20)
        
    # utime.sleep_ms(10)

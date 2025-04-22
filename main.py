from PicoGo_Code.goalie_defend_test import *
from PicoGo_Code.start_strike_test import *
import utime

utime.sleep(2)

M = PicoGo()

asyncio.run(start_strike())
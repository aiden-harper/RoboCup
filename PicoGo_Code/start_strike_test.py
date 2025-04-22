from PicoGo_Code.Motor import PicoGo
from PicoGo_Code.ST7789 import ST7789
import asyncio
import utime
import math
import random
from PicoGo_Code.boundary_test import *

STRIKE_BACKUP = 2.25
STRIKE_BALL_DISTANCE = 5 + STRIKE_BACKUP
STRIKE_ANGLE = 1.107

async def start_strike():
    speed = 25
    x_position_time = STRIKE_BACKUP / (DISTANCE_PER_SECOND_CONSTANT * speed)
    await asyncio.gather(
        move_robot(speed, x_position_time, "backward"),
        track_position(speed, x_position_time, "backward")
    )
    
    strike_range_z = STRIKE_BALL_DISTANCE / math.tan(STRIKE_ANGLE)
    print("range:", strike_range_z)
    strike_range_z -= strike_range_z * 0.1
    z_strike_pos = random.uniform(-strike_range_z, strike_range_z)
    time_to_move = abs(z_strike_pos) / (DISTANCE_PER_SECOND_CONSTANT * speed)
    
    print("z pos:", z_strike_pos)
    print("moving to", z_strike_pos)
    if z_strike_pos > 0:
        print("turning left")
        await asyncio.gather(
            move_robot(speed, 0.27, "left"),
            track_position(speed, 0.27, "left")
        )
    else:
        print("turning right")
        await asyncio.gather(
            move_robot(speed, 0.27, "right"),
            track_position(speed, 0.27, "right")
        )
        
    print("moving")
    await asyncio.gather(
        move_robot(speed, time_to_move, "forward"),
        track_position(speed, time_to_move, "forward")
    )
    
    if z_strike_pos > 0:
        strike_angle = math.pi/2 - math.atan(STRIKE_BALL_DISTANCE/z_strike_pos)
    else:
        strike_angle = math.pi/2 + math.atan(STRIKE_BALL_DISTANCE/z_strike_pos)
        
    print(strike_angle, math.degrees(strike_angle))
    time_to_turn = strike_angle / (RADIANS_PER_SECOND_CONSTANT * speed)
    
    if z_strike_pos > 0:
        await asyncio.gather(
            move_robot(speed, 0.27 + time_to_turn, "right"),
            track_position(speed, 0.27 + time_to_turn, "right")
        )
    else:
        await asyncio.gather(
            move_robot(speed, 0.27 + time_to_turn, "left"),
            track_position(speed, 0.27 + time_to_turn, "left")
        )
    
    utime.sleep(1)
    strike_speed = 100
    distance_from_ball = math.sqrt((z_strike_pos ** 2) + (5 ** 2))
    time_to_move = distance_from_ball / (DISTANCE_PER_SECOND_CONSTANT * strike_speed)
    time_to_move += time_to_move * 1
    print(time_to_move)
    await asyncio.gather(
        move_robot(strike_speed, time_to_move, "forward"),
        track_position(strike_speed, time_to_move, "forward")
    )
    
def test_start_strike():
    speed = 25
    z_strike_pos = random.uniform(-GOAL_STRIKE_RANGE_Z, GOAL_STRIKE_RANGE_Z)
    print("Z Strike Pos:", z_strike_pos)
    time_to_move = z_strike_pos / (DISTANCE_PER_SECOND_CONSTANT * speed)

    if z_strike_pos > 0:
        print("left strike")
        strike_angle = math.pi/2 - math.atan(5/z_strike_pos)
    else:
        print("right strike")
        strike_angle = math.pi/2 + math.atan(5/z_strike_pos)
        
    print("Strike Angle:", math.degrees(strike_angle))
    time_to_turn = strike_angle / (RADIANS_PER_SECOND_CONSTANT * speed)
    
#asyncio.run(start_strike())



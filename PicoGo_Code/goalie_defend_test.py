from PicoGo_Code.Motor import PicoGo
from PicoGo_Code.boundary_test import *
import utime

GOALIE_MOVE_FORWARD = 1.375
GOALIE_Z_RANGE = 5.75

async def goalie_defend():
    start_speed = 25
    time_to_defend_X = GOALIE_MOVE_FORWARD / (DISTANCE_PER_SECOND_CONSTANT * start_speed)
    await asyncio.gather(
        move_robot(start_speed, time_to_defend_X, "forward"),
        track_position(start_speed, time_to_defend_X, "forward"),
        check_bounds(time_to_defend_X)
    )

    await asyncio.gather(
        move_robot(start_speed, 0.27, "right"),
        track_position(start_speed, 0.27, "right")
    )

    time_to_bottom_z_range = (GOALIE_Z_RANGE / 2) / (DISTANCE_PER_SECOND_CONSTANT * start_speed)
    await asyncio.gather(
        move_robot(start_speed, time_to_bottom_z_range, "forward"),
        track_position(start_speed, time_to_bottom_z_range, "forward"),
        check_bounds(time_to_bottom_z_range)
    )

    while True:
        defend_speed = 75
        time_full_range = (GOALIE_Z_RANGE) / (DISTANCE_PER_SECOND_CONSTANT * defend_speed)
        await asyncio.gather(
            move_robot(75, time_full_range, "backward"),
            track_position(75, time_full_range, "backward"),
            check_bounds(time_full_range)
        )

        #utime.sleep_ms(1000)
        time_full_range = (GOALIE_Z_RANGE) / (DISTANCE_PER_SECOND_CONSTANT * defend_speed)
        await asyncio.gather(
            move_robot(75, time_full_range, "forward"),
            track_position(75, time_full_range, "forward"),
            check_bounds(time_full_range)
        )
        
        #utime.sleep_ms(1000)

#asyncio.run(goalie_defend())


from PicoGo_Code.Motor import PicoGo
from PicoGo_Code.ST7789 import ST7789
import asyncio
import math

# constants
STRIKER_START_POS = (20, 12)
BOUNDARY_TOLERANCE = 1
ZMAX = 25
ZMIN = 0
XMAX = 24
XMIN = 15
GOAL_STRIKE_RANGE_Z = 2.5
UPDATE_INTERVAL = 0.01
RADIANS_PER_SECOND_CONSTANT = 0.230
DISTANCE_PER_SECOND_CONSTANT = 0.42
true_speed = lambda speed: DISTANCE_PER_SECOND_CONSTANT * speed

# globals
x, z = STRIKER_START_POS
in_bounds = True
head_radian = 3*math.pi/2

# motor and lcd
m = PicoGo()
lcd = ST7789()

def rotate_in_place(direction, speed, duration):
    global head_radian
    if direction == "left":
        m.left(speed)
        head_radian = (head_radian + (speed * duration * RADIANS_PER_SECOND_CONSTANT)) % (2*math.pi)
    elif direction == "right":
        m.right(speed)
        head_radian= (head_radian - (speed * duration * RADIANS_PER_SECOND_CONSTANT)) % (2*math.pi)

async def move_robot(speed, duration, direction):
    if direction in ["forward", "backward"]:
        if direction == "forward":
            m.forward(speed)
        else:
            m.backward(speed)
        await asyncio.sleep(duration)
        m.stop()

    elif direction in ["left", "right"]:
        rotate_in_place(direction, speed, duration)
        await asyncio.sleep(duration)
        m.stop()
    else:
        print("Unknown direction")

async def track_position(speed, duration, direction, verbose=False):
    global x, z
    
    if direction not in ["forward", "backward"]:
        return

    steps = int(duration / UPDATE_INTERVAL)
    for _ in range(steps):
        if not in_bounds:
            print("Tracking stopped: Out of bounds")
            return

        await asyncio.sleep(UPDATE_INTERVAL)

        if not in_bounds:
            print("Tracking stopped (post-sleep): Out of bounds")
            return
        
        distance_step = true_speed(speed) * UPDATE_INTERVAL
        multiplier = -1 if direction == "backward" else 1
        z += multiplier * distance_step * math.cos(head_radian)
        x += multiplier * distance_step * math.sin(head_radian)
        if verbose:
            print(f"Position: x = {x:.2f} in, z = {z:.2f} in, heading = {math.degrees(head_radian):.2f}°")
            lcd.fill(0xFFFF)
            lcd.show()
            lcd.text("Position",10,5,0xFF00)
            lcd.text(f"x = {x:.2f} in, z = {z:.2f} in",10,15)
            lcd.text(f"Heading = {math.degrees(head_radian):.2f}",10,25,0x07E0)
            lcd.show()

async def check_bounds(duration):
    global x, z, in_bounds
    steps = int(duration / (UPDATE_INTERVAL / 2))
    for _ in range(steps):
        if not (XMIN+BOUNDARY_TOLERANCE <= x <= XMAX-BOUNDARY_TOLERANCE\
                and ZMIN+BOUNDARY_TOLERANCE <= z <= ZMAX-BOUNDARY_TOLERANCE):
            m.stop()
            in_bounds = False
            return
        await asyncio.sleep(UPDATE_INTERVAL/2)

async def main():
    global in_bounds
    await asyncio.gather(
        move_robot(25, 1, "forward"),
        track_position(25, 1, "forward"),
        check_bounds(1)
    )
    
    print("go left")
    await asyncio.gather(
        move_robot(25, 0.27, "left"),
        track_position(25, 0.27, "left")
    )
    
    print("go forward")
    await asyncio.gather(
        move_robot(25, 1, "forward"),
        track_position(25, 1, "forward"),
        check_bounds(1)
    )

    lcd.fill(0xFFFF)
    lcd.show()
    lcd.text("Position",10,5,0xFF00)
    lcd.text(f"x = {x:.2f} in, z = {z:.2f} in",10,15)
    lcd.text(f"Heading = {math.degrees(head_radian):.2f}",10,25,0x07E0)
    lcd.show()
    
    print("\n--- Final Position ---")
    print(f"x = {x:.2f} in, z = {z:.2f} in")
    print(f"Heading = {math.degrees(head_radian):.2f}")
    
#test_start_strike()
# Run the main logic
asyncio.run(main())


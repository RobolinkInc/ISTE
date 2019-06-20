from zumi.zumi import Zumi
import time
from zumi.util.screen import Screen
from personality import Personality, Sound

eye = Screen()
# set up camera
zumi =Zumi()
personality = Personality(zumi, eye)
duration = 1

while True:
    landmark = input('land:')

    if landmark == 'china':
        zumi.turn_right(90)
    elif landmark == 'bigben':
        zumi.turn_right(45)
    elif landmark == 'seattle':
        zumi.turn_left(45)
    elif landmark == 'nyc':
        zumi.turn_left(90)

    time.sleep(1)
    zumi.forward(10, duration)
    time.sleep(1)
    personality.celebrate()
    time.sleep(1)
    zumi.reverse(10, duration)
    time.sleep(1)

    if landmark == 'china':
        zumi.turn_left(90)
    elif landmark== 'bigben':
        zumi.turn_left(45)
    elif landmark == 'seattle':
        zumi.turn_right(45)
    elif landmark == 'nyc':
        zumi.turn_right(90)
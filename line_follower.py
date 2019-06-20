from zumi.zumi import Zumi
from zumi.util.screen import Screen
import time

zumi = Zumi()
speed = 30
threashold = 70
prev_state = -1
HEAD = zumi.read_z_angle()

while True:
    ir_readings = zumi.get_all_IR_data()
    left = ir_readings[1]
    right = ir_readings[3]

    print(left, right)
    
    if left > threashold and right> threashold :
        print('1')
        zumi.control_motors(speed,speed)
        prev_state = 0
    elif left < threashold and right > threashold: 
        print('2')
        zumi.control_motors(-int(speed/2),int(speed/2))
        prev_state = 1
    elif left > threashold and right < threashold: 
        print('3') 
        zumi.control_motors(int(speed/2), -int(speed/2))
        prev_state = 2
    else:
        if prev_state ==1 :
            print('11')
            zumi.control_motors(int(speed/2),-int(speed/2))
        else:
            print('22')
            zumi.control_motors(-int(speed/2), int(speed/2))
        prev_state = 3

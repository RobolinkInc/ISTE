
from zumi.zumi import Zumi
import time


class Drive:
    def __init__(self, _zumi=None):
        if _zumi is None:
            self.z=Zumi()
        else:
            self.z = _zumi
        self.z.mpu.calibrate_MPU()

        self.NORTH = 0
        self.WEST = 90
        self.EAST = -90
        self.SOUTH = 180

        self.heading = self.NORTH

        self.current_x = 0
        self.current_y = 0

        self.motor_speed = 10
        self.ir_threshold = 125

    # ----------------FUNCTIONS-----------------

    def turn(self, angle=91, speed=30, step=4, direction=-1, delay=0.01):
            direction = self.z.clamp(direction,-1,1)
            init_ang_z = self.z.read_z_angle()
            for i in range (0, angle, step):
                self.z.go_straight(speed, init_ang_z+direction*i)
                time.sleep(delay)

    def cross_intersection(self):

        start = time.time()
        end = 0
        while end < 0.4:
            end = time.time()-start
            self.z.go_straight(10, self.heading)

    def move_to_coordinate(self, desired_x,desired_y):

        dx = desired_x - self.current_x  # Find out the difference in x
        dy = desired_y - self.current_y  # Find out the difference in y

        if dx%10 == 0 and dx != 5:

            if dx > 0:  # If x is positive (going East)
                if not self.current_x == 0:
                    self.cross_intersection()
                self.heading = self.EAST
                self.drive_block(dx)

            elif dx < 0:  # If x is negative (going West)
                self.cross_intersection()
                self.heading = self.WEST
                self.drive_block(abs(dx))

                self.current_x = desired_x

            if dy > 0:  # If y is also positive (going North)
                self.cross_intersection()
                self.heading = self.NORTH
                self.drive_block(dy)

            elif dy < 0:  # If y is negative (going South)
                self.cross_intersection()
                self.heading = self.SOUTH
                self.drive_block(abs(dy))

            self.current_y = desired_y

        else:
            if dy > 0:  # If y is also positive (going North)
                self.cross_intersection()
                self.heading = self.NORTH
                self.drive_block(dy)

            elif dy < 0:  # If y is negative (going South)
                self.cross_intersection()
                self.heading = self.SOUTH
                self.drive_block(abs(dy))

            self.current_y = desired_y

            if dx >0: # If x is positive (going East)
                self.cross_intersection()
                self.heading = self.EAST
                self.drive_block(dx)

            elif dx<0: # If x is negative (going West)
                if self.self.current_x != 0:
                    self.cross_intersection()
                self.heading = self.WEST
                self.drive_block(abs(dx))

            self.current_x = desired_x

    def park_left(self):
        self.turn(direction=1)
        self.z.forward(duration=0.5)

    def park_right(self):
        self.turn()
        self.z.forward(duration=0.5)

    def drive_block(self, x):

        left_on_white = False
        right_on_white  = False
        right_switch = 0
        left_switch = 0

        while True:

            ir_readings = self.z.get_all_IR_data()
            bottom_right_ir = ir_readings[1]
            bottom_left_ir = ir_readings[3]
            front_left_ir = ir_readings[0]
            front_right_ir = ir_readings[5]

            if bottom_left_ir < self.ir_threshold:
                if not left_on_white:
                    left_switch += 1
                left_on_white = True
            else:
                left_on_white = False

            if bottom_right_ir < self.ir_threshold:
                if not right_on_white:
                    right_switch += 1
                right_on_white = True
            else:
                right_on_white = False

            if right_on_white and not left_on_white:
                self.heading -= 1

            if left_on_white and not right_on_white:
                self.heading += 1

            if right_switch == x or left_switch == x:
                break

            if front_left_ir < 70 or front_right_ir < 70:
                self.z.stop(0)
                continue

            #clear_output(wait=True)
            self.z.go_straight(self.motor_speed, self.heading)

    def run_demo(self, location):
        try:

            if location == "a":
                self.move_to_coordinate(10,5)
                self.park_left()

            if location == "b":
                self.move_to_coordinate(15,10)
                self.park_right()

            if location == "c":
                self.move_to_coordinate(25,0)
                self.park_left()

            if location == "d":
                self.move_to_coordinate(5,10)
                self.park_left()

            if location == "e":
                self.move_to_coordinate(15,20)
                self.park_right()

            if location == "f":
                self.move_to_coordinate(20,16)
                self.park_right()

            if location == "g":
                self.move_to_coordinate(0,26)
                self.park_right()

            if location == "h":
                self.move_to_coordinate(10,25)
                self.park_right()

            if location == "i":
                self.move_to_coordinate(26,30)
                self.park_right()

        finally:
            self.z.stop()






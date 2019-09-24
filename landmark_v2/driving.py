from zumi.zumi import Zumi
import math


def centimeter_to_inch(x):
    return x / 2.54


class Drive:
    def __init__(self, _zumi=None):
        if _zumi is None:
            self.zumi = Zumi()
        else:
            self.zumi = _zumi

        self.current_x = 0
        self.current_y = 0

        self.zumi.reset_gyro()

    def move_inches(self, distance, angle):
        y_intercept = 1
        slope = 6
        duration = (distance + y_intercept) / slope

        # make sure if there is no distance only turn
        if (distance < 0.2):
            self.zumi.turn(angle)
        # if there is a distance go at speed 40 at that angle
        else:
            self.zumi.forward(40, duration, angle)

    def move_to_coordinate(self, desired_x, desired_y):
        dx = desired_x - self.current_x
        dy = desired_y - self.current_y

        # find the angle
        angle = math.degrees(math.atan2(dy, dx))

        # find the distance to the coordinate
        distance = math.hypot(dx, dy)

        # update the coordinates
        self.current_x = desired_x
        self.current_y = desired_y

        print(" ang = ", angle, " dist = ", distance)

        self.zumi.turn(angle)
        self.move_inches(distance, angle)

    # this is for uber challenge/robo world demo map location hard coding
    def move_to_a(self):
        self.move_to_coordinate(centimeter_to_inch(50) - 4, 0)
        self.move_to_coordinate(centimeter_to_inch(50) - 4, centimeter_to_inch(25) - 3)
        self.move_to_coordinate(centimeter_to_inch(40) - 4, centimeter_to_inch(25) - 3)

    def return_from_a(self):
        self.move_to_coordinate(centimeter_to_inch(50) - 4, centimeter_to_inch(25) - 3)
        self.move_to_coordinate(centimeter_to_inch(50) - 4, 0)
        self.move_to_coordinate(0, 0)
    def move_to_b(self):
        self.move_to_coordinate(0, centimeter_to_inch(50) - 4)
        self.move_to_coordinate(centimeter_to_inch(75)-4, centimeter_to_inch(50) - 4)
        self.move_to_coordinate(centimeter_to_inch(75)-4, centimeter_to_inch(40) - 4)

    def return_from_b(self):
        self.move_to_coordinate(centimeter_to_inch(90) - 4, centimeter_to_inch(50) - 4)
        self.move_to_coordinate(0, centimeter_to_inch(50) - 4)
        self.move_to_coordinate(0, 0)

    def move_to_c(self):
        self.move_to_coordinate(centimeter_to_inch(105) - 4, 0)
        self.move_to_coordinate(centimeter_to_inch(105) - 4, 4)

    def return_from_c(self):
        self.move_to_coordinate(centimeter_to_inch(105) - 4, 0)
        self.move_to_coordinate(0, 0)

    def move_to_d(self):
        self.move_to_coordinate(0, centimeter_to_inch(50) - 4)
        self.move_to_coordinate(centimeter_to_inch(25) - 3, centimeter_to_inch(50) - 4)
        self.move_to_coordinate(centimeter_to_inch(25) - 3, centimeter_to_inch(50))

    def return_from_d(self):
        self.move_to_coordinate(centimeter_to_inch(25) - 3, centimeter_to_inch(50) - 4)
        self.move_to_coordinate(0, centimeter_to_inch(50) - 4)
        self.move_to_coordinate(0, 0)

    def move_to_e(self):
        self.move_to_coordinate(20, 0)
        self.move_to_coordinate(20, 15)
        self.move_to_coordinate(18, 15)

    def return_from_e(self):
        self.move_to_coordinate(20, 0)
        self.move_to_coordinate(20, 15)
        self.move_to_coordinate(18, 15)
        self.move_to_coordinate(0, 0)

    def move_to_f(self):
        self.move_to_coordinate(0, centimeter_to_inch(50) - 4)
        self.move_to_coordinate(centimeter_to_inch(100) - 4, centimeter_to_inch(50) - 4)
        self.move_to_coordinate(centimeter_to_inch(100) - 4, centimeter_to_inch(90) - 4)
        self.move_to_coordinate(centimeter_to_inch(120) - 4, centimeter_to_inch(90) - 4)

    def return_from_f(self):
        self.move_to_coordinate(0, centimeter_to_inch(50) - 4)
        self.move_to_coordinate(centimeter_to_inch(100) - 4, centimeter_to_inch(50) - 4)
        self.move_to_coordinate(centimeter_to_inch(100) - 4, centimeter_to_inch(90) - 4)
        self.move_to_coordinate(centimeter_to_inch(120) - 4, centimeter_to_inch(90) - 4)
        self.move_to_coordinate(0, 0)

    def move_to_g(self):
        self.move_to_coordinate(0, 28)
        self.move_to_coordinate(3, 28)

    def return_from_g(self):
        self.move_to_coordinate(0, 28)
        self.move_to_coordinate(3, 28)
        self.move_to_coordinate(0, 0)

    def move_to_h(self):
        self.move_to_coordinate(0, 20)
        self.move_to_coordinate(10, 20)
        self.move_to_coordinate(10, 25)
        self.move_to_coordinate(13, 25)

    def return_from_h(self):
        self.move_to_coordinate(0, 20)
        self.move_to_coordinate(10, 20)
        self.move_to_coordinate(10, 25)
        self.move_to_coordinate(13, 25)
        self.move_to_coordinate(0, 0)

    def move_to_i(self):
        self.move_to_coordinate(0, 30)
        self.move_to_coordinate(28, 30)
        self.move_to_coordinate(28, 28)

    def return_from_i(self):
        self.move_to_coordinate(0, 30)
        self.move_to_coordinate(28, 30)
        self.move_to_coordinate(28, 28)
        self.move_to_coordinate(0, 0)

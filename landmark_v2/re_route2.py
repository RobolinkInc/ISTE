import networkx as nx
import time
from zumi.zumi import Zumi


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "[{},{}]".format(self.x, self.y)

    def __repr__(self):
        return "[{},{}]".format(self.x, self.y)


class Route_new:
    def __init__(self, zumi = None):
        self.start_node = Point(0, 0)
        self.bigben = Point(5, 20)
        self.seattle = Point(25, 0)
        self.paris = Point(15, 10)
        self.NY = Point(10, 15)
        self.china = Point(25, 20)

        self.node1 = Point(10, 0)
        self.node2 = Point(20, 0)
        self.node3 = Point(30, 0)
        self.node4 = Point(0, 10)
        self.node5 = Point(10, 10)
        self.node6 = Point(20, 10)
        self.node7 = Point(30, 10)
        self.node8 = Point(0, 20)
        self.node9 = Point(10, 20)
        self.node10 = Point(20, 20)
        self.node11 = Point(30, 20)
        self.node12 = Point(0, 30)
        self.node13 = Point(10, 30)
        self.node14 = Point(30, 30)

        self.G = nx.Graph()
        self.generate_map()

        self.NORTH = 0
        self.WEST = 90
        self.EAST = -90
        self.SOUTH = 180

        self.heading = self.NORTH
        if zumi is None:
            # pass
            self.zumi = Zumi()

        self.motor_speed = 10
        self.ir_threshold = 70
        self.reverse = False

    def generate_map(self):
        # Directed Graph

        # G 그래프 만들기 (node 간의 edge가 존재하면 add_node 하고 add_edge 안해도 됨
        self.G.add_edge(self.start_node, self.node1, distance=10)
        self.G.add_edge(self.start_node, self.node4, distance=10)
        self.G.add_edge(self.node1, self.node2, distance=10)
        self.G.add_edge(self.node1, self.node5, distance=10)
        self.G.add_edge(self.node2, self.seattle, distance=5)
        self.G.add_edge(self.node2, self.node6, distance=10)
        self.G.add_edge(self.seattle, self.node3, distance=5)
        self.G.add_edge(self.node3, self.node7, distance=10)

        self.G.add_edge(self.node4, self.node5, distance=10)
        self.G.add_edge(self.node4, self.node8, distance=10)
        self.G.add_edge(self.node5, self.NY, distance=5)
        self.G.add_edge(self.node5, self.paris, distance=5)
        self.G.add_edge(self.NY, self.node9, distance=5)
        self.G.add_edge(self.paris, self.node6, distance=5)
        self.G.add_edge(self.node6, self.node7, distance=10)
        self.G.add_edge(self.node6, self.node10, distance=10)
        self.G.add_edge(self.node7, self.node11, distance=10)

        self.G.add_edge(self.node8, self.bigben, distance=5)
        self.G.add_edge(self.node8, self.node12, distance=10)
        self.G.add_edge(self.bigben, self.node9, distance=5)
        self.G.add_edge(self.node9, self.node10, distance=10)
        self.G.add_edge(self.node9, self.node13, distance=10)
        self.G.add_edge(self.node10, self.china, distance=5)
        self.G.add_edge(self.china, self.node11, distance=5)
        self.G.add_edge(self.node11, self.node14, distance=10)

        self.G.add_edge(self.node12, self.node13, distance=10)
        self.G.add_edge(self.node13, self.node14, distance=20)

    def find_path(self, start, destination):

        start_point = start
        destination = destination

        # 연결 안 된 노드가 있을 경우를 방지
        if nx.has_path(self.G, start_point, destination):
            path = nx.shortest_path(self.G, source=start_point, target=destination, weight='distance')
        else:
            print("No path!!")
            return
        if path is not None:
            print(path)

        return path

    def driving(self, start, destination):
        shortest_path = self.find_path(start, destination)[1:]
        current_node = start
        while len(shortest_path):
            print(shortest_path)
            next_node = shortest_path.pop(0)
            # found_obstacle = False
            found_obstacle = self.drive_to_nextnode(current_node,next_node)
            if found_obstacle:
                print("find obstacle : {}".format(found_obstacle))
                self.go_back_to_node(found_obstacle)
                self.disconnect_route(current_node, next_node)
                self.driving(current_node, destination)
                return
            current_node = next_node
        self.zumi.stop()
        return

    def driving_without_reroute(self, start, destination):
        shortest_path = self.find_path(start, destination)[1:]
        current_node = start
        while len(shortest_path):
            print(shortest_path)
            next_node = shortest_path.pop(0)
            x = self.drive_to_nextnode(current_node,next_node)
            current_node = next_node
        self.zumi.stop()
        return

    def drive_to_nextnode(self, current, next):
        dx = next.x - current.x
        dy = next.y - current.y
        print("[{},{}]".format(dx, dy))
        self.decide_turn_or_pass_intersection(dx, dy, current)
        # if max(abs(dx),abs(dy))%10:
        #     result = self.drive_n_block(abs(dx + dy)+1)
        # else:
        result = self.drive_n_block(abs(dx+dy))
        return result

    def decide_turn_or_pass_intersection(self, dx, dy, current):
        print("check turn or not")
        temp = current.x + current.y
        if self.reverse:
            self.reverse = False
        elif temp and temp % 10 == 0:
            self.cross_intersection()

        if dx > 0:
            new_heading = self.EAST
        elif dx < 0:
            new_heading = self.WEST
        elif dy > 0:
            new_heading = self.NORTH
        else:
            new_heading = self.SOUTH

        if not new_heading - 20 < self.heading < new_heading + 20:
            print("change heading")
            self.heading = new_heading

    def drive_n_block(self, n):
        print("drive n block")
        ir_readings = self.zumi.get_all_IR_data()
        left_on_white = False if ir_readings[3] > self.ir_threshold else True
        right_on_white = False if ir_readings[1] > self.ir_threshold else True
        right_switch = 0
        left_switch = 0
        while left_on_white or right_on_white:
            ir_readings = self.zumi.get_all_IR_data()
            if ir_readings[3] < self.ir_threshold:
                if not left_on_white:
                    left_on_white = True
            else:
                left_on_white = False

            if ir_readings[1] < self.ir_threshold:
                if not right_on_white:
                    right_on_white = True
            else:
                right_on_white = False

            self.adjust_driving(left_on_white, right_on_white)
            if ir_readings[0] < 70 or ir_readings[5] < 70:
                return max(right_switch, left_switch)
            self.zumi.go_straight(self.motor_speed, self.heading)

        while right_switch != n and left_switch != n:
            print("{},{}".format(left_switch, right_switch))
            ir_readings = self.zumi.get_all_IR_data()

            if ir_readings[3] < self.ir_threshold:
                if not left_on_white:
                    left_switch += 1
                    left_on_white = True
            else:
                left_on_white = False

            if ir_readings[1] < self.ir_threshold:
                if not right_on_white:
                    right_switch += 1
                    right_on_white = True
            else:
                right_on_white = False

            self.adjust_driving(left_on_white, right_on_white)

            # detect obstacle
            if ir_readings[0] < 70 or ir_readings[5] < 70:
                return max(right_switch, left_switch)

            self.zumi.go_straight(self.motor_speed, self.heading)
        return False

    def adjust_driving(self, left_on_white, right_on_white, reverse=1):
        if right_on_white and not left_on_white:
            correction = -1
        elif left_on_white and not right_on_white:
            correction = 1
        else:
            return
        self.heading += correction*reverse

    def cross_intersection(self):
        print("cross road")
        start = time.time()
        end = 0
        while end < 0.45:
            end = time.time()-start
            self.zumi.go_straight(10, self.heading)

    def go_back_to_node(self, n):
        self.reverse = True
        left_on_white = False
        right_on_white = False
        right_switch = 0
        left_switch = 0

        while right_switch != n and left_switch != n:
            print( "{},{}".format(left_switch, right_switch))
            ir_readings = self.zumi.get_all_IR_data()

            if ir_readings[3] < self.ir_threshold:
                if not left_on_white:
                    left_switch += 1
                    left_on_white = True
            else:
                left_on_white = False

            if ir_readings[1] < self.ir_threshold:
                if not right_on_white:
                    right_switch += 1
                    right_on_white = True
            else:
                right_on_white = False

            self.adjust_driving(left_on_white, right_on_white, reverse=-1)
            self.zumi.go_reverse(self.motor_speed, self.heading)
        # while right_on_white or left_on_white:
        #     ir_readings = self.zumi.get_all_IR_data()
        #
        #     if ir_readings[3] < self.ir_threshold:
        #         if not left_on_white:
        #             left_switch += 1
        #             left_on_white = True
        #     else:
        #         left_on_white = False
        #
        #     if ir_readings[1] < self.ir_threshold:
        #         if not right_on_white:
        #             right_switch += 1
        #             right_on_white = True
        #     else:
        #         right_on_white = False
        #
        #     self.adjust_driving(left_on_white, right_on_white, reverse=-1)
        #
        #     # detect obstacle
        #     if ir_readings[0] < 70 or ir_readings[5] < 70:
        #         return max(right_switch, left_switch)
        #
        #     self.zumi.go_reverse(self.motor_speed, self.heading)
        time.sleep(0.4)

        print("done")

    def disconnect_route(self, current_node, next_node):
        # self.G.add_edge(current_node, next_node, distance=1000)
        self.G.remove_edge(current_node, next_node)

    def reset_map(self):
        self.G = nx.Graph()
        self.generate_map()

    def turn(self, angle=91, speed=30, step=4, direction=-1, delay=0.01):
            direction = self.zumi.clamp(direction,-1,1)
            init_ang_z = self.zumi.read_z_angle()
            for i in range(0, angle, step):
                self.zumi.go_straight(speed, init_ang_z+direction*i)
                time.sleep(delay)

    def park_left(self):
        self.turn(direction=1)
        self.zumi.forward(duration=0.5)

    def park_right(self):
        self.turn()
        self.zumi.forward(duration=0.5)


if __name__ == '__main__':
    route = Route()
    try:
        # route.find_path(route.start_node, route.paris)
        # route.find_path(route.start_node, route.seattle)
        # route.disconnect_route(route.start_node, route.node1)
        # route.find_path(route.start_node, route.seattle)
        # route.find_path(route.start_node, route.bigben)
        # route.find_path(route.start_node, route.NY)
        # route.find_path(route.start_node, route.china)
        # route.find_path(route.start_node, route.china)
        # route.disconnect_route(route.start_node, route.node5)
        # route.find_path(route.start_node, route.china)
        # route.disconnect_route(route.start_node, route.node1)
        # route.find_path(route.start_node, route.china)
        # route.reset_map()
        # route.find_path(route.start_node, route.china)
        # route.drive_n_block(10)
        # route.go_back_to_node(10)
        # route.disconnect_route(route.start_node, route.node4)
        route.driving(route.start_node, route.NY)
        route.park_right()
        # route.disconnect_route(route.node1, route.node7)
        # route.driving(route.start_node, route.seattle)
        # route.driving(route.start_node, route.paris)
        # route.driving(route.start_node, route.china)
        # route.driving(route.start_node, route.bigben)
        # route.go_back_to_node(10)
        # route.zumi.go_straight(route.motor_speed, 0)
        # time.sleep(10)
        # route.zumi.turn_left(90, 1.5)
        # time.sleep(1)
        # route.zumi.go_straight(route.motor_speed, 0)
        # time.sleep(10)
        # route.zumi.turn_left(90, 1.5)
        # time.sleep(1)

    finally:
        route.zumi.stop()


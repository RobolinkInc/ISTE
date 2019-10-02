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

    # def __eq__(self, other):
    #
    #     if not isinstance(other, Point):
    #         return False
    #     if self.x==other.x and self.y == other.y:
    #         return True
    #     return False
    #
    # def __ne__(self, other):
    #     return not self.__eq__(other)


class Route:
    def __init__(self, zumi = None):
        self.start_node = Point(0, 0)
        self.node1 = Point(10, 0)
        self.node2 = Point(20, 0)
        self.bigben = Point(25, 0)
        self.node4 = Point(30, 0)
        self.node5 = Point(0, 10)
        self.NY = Point(5, 10)
        self.node7 = Point(10, 5)
        self.node8 = Point(10, 10)
        self.seattle = Point(15, 10)
        self.node10 = Point(20, 10)
        self.node11 = Point(30, 10)
        self.node12 = Point(0, 20)
        self.node13 = Point(20, 10)
        self.paris = Point(15, 20)
        self.node15 = Point(20, 15)
        self.node16 = Point(20, 20)
        self.node17 = Point(30, 20)
        self.node18 = Point(0, 27)
        self.node19 = Point(0, 30)
        self.node20 = Point(10, 25)
        self.node21 = Point(10, 30)
        self.node22 = Point(20, 30)
        self.china = Point(27, 30)
        self.node24 = Point(30, 30)
        self.G = nx.Graph()
        self.generate_map()

        self.NORTH = 0
        self.WEST = 90
        self.EAST = -90
        self.SOUTH = 180

        self.heading = self.NORTH
        if zumi is None:
            self.zumi = Zumi()
        self.motor_speed = 10
        self.ir_threshold = 125

    def generate_map(self):
        # Directed Graph

        # G 그래프 만들기 (node 간의 edge가 존재하면 add_node 하고 add_edge 안해도 됨
        self.G.add_edge(self.start_node, self.node1, distance=10)
        self.G.add_edge(self.start_node, self.node5, distance=10)
        self.G.add_edge(self.node1, self.node2, distance=10)
        self.G.add_edge(self.node1, self.node7, distance=5)
        self.G.add_edge(self.node2, self.bigben, distance=5)
        self.G.add_edge(self.node2, self.node10, distance=10)
        self.G.add_edge(self.bigben, self.node4, distance=5)
        self.G.add_edge(self.node4, self.node11, distance=10)
        self.G.add_edge(self.node5, self.NY, distance=5)
        self.G.add_edge(self.node5, self.node12, distance=10)
        self.G.add_edge(self.NY, self.node8, distance=5)
        self.G.add_edge(self.node8, self.NY, distance=5)
        self.G.add_edge(self.node7, self.node8, distance=5)
        self.G.add_edge(self.node8, self.seattle, distance=5)
        self.G.add_edge(self.node8, self.node13, distance=10)
        self.G.add_edge(self.seattle, self.node10, distance=5)
        self.G.add_edge(self.node10, self.node11, distance=10)
        self.G.add_edge(self.node10, self.node15, distance=7)
        self.G.add_edge(self.node11, self.node17, distance=10)
        self.G.add_edge(self.node12, self.node13, distance=10)
        self.G.add_edge(self.node12, self.node18, distance=7)
        self.G.add_edge(self.node13, self.paris, distance=5)
        self.G.add_edge(self.node13, self.node20, distance=5)
        self.G.add_edge(self.paris, self.node16, distance=5)
        self.G.add_edge(self.node15, self.node16, distance=3)
        self.G.add_edge(self.node16, self.node17, distance=10)
        self.G.add_edge(self.node16, self.node22, distance=10)
        self.G.add_edge(self.node17, self.node24, distance=10)
        self.G.add_edge(self.node18, self.node19, distance=3)
        self.G.add_edge(self.node19, self.node21, distance=10)
        self.G.add_edge(self.node20, self.node21, distance=5)
        self.G.add_edge(self.node21, self.node22, distance=10)
        self.G.add_edge(self.node22, self.china, distance=7)
        self.G.add_edge(self.china, self.node24, distance=3)

    def find_path(self, start, destination):

        start_point = start
        destination = destination

        # 연결 안 된 노드가 있을 경우를 방지
        if nx.has_path(self.G, start_point, destination):
            path = nx.shortest_path(self.G, source=start_point, target=destination, weight='distance')

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
                print("find obstacle")
                self.go_back_to_node(found_obstacle)
                self.disconnect_route(current_node, next_node)
                self.driving(current_node, destination)
                return
            current_node = next_node
        self.zumi.stop()
        return

    def drive_to_nextnode(self, current, next):
        dx = next.x - current.x
        dy = next.y - current.y
        print("[{},{}]".format(dx, dy))
        self.decide_turn_or_pass_intersection(dx, dy, current)
        result = self.drive_n_block(abs(dx+dy))
        return result

    def decide_turn_or_pass_intersection(self, dx, dy, current):
        print("check turn or not")
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
            return self.cross_intersection()
        elif not current.x+current.y:
            return
        else:
            return self.cross_intersection()

    def drive_n_block(self, n):
        print("drive n block")
        left_on_white = False
        right_on_white = False
        right_switch = 0
        left_switch = 0

        while right_switch != n and left_switch != n:

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
        while end < 0.4:
            end = time.time()-start
            self.zumi.go_straight(10, self.heading)

    def go_back_to_node(self, n):
        left_on_white = False
        right_on_white = False
        right_switch = 0
        left_switch = 0

        while right_switch == n or left_switch == n:

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

    def disconnect_route(self, current_node, next_node):
        self.G.add_edge(current_node, next_node, distance=1000)


route = Route()
route.driving(route.start_node, route.NY)
# route.disconnect_route(route.node2, route.node1)
# route.driving(route.node1, route.node15)
# route.find_path(route.start_node, route.node15)
# route.disconnect_route(route.node2, route.node1)
# route.find_path(route.node1, route.node15)
#route.drive_n_block(10)
#route.zumi.stop()


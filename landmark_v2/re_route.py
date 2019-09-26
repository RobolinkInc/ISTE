import networkx as nx


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
    def __init__(self):
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
            next_node = shortest_path.pop(0)
            found_obstacle = self.drive_to_nextnode()
            if found_obstacle:
                self.go_back_to_node()
                self.disconnect_route(current_node, next_node)
                self.driving(current_node, destination)
                return
        return

    def drive_to_nextnode(self):
        self.node1 = self.node1
        return False

    def go_back_to_node(self):
        pass

    def disconnect_route(self, current_node, next_node):
        self.G.add_edge(current_node, next_node, distance=1000)


route = Route()
route.find_path(route.start_node, route.node15)
route.disconnect_route(route.node1, route.node2)
route.find_path(route.node1, route.node15)




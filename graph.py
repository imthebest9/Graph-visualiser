import os
import random
import heapq
import sys
from os import system
from collections import defaultdict


class Graph:
    def __init__(self, start_input, is_directed=False):
        self.start_point = start_input  # A,B,C,D An array
        self.adj_list = {}
        self.weight = {}
        self.is_directed = is_directed
        self.isCycle = False
        self.queue = []

        for node in self.start_point:
            self.adj_list[node] = []  # Create array to store Destination for that node
            self.weight[node] = []  # Create array to store weight

    def add_edge(self, u, v, w):
        self.adj_list[u].append(v)
        self.weight[u].append(w)

        if not self.is_directed:
            self.adj_list[v].append(u)
            self.weight[u].append(w)

    def del_edge(self, u, v, w):
        self.adj_list[u].remove(v)
        self.weight[u].remove(w)

        if not self.is_directed:
            self.adj_list[v].remove(u)
            self.weight[v].remove(w)

    def degree(self, node):
        deg = len(self.adj_list[node])
        return deg

    def super_add(self, u, v, w):  # ONLY Add edge that doesnt exist
        num = 0
        for i in self.adj_list[u]:
            if i != v:
                num += 1

        if num == len(self.adj_list[u]):
            self.adj_list[u].append(v)
            self.weight[u].append(w)

    def super_del(self, u, v, w):  # ONLY Delete edge that exist
        for i in self.adj_list[u]:
            if i == v:
                self.adj_list[u].remove(v)
                self.weight[u].remove(w)

    def print_adj_list(self):
        for node in self.start_point:  # node= destination
            # print("List  : ", node, "->", self.adj_list[node])
            print(node, "-> [", end=" ")
            for x, y in zip(self.adj_list[node], self.weight[node]):
                if y != self.weight[node][-1]:
                    print("(", x, ",", y, "),", end=" ")
                else:
                    print("(", x, ",", y, ")", end=" ")
            print("]")

    def add_random_edge(self, rand_edges):
        a, b, c = random.choice(list(rand_edges))
        self.super_add(a, b, c)
        print("(", a, ",", b, ",", c, ") is randomly generated and added")

    # function 1: detecting strongly connected component
    def DFS(self, s):
        # Initially mark all vertices as not visited
        visited = defaultdict()
        for i in self.start_point:  # start_point = all nodes
            visited[i] = False

        # Create a stack for DFS
        stack = []

        # Push the current source node.
        stack.append(s)

        # print("Start from node: ", s)

        while len(stack):
            # Pop a vertex from stack and print it
            s = stack[-1]  # The top value of the stack
            stack.pop()

            # Stack may contain same vertex twice. So
            # we need to print the popped item only
            # if it is not visited.
            if not visited[s]:
                visited[s] = True

            # Get all adjacent vertices of the popped vertex s
            # If a adjacent has not been visited, then push it
            # to the stack.
            for node in self.adj_list[s]:
                if not visited[node]:
                    stack.append(node)

        for node in visited:
            if not visited[node]:
                return False
            return True

    def isSC(self):
        for x in self.start_point:
            if not self.DFS(x):
                return False

        return True

    def gen_SC(self, other_edge):
        while not self.isSC():
            self.add_random_edge(other_edge)

    # function 2: detecting cycle
    def detectAlgo(self, num, pred, n, v):
        n += 1
        num[v] = n
        self.queue.append(v)

        for u in self.adj_list[v]:
            if num[u] == 0:
                pred[u] = v
                self.detectAlgo(num, pred, n, u)

            elif num[u] != 999:
                pred[u] = v
                stack2 = []
                stack3 = []
                print("Cycle start point:", u)
                for i in self.queue:
                    stack2.append(i)

                while stack2:
                    if stack2[-1] != u:
                        stack3.append(stack2.pop())
                    elif stack2[-1] == u:
                        stack3.append(stack2.pop())
                        break

                while stack3:
                    print(stack3.pop(), "->", end="")
                print(u)

                self.isCycle = True

        num[v] = 999
        self.queue.pop()
        return self.isCycle

    def cycleDetection(self):
        num = defaultdict()
        for i in self.start_point:
            num[i] = 0

        pred = defaultdict()
        for i in self.start_point:
            pred[i] = ""

        n = 0

        self.detectAlgo(num, pred, n, 'RI')

        if self.isCycle:
            print("Cycle Detected")
        else:
            print("Cycle Not Detected")

        print(" ")
        return self.isCycle

    def gen_Cycle(self):
        while not self.cycleDetection():
            self.add_random_edge(other_edges)
        self.print_adj_list()

    # function 3: shortest path
    def shortest_path(self, source, destination):
        queue = [(0, source, [])]  # initialize a priority queue
        visited = set()  # create hash set to store visited node
        heapq.heapify(queue)  # create heap priority queue (this can pop the smallest value)
        # traverse graph with BFS
        while queue:
            (cost, node, path) = heapq.heappop(queue)
            # visit the node that has not been visited before
            if node not in visited:
                visited.add(node)
                path = path + [node]
                # if the node is the destination
                if node == destination:
                    return cost, path
                # visit neighbours
                for c, neighbour in zip(self.weight[node], self.adj_list[node]):
                    if neighbour not in visited:
                        heapq.heappush(queue, (cost + c, neighbour, path))
        # if the destination is not reachable, add random edge until it does
        self.add_random_edge(other_edges)
        return self.shortest_path(source, destination)


default_edges = {
    ("RI", "JK", 7349), ("RI", "HU", 12733), ("JK", "KH", 8527), ("HU", "SE", 11328), ("SE", "KH", 9340)
}

other_edges = {
    ("RI", "SE", 7549), ("RI", "KH", 1792),
    ("JK", "RI", 7349), ("JK", "HU", 16511), ("JK", "SE", 5294),
    ("HU", "RI", 12733), ("HU", "JK", 16511), ("HU", "KH", 12492),
    ("SE", "RI", 7549), ("SE", "JK", 5294), ("SE", "HU", 11328),
    ("KH", "RI", 1792), ("KH", "JK", 8527), ("KH", "HU", 12492), ("KH", "SE", 9340)
}

nodes = ["RI", "SE", "JK", "HU", "KH"]
graph = Graph(nodes, True)
for u, v, w in default_edges:
    graph.super_add(u, v, w)


# graph.gen_Cycle() function 2
# function 3
# print("The original graph is: ")
# graph.print_adj_list()
# print(graph.shortest_path("SE", "RI"))
# print("The final graph is: ")
# graph.print_adj_list()
# print(graph.isSC())

def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')


# menu
def menu():
    clear = lambda: system('clear')
    cont = True
    while cont:
        print("************Welcome to Graph Demo**************")
        print()

        choice = input("""
                          1: Add a new edge
                          2: Remove an edge
                          3: Strongly connectivity
                          4: Cycle detection
                          5: Shortest path
                          6: Reset graph
                          7: Exit

                          Please enter your choice: """)

        if choice == "3":
            graph.print_adj_list()
            if graph.isSC():
                print("Graph is strongly connected")
            else:
                print("Graph is not strongly connected")
                graph.gen_SC(other_edges)
                graph.print_adj_list()
                print("The graph is now strongly connected")
            print()
            cont = input("Do you want to continue (y/n): ")
            if cont == "n":
                break
            elif cont == "y":
                continue
            else:
                print("Only input y or n")
                cont = input("Do you want to continue (y/n): ")
        elif choice == "4":
            graph.print_adj_list()
            graph.gen_Cycle()
            print()
            cont = input("Do you want to continue (y/n): ")
            if cont == "n":
                break
            elif cont == "y":
                continue
            else:
                print("Only input y or n")
                cont = input("Do you want to continue (y/n): ")
        elif choice == "5":
            print("The original graph is: ")
            graph.print_adj_list()
            print("Shortest path")
            start = input("Start point: ")
            end = input("End point: ")
            print(graph.shortest_path(start, end))
            print("The final graph is: ")
            graph.print_adj_list()
            print()
            cont = input("Do you want to continue (y/n): ")
            if cont == "n":
                break
            elif cont == "y":
                continue
            else:
                print("Only input y or n")
                cont = input("Do you want to continue (y/n): ")
        elif choice == "7":
            sys.exit()
        elif choice == "1":
            addEdge = True
            while addEdge:
                print("The cities in the graph are RI, SE, JK, HU and KH")
                start = input("Starting node: ")
                end = input("Ending node: ")
                weight = 0
                for u, v, w in default_edges:
                    if u == start and v == end:
                        weight = w
                for u, v, w in other_edges:
                    if u == start and v == end:
                        weight = w
                graph.super_add(start, end, weight)
                print()
                print("The updated graph: ")
                print(graph.print_adj_list())
                addEdge = input("Do you want to add more edge (y/n): ")
                if addEdge == "n":
                    addEdge = False
                    break
                elif addEdge == "y":
                    continue
                else:
                    print("Only input y or n")
                    addEdge = input("Do you want to add more edge (y/n): ")
        elif choice == "2":
            removeEdge = True
            while removeEdge:
                print("The current graph is: ")
                print(graph.print_adj_list())
                start = input("Starting node: ")
                end = input("Ending node: ")
                weight = 0
                for u, v, w in default_edges:
                    if u == start and v == end:
                        weight = w
                for u, v, w in other_edges:
                    if u == start and v == end:
                        weight = w
                graph.del_edge(start, end, weight)
                print()
                print("The updated graph: ")
                print(graph.print_adj_list())
                removeEdge = input("Do you want to remove more edge (y/n): ")
                if removeEdge == "n":
                    removeEdge = False
                    break
                elif removeEdge == "y":
                    continue
                else:
                    print("Only input y or n")
                    removeEdge = input("Do you want to remove more edge (y/n): ")
        elif choice == "6":
            reset = True
            while reset:
                print("The current graph is: ")
                print(graph.print_adj_list())
                for u, v, w in other_edges:
                    graph.super_del(u, v, w)
                for u, v, w in default_edges:
                    graph.super_add(u, v, w)
                print("The updated graph is: ")
                print(graph.print_adj_list())
                if reset:
                    reset = False
                    break

        else:
            print("You must only select either 1, 2, 3 or 4")
            print("Please try again")
            menu()


menu()

# Adrian Chen
# Assignment 5
# CSCI 3202
import argparse
import math

WIDTH = 10
HEIGHT = 8

def read_graph(f, g, height):
    # Read file, then create nodes in graph g for each entry in the matrix
    list_index = 0
    # We read from top to bottom
    y = height-1
    for line in f:
        if line:
            # Keeps track of x coordinate (read in order)
            x = 0
            # Split on space to get each entry
            vals = str.split(line)
            for v in vals:
                n = Node(v)
                n.set_loc(x,y)
                g.add_to_data(n, list_index)
                x += 1
            y -= 1
            list_index += 1

class Graph:

    def __init__(self, width, height, epsilon, discount):
        self.width = width
        self.height = height
        self.epsilon = float(epsilon)
        self.discount = float(discount)
        self.data = []
        # 2d array of Nodes
        for i in range(0, height):
            self.data.append([])



    def add_to_data(self, node, x):
        self.data[x].append(node)

    def print_graph(self):
        for i in range(0, self.height):
            line = ""
            for j in range(0, self.width):
                try:
                    line += str("{0:.2f}".format(self.data[i][j].utility)) + "\t"
                except ValueError:
                    line += "None\t"
            print line
    
    def get(self, x, y):
        # Get node at given location, or if it doesn't exist return None
        if (x < 0) or (y < 0) or (x > WIDTH-1) or (y > HEIGHT-1): 
            return None
        else:
            for l in self.data:
                for n in l:
                    if n.x is x and n.y is y:
                        if n.val == 2:
                            return None
                        return n

    # TODO: don't change utility of end states
    def find_utility(self):
        max_change = 100
        while max_change >= self.epsilon*(1-self.discount)/self.discount:
            max_change = -100
            for i in range(0, self.width):
                for j in range(0, self.height):
                        current_node = self.get(i, j)
                        above_node = self.get(i, j+1)
                        below_node = self.get(i, j-1)
                        left_node = self.get(i-1, j)
                        right_node = self.get(i+1, j)
                        if current_node != None and current_node.val != 50:
                            above_node_utility = None
                            below_node_utility = None
                            left_node_utility = None
                            right_node_utility = None

                            if above_node == None:
                                above_node_utility = current_node.utility
                            else:
                                above_node_utility = above_node.utility
                            if below_node == None:
                                below_node_utility = current_node.utility
                            else:
                                below_node_utility = below_node.utility
                            if left_node == None:
                                left_node_utility = current_node.utility
                            else:
                                left_node_utility = left_node.utility
                            if right_node == None:
                                right_node_utility = current_node.utility
                            else:
                                right_node_utility = right_node.utility


                            up = 0.8*above_node_utility + 0.1*left_node_utility + 0.1*right_node_utility
                            down = 0.8*below_node_utility + 0.1*left_node_utility + 0.1 * right_node_utility
                            left = 0.8*left_node_utility + 0.1*above_node_utility + 0.1*below_node_utility
                            right = 0.8*right_node_utility + 0.1*above_node_utility + 0.1*below_node_utility
                            previous_utility = current_node.utility
                            current_node.utility = max(up, down, left, right) + current_node.reward
                            current_node.utility *= self.discount
                            if abs(current_node.utility - previous_utility) > max_change:
                                max_change = abs(current_node.utility - previous_utility)

class Node:
    def __init__(self, val):
        self.val = int(val)
        # Add these t  simplify
        self.x = 0
        self.y = 0
        self.parent = None
        if self.val == 0:
            self.reward = 0
            self.utility = 0
        elif self.val == 1:
            self.reward = -1
            self.utility = -1
        elif self.val == 2:
            self.reward = None
            self.utility = None
        elif self.val == 3:
            self.reward = -2
            self.utility = -2
        elif self.val == 4:
            self.reward = 1
            self.utility = 1
        elif self.val == 50:
            self.reward = 50
            self.utility = 50
        else:
            raise ValueError('Unexpected Node Value')

    def set_loc(self, x, y):
        # Set x and y coords for a node
        self.x = x
        self.y = y

class markov:
    # The maximum number to follow when printing path, in case we have a loop
    MAX_PATH_LENGTH = 100
    
    def __init__(self, start, end, g):
        self.path = []
        self.utilities = []
        self.start = start
        self.end = end
        self.g = g
    
    def find_path(self):
        # find optimal path
        self.g.find_utility()
        self.path.append(self.start)
        self.utilities.append(self.start.utility)
        current_node = self.start
        while True:
            above_node = self.g.get(current_node.x, current_node.y+1)
            below_node = self.g.get(current_node.x, current_node.y-1)
            left_node = self.g.get(current_node.x-1, current_node.y)
            right_node = self.g.get(current_node.x+1, current_node.y)
        
            above_node_utility = None
            below_node_utility = None
            left_node_utility = None
            right_node_utility = None
            if above_node == None:
                above_node_utility = float("-inf")
            else:
                above_node_utility = above_node.utility
            if below_node == None:
                below_node_utility = float("-inf")
            else:
                below_node_utility = below_node.utility
            if left_node == None:
                left_node_utility = float("-inf")
            else:
                left_node_utility = left_node.utility
            if right_node == None:
                right_node_utility = float("-inf")
            else:
                right_node_utility = right_node.utility

            if current_node.utility > max(above_node_utility, below_node_utility, left_node_utility, right_node_utility):
                raise ValueError('Graph stuck before final node')
            elif above_node_utility == max(above_node_utility, below_node_utility, left_node_utility, right_node_utility):
                current_node = above_node
            elif below_node_utility == max(above_node_utility, below_node_utility, left_node_utility, right_node_utility):
                current_node = below_node
            elif right_node_utility == max(above_node_utility, below_node_utility, left_node_utility, right_node_utility):
                current_node = right_node
            else:
                current_node = left_node

            self.path.append(current_node)
            self.utilities.append(current_node.utility)

            if current_node is self.end:
                break
        
        self.print_output()

        

        
    def print_output(self):
        # Print assignment specified output
        path = ""
        utilities = ""
        for node in self.path:
            path += "(" + str(node.x) + ", " + str(node.y) + "),  "
        for u in self.utilities:
            utilities += str(u) + "  "
        print """
=======================================MDP==========================================
Successfully finished pathfinding using Markov Decision Processes.
The optimal path was: 
%s
The utilities along that path were:
%s
====================================================================================
        """ % (path, utilities)

if __name__ == "__main__":
    # Command line parser
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="The name of the file to treat as the search space")
    parser.add_argument("epsilon", help="Our epsilon value to check if our utilities are final")
    parser.add_argument("discount", help="Our discount value for each iteration of utility calculation")
    args = parser.parse_args()

    # open file
    f = open(args.input_file, 'r');
    g = Graph(WIDTH, HEIGHT, args.epsilon, args.discount)

    # Read the graph from txt
    read_graph(f, g, HEIGHT)
    markov = markov(g.get(0,0), g.get(WIDTH-1,HEIGHT-1), g)
    markov.find_path()


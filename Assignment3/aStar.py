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

    def __init__(self, width, height):
        self.width = width
        self.height = height
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
                line += str(self.data[i][j].val) + " "
            print line
    
    def get(self, x, y):
        # Get node at given location, or if it doesn't exist return None
        if x < 0 or y < 0:
            return None
        else:
            for l in self.data:
                for n in l:
                    if n.x is x and n.y is y:
                        return n

    def setup_edges_node(self, node):
        # For any given node, return all adjacent nodes that are valid
        adjacent=[]
        x = node.x
        y = node.y
        # All possible adjacent nodes
        down_left = self.get(x-1,y-1)
        down = self.get(x,y-1)
        down_right = self.get(x+1,y-1)
        right = self.get(x+1,y)
        up_right = self.get(x+1,y+1)
        up = self.get(x,y+1)
        up_left = self.get(x-1,y+1)
        left = self.get(x-1, y)
        
        for node in [down_left, down, down_right, right, up_right, up, up_left, left]:
            # Don't count as adjacent if it's a wall
            if node is not None and node.val is not 2:
                # Set costs (diag different)
                additional_cost = 0
                if node in [down_left, down_right, up_left, up_right]:
                    additional_cost = 14
                else:
                    additional_cost = 10
                
                # We have extra cost if space is a mountain
                if node.val is 1:
                    additional_cost += 10

                adjacent.append([node,additional_cost])
        return adjacent

    def setup_edges(self,x,y):
        # Wraps setup_edges_node if we only have the grid location
        node = self.get(x,y)
        return setup_edges_node(node)

class Node:

    def __init__(self, val):
        self.val = int(val)
        # Add these t  simplify
        self.x = 0
        self.y = 0
        self.parent = None
        # Cost so far 
        self.g = 0
        # Cost of heuristic
        self.h = 0
        # Sum total cost
        self.cost = 0

    def set_loc(self, x, y):
        # Set x and y coords for a node
        self.x = x
        self.y = y

class aStar:
    # The maximum number to follow when printing path, in case we have a loop
    MAX_PATH_LENGTH = 100
    
    def __init__(self, start, end, g, heuristic):
        self.path = []
        self.start = start
        self.end = end
        self.chosen_heuristic = heuristic
        self.g = g
        # Track locations evaluated for assignment - begin at 1 for start node
        self.locations_evaluated = 1 

    def heuristic(self, n):
        # Dispatches to correct heurstic function
        if self.chosen_heuristic == "manhattan":
            return self.manhattan(n)
        elif self.chosen_heuristic =="diagonal":
            return self.diagonal(n)
        else:
            raise Exception('Invalid choice of heuristic')
    
    def manhattan(self, n):
            return 10 * abs(n.x - self.end.x) +  10 * abs(n.y-self.end.y)

    def diagonal(self, n):
        dx = abs(n.x - self.end.x)
        dy = abs(n.y - self.end.y)
        return 10 * (dx + dy) + (14 - 20) * min(dx, dy)
        
    def update_node(self, node, parent, move_cost):
        # Update information for a given node - specifically cost and parent
        node.parent = parent
        # Update actual distance
        node.g = move_cost + parent.g
        # Update heuristic
        node.h = self.heuristic(node)
        # Set final cost
        node.cost = node.g + node.h
    
    def search(self):
        # Run actual search algorithm
        # Begin at start node
        open = [self.start]
        closed = []
        while len(open) > 0:
            # Grab minimum cost node out of list
            node = min(open, key=lambda n: n.cost)
            open.remove(node)
            if node is not self.end:
                # If we haven't found the end 
                closed.append(node)
                # Add adjacent edges
                for (adj, move_cost) in self.g.setup_edges_node(node):
                    # As long as it is not already finished
                    if adj not in closed:
                        if adj in open:
                                # Check if current path is better than previously found path
                            if adj.g > (node.g + move_cost):
                                self.update_node(adj, node, move_cost)
                        else:
                            # Otherwise give it info for the first time and add it to open
                            self.update_node(adj, node, move_cost)
                            open.append(adj)
                            self.locations_evaluated = self.locations_evaluated + 1
            else:
                self.print_output() 
                break
        
    def print_output(self):
        # Print assignment specified output
        path = self.get_path(self.end)
        print """
=====================================A* Search======================================
Successfully finished pathfinding using A* search with the %s heuristic.
The final cost of the path was %d.
The number of locations traveled was %d.
The optimal path was: 
%s
====================================================================================
        """ % (self.chosen_heuristic, self.end.cost, self.locations_evaluated, path)
        
    def get_path(self, node):
        # Get path to a given node from the start node
        path = []
        cursor = node
        # Maximum just in case
        for i in range(0,self.MAX_PATH_LENGTH):
            if cursor:
                path.append((cursor.x, cursor.y))
                cursor = cursor.parent
        # We want it in reverse order
        return path[::-1]

if __name__ == "__main__":
    # Command line parser
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="The name of the file to treat as the search space")
    parser.add_argument("heuristic", help="Name of search heuristic to use in A* search", 
        choices=("manhattan", "diagonal"), default="manhattan")
    args = parser.parse_args()

    # open file
    f = open(args.input_file, 'r');
    g = Graph(WIDTH, HEIGHT)

    # Read the graph from txt
    read_graph(f, g, HEIGHT)

    # Create and perform A* search
    search = aStar(g.get(0,0), g.get(WIDTH-1,HEIGHT-1), g, args.heuristic)
    search.search()
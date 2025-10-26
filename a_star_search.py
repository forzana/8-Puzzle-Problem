# Forzana Rime & Mohammed Uddin
# CS-GY 6613 AI Project 1

import os
from typing import Any, List
from heapq import *
from copy import deepcopy

input_directory_path = "./actual/input" # The location of the input files
output_directory_path = "./actual/output" # Where the output files will go

# Defines each node in our tree
class Node:
    # Initializes the node given parent node, current state, action to get here, f(n) val, and path cost
    def __init__(self, parent: Any, state: str, action_to_get_here: str, function_cost: int, path_cost: int):
        self.parent = parent # Pointer to the parent node
        self.state = state # Current state
        self.action_to_get_here = action_to_get_here # L, R, U, D action from parent state to current state
        self.function_cost = function_cost # The f(n) val at this node
        self.path_cost = path_cost # The path cost at this node; also the depth of this node

    # Define what it means to be less than; used for the frontier or priority queue
    def __lt__(self, other):
        return self.function_cost < other.function_cost

    # Helper function to generate the sequence of actions and f(n) vals for the output file
    def get_info(self):
        f_vals = []
        actions = []
        curr = self
        while curr:
            f_vals.append(str(curr.function_cost))
            if curr.action_to_get_here:
                actions.append(curr.action_to_get_here)
            curr = curr.parent
        
        return " ".join(f_vals[::-1]), " ".join(actions[::-1])

# Store the position (row and column) of each square in a dictionary
# This will be used to calculate Manhattan distance
def encode_locations(arr):
    obj = {}
    for row in range(3):
        for col in range(3):
            obj[arr[row][col]] = [row, col]
    return obj

# Stringifies the state so we can easily look it up in our reached table
def stringify(state):
    stringified = "".join(["".join(row) for row in state])
    return stringified

# h1(n) = the sum of the Manhattan distances of the tiles from their goal positions
def h1n(curr_state, goal_state):
    curr = encode_locations(curr_state)
    goal = encode_locations(goal_state)
    sum = 0
    # Calc the Manhattan distance for each tile excluding the blank and add it to the sum
    for item in curr.keys():
        if item != '0':
            sum += abs(goal.get(item)[0] - curr.get(item)[0]) + abs(goal.get(item)[1] - curr.get(item)[1])
    return sum

# h2(n) = h1(n) + 2 * number of linear conflicts
def h2n(curr_state, goal_state):
    linear_conf = 0
    # Linear conflicts by row
    for i in range(3):
        curr = [
            (curr_state[i][0], curr_state[i][1]), 
            (curr_state[i][0], curr_state[i][2]), 
            (curr_state[i][1], curr_state[i][2])
        ]
        goal = [
            (goal_state[i][0], goal_state[i][1]), 
            (goal_state[i][0], goal_state[i][2]), 
            (goal_state[i][1], goal_state[i][2])
        ]
        for i,j in curr:
            if i != '0' and j != '0' and (j,i) in goal:
                linear_conf += 1

    # Linear conflicts by column
    for i in range(3):
        curr = [
            (curr_state[0][i], curr_state[1][i]), 
            (curr_state[0][i], curr_state[2][i]), 
            (curr_state[1][i], curr_state[2][i])
        ]
        goal = [
            (goal_state[0][i], goal_state[1][i]), 
            (goal_state[0][i], goal_state[2][i]), 
            (goal_state[1][i], goal_state[2][i])
        ]
        for i,j in curr:
            if i != '0' and j != '0' and (j,i) in goal: 
                linear_conf += 1
    
    total = h1n(curr_state, goal_state) + 2 * linear_conf 
    return total

# Expand function to generate child nodes, yields children
def expand(node, goal, heuristic_func):
    state = node.state
    zero_x, zero_y = encode_locations(state).get('0') # Find the position of the blank (0)
    for i, j, action in [(0,1,'R'), (1,0,'D'), (-1,0,'U'), (0,-1,'L')]: # Go through each potential action
        if not (-1 < zero_x + i < 3 and -1 < zero_y + j < 3): # Ignore the moves that will result in the same state
            continue
        
        h = zero_x + i
        k = zero_y + j

        new_state = deepcopy(state)
        new_state[h][k],new_state[zero_x][zero_y] = new_state[zero_x][zero_y], new_state[h][k] # Move the blank (0) 

        function_cost = node.path_cost + 1 + heuristic_func(new_state, goal) # Calculate the f(n) val 
        
        yield Node(node, new_state, action, function_cost, node.path_cost + 1) # Yield the child node generated with the action

# This function performs the A* search with the provided heuristic function
# Returns the goal node and the reached table
def search(initial, goal, heuristic_func):
    path_cost = 0
    curr = Node(None, initial, None, heuristic_func(initial, goal), path_cost) # Create a node for the current state
    reached = {} # Our reached table; keys are the state stringified and values are the f(n) values
    frontier = [curr] # min heap; priority queue frontier
    while frontier:
        node = heappop(frontier)

        # Check to see if we have the goal state
        if node.state == goal:
            return node, reached
        
        # Expand the node and generate children
        for child in expand(node, goal, heuristic_func):
            child_state = child.state
            s = stringify(child_state)
            # Add the child to the frontier only if we should
            if (s not in reached or child.function_cost < reached.get(s)):
                reached[s] = child.function_cost
                heappush(frontier, child)

    return None, reached # Return this if the search failed

# This function takes each input file and splits it into an initial and goal state
def parse_input():
    # Process each input text file
    for entry_name in os.listdir(input_directory_path):
        full_path = os.path.join(input_directory_path, entry_name)
        if os.path.isfile(full_path):
            # Open the file and grab the contents
            test_file = open(full_path)
            test_file_content = test_file.read()
            test_file.close()

            # Break it up into initial and goal state matrices
            initial_state = list(map(lambda x: x.split(' '), test_file_content.split('\n\n')[0].split('\n')))
            goal_state = list(map(lambda x: x.split(' '), test_file_content.split('\n\n')[1].split('\n')))

            # Yield the original content, initial state matrix, goal state matrix, and the problem number
            yield test_file_content, initial_state, goal_state, entry_name.replace('Input', '').replace('.txt', '')

def main():
    # For each problem (input file)
    for content, initial_state, goal_state, problem_number in parse_input():
        # For each heuristic function
        for func, index in [(h1n, "h1"), (h2n, "h2")]:
            output_file = open(f"{output_directory_path}/output{problem_number}{index}.txt", "w") # Write to an output file with the naming convention required
            output_file.write(content + "\n\n") # Write the input file content
            goal_node, reached = search(initial_state, goal_state, func) # Perform the A* search with the appropriate heuristic function
            if not goal_node: # Search was not successful
                print("failure")
                continue
            function_costs, actions = goal_node.get_info() # function costs and actions from the initial to the goal
            output_file.write(str(goal_node.path_cost) + "\n") # path cost of the goal node will tell us the depth of our shallowest goal
            output_file.write(str(len(reached)) + "\n") # Number of nodes in our tree is the size of the reached table
            output_file.write(actions + "\n") # actions list
            output_file.write(function_costs) # f(n) values list
            output_file.close()

main()
import os

directory_path = "./test/input" # The location of the input files

# Helper functions
# Store the row and column of each square in a dictionary
# This will be used to calculate Manhattan Distance
def encode_locations(arr, obj):
    for row in range(3):
        for col in range(3):
            obj[arr[row][col]] = [row, col]
    return obj

# Stringifies the state so we can easily look it up in our visited dict
def stringify(state):
    stringified = "".join(["".join(row) for row in state])
    return stringified

# h1(n) = the sum of the Manhattan distances of the tiles from their goal positions
def h1n(curr, goal):
    print("curr", curr)
    print("goal", goal)
    sum = 0
    for item in curr.keys():
        sum += abs(goal.get(item)[0] - curr.get(item)[0]) + abs(goal.get(item)[1] - curr.get(item)[1])
    print("sum", sum)
    return sum

def heuristic1(initial, goal, problem=""):
    # if (problem):
    #     output = open(f"output{problem}h1.txt", "w")
    curr = initial
    step_cost = 0
    visited = {} 
    # Need to declare a priority queue fronteir
    stringify(curr)
    while (curr != goal):
        # Calculate f
        f = h1n(encode_locations(curr, {}), encode_locations(goal, {})) + step_cost
        s = stringify(curr)
        if (s not in visited or f < visited.get(s)):
            visited[s] = f
            # Add it to the fronteir
        step_cost += 1
    return

# h2(n) = h1(n) + 2 * number of linear conflicts
def h2n(curr, goal):
    linear_conf = 0
    return h1n(curr, goal) + 2 * linear_conf

def heuristic2(initial, goal, problem):
    # output = open(f"output{problem}h2.txt", "w")
    curr = initial
    step_cost = 0
    while (curr != goal):
        # Calculate f
        f = h2n(encode_locations(curr, {}), encode_locations(goal, {})) + step_cost
        step_cost += 1
    return

# Process each input text file
for entry_name in os.listdir(directory_path):
    full_path = os.path.join(directory_path, entry_name)
    if os.path.isfile(full_path):
        print(f"Processing file: {entry_name}")

        # Open the file and store contents
        test_file = open(full_path)
        test_file_content = test_file.read()
        test_file.close()
        print(test_file_content)

        # Break it up into initial and goal state
        initial_state = list(map(lambda x: x.split(' '), test_file_content.split('\n\n')[0].split('\n')))
        print("\nInitial state:", initial_state)
        goal_state = list(map(lambda x: x.split(' '), test_file_content.split('\n\n')[1].split('\n')))
        print("Goal state:", goal_state)

        # Perform A* search with heuristic functions
        heuristic1(initial_state, goal_state, entry_name.replace('.txt', ''))
        # heuristic2(initial_state, goal_state, entry_name.replace('.txt', ''))
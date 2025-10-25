import os

directory_path = "./test/input" # The location of the input files

# Helper functions
# Store the row and column of each square in a dictionary
# This will be used to calculate Manhattan Distance
def encode_locations(arr, obj):
    for row in range(3):
        for col in range(3):
            obj[arr[row][col]] = [row, col]
    print("\n", obj)
    return obj

# h1(n) = the sum of the Manhattan distances of the tiles from their goal positions
def h1(initial, goal, problem=""):
    # if (problem):
    #     output = open(f"output{problem}h1.txt")
    while (initial != goal):
        curr = encode_locations(initial, {})

    return

# h2(n) = h1(n) + 2 * number of linear conflicts
def h2(initial, goal, problem):
    # output = open(f"output{problem}h2.txt")
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
        h1(initial_state, goal_state, entry_name.replace('.txt', ''))
        h2(initial_state, goal_state, entry_name.replace('.txt', ''))
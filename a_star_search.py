import os

directory_path = "./test/input"

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
from collections import deque
import copy

def dfs_solve(initial_puzzle):
    print("in dfs")
    stack = [(initial_puzzle, [])]  # Initialize the stack with the initial puzzle state and an empty path
    visited = set()  # Keep track of visited states

    while stack:
        current_puzzle, path = stack.pop()
        current_state = tuple(map(tuple, current_puzzle.board))  # Convert the puzzle state to a tuple for hashing

        if current_puzzle.checkWin():
            print(f"Found solution! Puzzle state:\n{current_puzzle}")
            return path

        if current_state not in visited:
            visited.add(current_state)

            for direction in current_puzzle.directions:  # Use the directions from the puzzle
                child = current_puzzle.create_child(direction)
                if child:
                    child_state = tuple(map(tuple, child.board))  # Convert the child state to a tuple for hashing
                    if child_state not in visited:  # Check if the child state is not already visited
                        # print(f"Adding child to stack: {child}")
                        # print(f"Current path: {path}")
                        stack.append((child, path + [direction]))
                        print("creating")

    return None  # Return None if no solution is found

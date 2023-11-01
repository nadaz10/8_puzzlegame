from collections import deque

def bfs_solve(Puzzle):
    print("in bfs")
    queue = deque([(Puzzle, [])])  # Initialize the queue with the initial puzzle state and an empty path
    visited = set()  # Keep track of visited states
    while queue:
        current_puzzle, path = queue.popleft()
        current_state = tuple(map(tuple, current_puzzle.board))  # Convert the puzzle state to a tuple for hashing

        if current_puzzle.checkWin():
            print(f"Found solution! Puzzle state:\n{current_puzzle}")
            return path

        if current_state not in visited:
            visited.add(current_state)

            for direction in current_puzzle.directions:
                child = current_puzzle.create_child(direction)
                child_state = tuple(map(tuple, child.board))  # Convert the child state to a tuple for hashing
                if child and child_state not in visited:  # Check if the child state is not already visited
                    print(f"Adding child to queue: {child}")
                    print(f"Current path: {path}")
                    queue.append((child, path + [direction]))
                    print("creating")

    return None  # Return None if no solution is found

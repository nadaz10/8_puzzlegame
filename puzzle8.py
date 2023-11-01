from random import choice
import copy
class Puzzle:

    UP = (1, 0)
    DOWN = (-1, 0)
    LEFT = (0, 1)
    RIGHT = (0, -1)
    
    directions = {'UP': UP, 'DOWN': DOWN, 'LEFT': LEFT, 'RIGHT': RIGHT}
    
    def __init__(self, parent=None, boardSize=3):
        self.boardSize = boardSize
        self.board = [[0] * boardSize for _ in range(boardSize)]
        self.blankPos = (0, 0)
        self.child = None

        if parent is None:
            self.initialize_board()

    def initialize_board(self):
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                self.board[i][j] = i * self.boardSize + j
        self.board[0][0] = 0
        self.shuffle()
    def __hash__(self):
        # Convert the board state to a tuple to make it hashable
        board_tuple = tuple(tuple(row) for row in self.board)
        return hash(board_tuple)
    def __lt__(self, other):
        # Define the less than operator
        return self.heuristic() < other.heuristic()
    
    def __gt__(self, other):
        # Define the greater than operator
        return self.heuristic() > other.heuristic()
    
    def __le__(self, other):
        # Define the less than or equal to operator
        return self.heuristic() <= other.heuristic()
    
    def __ge__(self, other):
        # Define the greater than or equal to operator
        return self.heuristic() >= other.heuristic()
    
    def __eq__(self, other):
    # Compare the board states directly
        return self.board == other.board

    
    def __ne__(self, other):
        # Define the not equal to operator
        return self.heuristic() != other.heuristic()

    def __str__(self):
        outStr = ''
        for i in self.board:
            outStr += '\t'.join(map(str, i))
            outStr += '\n'
        return outStr

    def __getitem__(self, key):
        return self.board[key]

    def shuffle(self):
        print("in shuffle")
        numberShuffles = 100
        for i in range(numberShuffles):
            direction = choice(list(self.directions.keys()))
            self.move(direction)

    def move(self, direction):
        newBlankPos = (self.blankPos[0] + self.directions[direction][0], self.blankPos[1] + self.directions[direction][1])
        if not (0 <= newBlankPos[0] < self.boardSize and 0 <= newBlankPos[1] < self.boardSize):
            return False
        
        self.board[self.blankPos[0]][self.blankPos[1]] = self.board[newBlankPos[0]][newBlankPos[1]]
        self.board[newBlankPos[0]][newBlankPos[1]] = 0
        self.blankPos = newBlankPos
        return True

    def checkWin(self):
        expected_board = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8]
        ]

        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if self.board[i][j] != expected_board[i][j]:
                    return False
        
        return True

    def create_child(self, direction):
        print("creating")
        child = copy.deepcopy(self)
        child.move(direction)
        return child
    def get_neighbors(self):
        neighbors = [self.create_child(direction) for direction in self.directions.keys() if self.create_child(direction) is not None]
        return neighbors

    def set_state(self, initial_state):
        self.board = initial_state
        for i in range(len(initial_state)):
            for j in range(len(initial_state[i])):
                if initial_state[i][j] == 0:
                    self.blankPos = (i, j)
    def is_solvable(self):
        flat_puzzle = [tile for row in self.board for tile in row if tile != 0]
        inversions = 0

        for i in range(len(flat_puzzle)):
            for j in range(i + 1, len(flat_puzzle)):
                if flat_puzzle[i] > flat_puzzle[j]:
                    inversions += 1

        if self.boardSize % 2 == 1:
            return inversions % 2 == 0
        else:
            blank_row = next(i for i, row in enumerate(self.board) if 0 in row)
            return (inversions + blank_row) % 2 == 1
        
            
    def heuristic(state):
        # Manhattan distance heuristic
        distance = 0
        for i in range(3):
            for j in range(3):
                value = state.board[i][j]
                if value != 0:
                    target_row = (value - 1) // 3
                    target_col = (value - 1) % 3
                    distance += abs(i - target_row) + abs(j - target_col)
        return distance
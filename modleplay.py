import pygame
import sys
import puzzle8
from bfs_solution import bfs_solve
from dfs_solution import dfs_solve
from astar_solution import a_star_solve

pygame.init()
board_size = 3

size = width, height = 300, 300
screen = pygame.display.set_mode(size)
pygame.display.set_caption('{} Puzzle'.format(board_size**2-1))

# Fonts
tileFont = pygame.font.SysFont("", 72)

# Colors
black = (0, 0, 0)
borderColor = (92, 90, 86)
tileColor = (242, 197, 133)
fontColor = black

game_running = True
animate_solution_flag = True
bfs_flag = False
dfs_flag = False
astar_flag = False  # New flag for A*
move_counter = 0
bfs_counter = 0
dfs_counter = 0
astar_counter = 0  # Counter for A*
astarmoves = []  # List to store A* solution moves
astar_index = 0 


def gameLoop():
    global game_running, animate_solution_flag, bfs_flag, dfs_flag, astar_flag, move_counter
    global bfs_counter, dfs_counter, astar_counter, astarmoves, astar_index

    clock = pygame.time.Clock()
    puzzle = puzzle8.Puzzle()

    while game_running:
        for event in pygame.event.get():
            handleInput(event, puzzle)
        if bfs_flag:
            solution_path = bfs_solve(puzzle)
            if solution_path:
                animate_solution(solution_path, puzzle)
                bfs_counter = len(solution_path) - 1  # Count moves for BFS
                print(f"BFS: Number of moves - {bfs_counter}")
                bfs_flag = False  # Disable BFS

        if dfs_flag:
            solution_path = dfs_solve(puzzle)
            if solution_path:
                for puzzle_state in solution_path:
                    print(puzzle_state)
                # animate_solution(solution_path, puzzle)
                dfs_counter = len(solution_path) - 1
                print(f"DFS: Number of moves - {dfs_counter}")
                dfs_flag = False
                
        
        if astar_flag:  # Check if A* flag is set
            if not astarmoves:  # If A* solution moves are empty, calculate them
                astarmoves = a_star_solve(puzzle)
                if astarmoves:
                    astar_counter = len(astarmoves) - 1
                    print(f"A*: Number of moves - {astar_counter}")
                    astar_flag = False  # Disable A* after calculating the solution

            if astarmoves:  # If there are A* solution moves, animate them
                # animate_solution( puzzle, astar_index)
                astar_index += 1  # Increment A* solution index
                if astar_index >= len(astarmoves):  # Reset A* animation if at the end
                    astarmoves = []
                    astar_index = 0
        drawPuzzle(puzzle)
        pygame.display.flip()

        clock.tick(10)  # Limit the frame rate


def handleInput(event, puzzle):
    global bfs_flag, dfs_flag, astar_flag, move_counter
    global bfs_counter, dfs_counter, astar_counter,astarmoves

    if event.type == pygame.QUIT:
        sys.exit()
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_r:
            puzzle.shuffle()
            bfs_flag = False
            dfs_flag = False
            astar_flag = False
            move_counter = 0
        elif event.key == pygame.K_b:
            bfs_flag = True
            dfs_flag = False
            astar_flag = False
        elif event.key == pygame.K_d:
            dfs_flag = True
            bfs_flag = False
            astar_flag = False
        elif event.key == pygame.K_a:
            astar_flag = True
            bfs_flag = False
            dfs_flag = False
            astar_counter = 0
            astarmoves = []
            
    elif event.type == pygame.MOUSEBUTTONUP:
        pos = pygame.mouse.get_pos()
        puzzleCoord = (pos[1] * puzzle.boardSize // height,
                       pos[0] * puzzle.boardSize // width)
        dir = (puzzleCoord[0] - puzzle.blankPos[0],
               puzzleCoord[1] - puzzle.blankPos[1])
        if dir == puzzle.RIGHT:
            puzzle.move(puzzle.RIGHT)
            move_counter += 1
        elif dir == puzzle.LEFT:
            puzzle.move(puzzle.LEFT)
            move_counter += 1
        elif dir == puzzle.DOWN:
            puzzle.move(puzzle.DOWN)
            move_counter += 1
        elif dir == puzzle.UP:
            puzzle.move(puzzle.UP)
            move_counter += 1


def drawPuzzle(puzzle):
    screen.fill(black)

    for i in range(puzzle.boardSize):
        for j in range(puzzle.boardSize):
            currentTileColor = tileColor
            numberText = str(puzzle[i][j])

            if puzzle[i][j] == 0:
                currentTileColor = borderColor
                numberText = ''

            rect = pygame.Rect(j * width / puzzle.boardSize,
                               i * height / puzzle.boardSize,
                               width / puzzle.boardSize,
                               height / puzzle.boardSize)

            pygame.draw.rect(screen, currentTileColor, rect)
            pygame.draw.rect(screen, borderColor, rect, 1)

            fontImg = tileFont.render(numberText, 1, fontColor)
            screen.blit(fontImg,
                        (j * width / puzzle.boardSize + (width / puzzle.boardSize - fontImg.get_width()) / 2,
                         i * height / puzzle.boardSize + (height / puzzle.boardSize - fontImg.get_height()) / 2))


def animate_solution(solution, puzzle):
    global game_running
    for move in solution:
        puzzle.move(move)
        drawPuzzle(puzzle)
        pygame.display.flip()
        pygame.time.delay(1000)

        # Handle events during animation
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                sys.exit()


if __name__ == "__main__":
    gameLoop()
    print(f"Number of moves: {move_counter}")

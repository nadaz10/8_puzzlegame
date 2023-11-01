from puzzle8 import Puzzle
import copy
import heapq

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

def a_star_solve(initial_state):
    open_set = [(heuristic(initial_state), 0, initial_state)]
    heapq.heapify(open_set)
    closed_set = set()
    g_scores = {initial_state: 0}
    parents = {initial_state: None}

    while open_set:
        _, g_score, current_state = heapq.heappop(open_set)

        if current_state.checkWin():
            path = []
            while current_state is not None:
                path.append(current_state)
                current_state = parents[current_state]
            return list(reversed(path))

        closed_set.add(current_state)

        for move in current_state.directions:
            successor = copy.deepcopy(current_state)
            if successor.move(move):
                tentative_g_score = g_score + 1

                if successor in closed_set and tentative_g_score >= g_scores[successor]:
                    continue

                if tentative_g_score < g_scores.get(successor, float('inf')):
                    parents[successor] = current_state
                    g_scores[successor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(successor)
                    heapq.heappush(open_set, (f_score, tentative_g_score, successor))

    return None
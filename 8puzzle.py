from collections import deque
import heapq

# Helper functions

def swap_tiles(state, pos1, pos2):
    new_state = state[:]
    new_state[pos1], new_state[pos2] = new_state[pos2], new_state[pos1]
    return new_state

def print_solution(path):
    for i, state in enumerate(path):
        print("Step", i)
        print_state(state)
        print()

def print_state(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()

def is_goal(state):
    return state == goal_state

def get_possible_moves(pos):
    moves = []
    row, col = pos // 3, pos % 3

    if row > 0:
        moves.append(pos - 3)  # Move Up
    if row < 2:
        moves.append(pos + 3)  # Move Down
    if col > 0:
        moves.append(pos - 1)  # Move Left
    if col < 2:
        moves.append(pos + 1)  # Move Right

    return moves

def iterative_deepening_dfs(initial_state, max_depth):
    for depth in range(max_depth + 1):
        result = dfs_recursive(initial_state, depth, set())
        if result is not None:
            return result
    return None

# Algorithms

def bfs(initial_state):
    queue = deque([(initial_state, [])])
    visited = set()

    while queue:
        state, path = queue.popleft()
        visited.add(tuple(state))

        if is_goal(state):
            return path + [state]

        empty_tile = state.index(0)
        possible_moves = get_possible_moves(empty_tile)

        for move in possible_moves:
            new_state = swap_tiles(state, empty_tile, move)
            if tuple(new_state) not in visited:
                queue.append((new_state, path + [state]))

    return None


def dfs_recursive(state, depth, visited):
    if depth == 0:
        return None
    if is_goal(state):
        return [state]
    
    visited.add(tuple(state))
    empty_tile = state.index(0)
    possible_moves = get_possible_moves(empty_tile)
    
    for move in possible_moves:
        new_state = swap_tiles(state, empty_tile, move)
        if tuple(new_state) not in visited:
            result = dfs_recursive(new_state, depth - 1, visited)
            if result is not None:
                return [state] + result
    
    visited.remove(tuple(state))
    return None

def h(state):
    # Heuristic function for Hill Climbing and A*
    return sum(1 for i in range(9) if state[i] != goal_state[i])

def hill_climbing(initial_state):
    current_state = initial_state
    while True:
        if is_goal(current_state):
            return [current_state]
        
        empty_tile = current_state.index(0)
        possible_moves = get_possible_moves(empty_tile)
        next_states = [swap_tiles(current_state, empty_tile, move) for move in possible_moves]
        next_states.sort(key=h)
        
        if h(next_states[0]) >= h(current_state):
            return None
        
        current_state = next_states[0]

def a_star(initial_state):
    queue = [(h(initial_state), 0, initial_state, [])]
    visited = set()

    while queue:
        _, cost, state, path = heapq.heappop(queue)
        visited.add(tuple(state))

        if is_goal(state):
            return path + [state]

        empty_tile = state.index(0)
        possible_moves = get_possible_moves(empty_tile)

        for move in possible_moves:
            new_state = swap_tiles(state, empty_tile, move)
            if tuple(new_state) not in visited:
                new_cost = cost + 1
                heapq.heappush(queue, (new_cost + h(new_state), new_cost, new_state, path + [state]))

# Main

initial_state = [
    1, 2, 0,
    4, 5, 3, 
    7, 8, 6
]
goal_state = [
    1, 2, 3,
    4, 5, 6, 
    7, 8, 0
]

print("Initial State:")
print_state(initial_state)

print("BFS Solution:")
bfs_solution = bfs(initial_state)
if bfs_solution:
    print_solution(bfs_solution)
else:
    print("No solution found for BFS.")


max_dfs_depth = 50  # Set the maximum depth for DFS
print("DFS Solution:")
iterative_dfs_solution = iterative_deepening_dfs(initial_state, max_dfs_depth)
if iterative_dfs_solution:
    print_solution(iterative_dfs_solution)
else:
    print("No solution found for DFS.")


print("Hill Climbing Solution:")
hill_climbing_solution = hill_climbing(initial_state)
if hill_climbing_solution:
    print_solution(hill_climbing_solution)
else:
    print("No solution found for Hill Climbing.")


print("A* Solution:")
a_star_solution = a_star(initial_state)
if a_star_solution:
    print_solution(a_star_solution)
else:
    print("No solution found for A*.")

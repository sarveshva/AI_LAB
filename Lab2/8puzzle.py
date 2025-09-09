goal_state = ((1, 2, 3), (8, 0, 4), (7, 6, 5))

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def is_valid_move(row, col):
    return 0 <= row < 3 and 0 <= col < 3

def get_neighbors(state):
    zero_row, zero_col = next((r, c) for r in range(3) for c in range(3) if state[r][c] == 0)
    neighbors = []

    for dr, dc in DIRECTIONS:
        new_row, new_col = zero_row + dr, zero_col + dc
        if is_valid_move(new_row, new_col):
            new_state = [list(row) for row in state]
            new_state[zero_row][zero_col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[zero_row][zero_col]
            neighbors.append(tuple(tuple(row) for row in new_state))

    return neighbors

def dfs(initial_state, path=None, visited=None):
    if path is None:
        path = []
    if visited is None:
        visited = set()

    visited.add(initial_state)
    path.append(initial_state)

    if initial_state == goal_state:
        return path

    for neighbor in get_neighbors(initial_state):
        if neighbor not in visited:
            result = dfs(neighbor, path.copy(), visited)
            if result:
                return result

    return None

def print_state(state):
    for row in state:
        print(' '.join(str(x) if x != 0 else ' ' for x in row))
    print()

if __name__ == "__main__":
    initial_state = ((5, 1, 2), (8, 0, 3), (7, 4, 6))
    print("Initial State:")
    print_state(initial_state)

    solution = dfs(initial_state)

    if solution:
        print("Solution Path:")
        for state in solution:
            print_state(state)
    else:
        print("No solution found")

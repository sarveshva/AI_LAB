def calculate_heuristic(state, goal):
    h = 0
    for i in range(len(state)):
        if state[i] != goal[i] and state[i] != 0:
            h += 1
    return h

def operate(state, move):
    blank_pos = state.index(0)
    new_state = state[:]
    if move == 'LEFT' and blank_pos % 3 > 0:
        new_state[blank_pos], new_state[blank_pos - 1] = new_state[blank_pos - 1], new_state[blank_pos]
    elif move == 'RIGHT' and blank_pos % 3 < 2:
        new_state[blank_pos], new_state[blank_pos + 1] = new_state[blank_pos + 1], new_state[blank_pos]
    elif move == 'UP' and blank_pos > 2:
        new_state[blank_pos], new_state[blank_pos - 3] = new_state[blank_pos - 3], new_state[blank_pos]
    elif move == 'DOWN' and blank_pos < 6:
        new_state[blank_pos], new_state[blank_pos + 3] = new_state[blank_pos + 3], new_state[blank_pos]
    h = calculate_heuristic(new_state, goal)
    return new_state, h

def print_state(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()

def hill_climbing(initial_state, goal):
    state = initial_state
    h = calculate_heuristic(state, goal)
    print("Initial state:")
    print_state(state)
    print(f"Heuristic (h): {h}")
    
    while h != 0:
        moves = ['LEFT', 'RIGHT', 'UP', 'DOWN']
        next_state = None
        min_h = float('inf')
        chosen_move = None

        for move in moves:
            new_state, new_h = operate(state, move)
            if new_h < min_h:
                min_h = new_h
                next_state = new_state
                chosen_move = move

        print(f"Chosen move: {chosen_move}")
        print(f"New state after {chosen_move}:")
        print_state(next_state)
        print(f"Heuristic (h): {min_h}")

        if next_state == state:
            return [-1, -1, -1, -1, -1, -1, -1, -1]
        
        state = next_state
        h = min_h

    return state

initial_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
solved_state = hill_climbing(initial_state, goal)
print("Solved state:")
print_state(solved_state)

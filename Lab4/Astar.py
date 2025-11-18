def calculate_heuristic(state, goal):
    sum = 0
    for i in range(len(state)):
        if state[i] != goal[i] and state[i] != 0:
            sum += 1
    return sum

def operate(state, move, goal):
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
    else:
        return state, calculate_heuristic(state, goal)

    h = calculate_heuristic(new_state, goal)
    return new_state, h

def print_state(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()

def a_star(initial_state, goal):
    open_set = [(initial_state, 0, calculate_heuristic(initial_state, goal), [])] 
    closed_set = set()

    while open_set:
        current_index = 0
        current_f = open_set[0][1] + open_set[0][2]
        for i in range(1, len(open_set)):
            f = open_set[i][1] + open_set[i][2]
            if f < current_f:
                current_f = f
                current_index = i

        current_state, g, h, path = open_set.pop(current_index)
        state_tuple = tuple(current_state)

        if state_tuple in closed_set:
            continue
        closed_set.add(state_tuple)

        if current_state == goal:
            for move in path:
                print(f"Move: {move}")
                print_state(current_state)
                current_state, _ = operate(current_state, move, goal)
            print("Goal reached!")
            return current_state

        moves = ['LEFT', 'RIGHT', 'UP', 'DOWN']
        for move in moves:
            new_state, new_h = operate(current_state, move, goal)
            new_state_tuple = tuple(new_state)
            if new_state_tuple not in closed_set:
                open_set.append((new_state, g + 1, new_h, path + [move]))

    return [-1, -1, -1, -1, -1, -1, -1, -1, -1]

initial_state = [1, 2, 3, 4, 5, 6, 0, 7, 8]
goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]

print("Initial state:")
print_state(initial_state)

solved_state = a_star(initial_state, goal)

print("Final state:")
print_state(solved_state)

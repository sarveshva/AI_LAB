import random

def heuristic(state):
    attacks = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                attacks += 1
    return attacks

def generate_neighbors(state):
    neighbors = []
    n = len(state)
    for col in range(n):
        for row in range(n):
            if row != state[col]:
                new_state = state[:]
                new_state[col] = row
                neighbors.append(new_state)
    return neighbors

def hill_climbing(n):
    state = [random.randint(0, n - 1) for _ in range(n)]
    while True:
        current_h = heuristic(state)
        if current_h == 0:
            return state, current_h

        neighbors = generate_neighbors(state)
        next_state = min(neighbors, key=heuristic)
        next_h = heuristic(next_state)

        if next_h >= current_h:
            return state, current_h

        state = next_state

def random_restart_hill_climbing(n, max_restarts=1000):
    best_state = None
    best_h = float('inf')

    for _ in range(max_restarts):
        state, h = hill_climbing(n)
        if h == 0:
            return state, h  # found perfect solution
        if h < best_h:
            best_h = h
            best_state = state

    return best_state, best_h  # return best found solution

# --- Example ---
n = 8
solution, h_val = random_restart_hill_climbing(n)
print("State:", solution)
print("Heuristic (attacking pairs):", h_val)
H

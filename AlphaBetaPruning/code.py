import math

# ---------------------------------------------------------
# Alpha-Beta Search
# ---------------------------------------------------------

def alpha_beta_search(state):
    return max_value(state, -math.inf, math.inf)


def max_value(state, alpha, beta):
    if terminal(state):
        return utility(state)

    v = -math.inf

    for s in successors(state):
        v = max(v, min_value(s, alpha, beta))

        if v >= beta:
            return v          # beta cutoff

        alpha = max(alpha, v)

    return v


def min_value(state, alpha, beta):
    if terminal(state):
        return utility(state)

    v = math.inf

    for s in successors(state):
        v = min(v, max_value(s, alpha, beta))

        if v <= alpha:
            return v          # alpha cutoff

        beta = min(beta, v)

    return v


# ---------------------------------------------------------
# Demo Game Tree (Simple Example)
# ---------------------------------------------------------

# You can replace these with your actual game functions

game_tree = {
    "A": ["B", "C"],          # root
    "B": ["D", "E"],
    "C": ["F", "G"],
    "D": [], "E": [], "F": [], "G": []
}

utilities = {
    "D": 3,
    "E": 12,
    "F": 8,
    "G": 2
}


def successors(state):
    return game_tree[state]


def terminal(state):
    return len(game_tree[state]) == 0


def utility(state):
    return utilities[state]


# ---------------------------------------------------------
# Run Alpha-Beta
# ---------------------------------------------------------

result = alpha_beta_search("A")
print("Best achievable score:", result)

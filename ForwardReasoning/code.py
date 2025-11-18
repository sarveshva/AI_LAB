from copy import deepcopy

# --------------------------------------------------------
# Helper functions
# --------------------------------------------------------

def is_variable(x):
    return isinstance(x, str) and x[0].islower()

def unify(x, y, subst=None):
    """UNIFY algorithm (simple version)"""
    if subst is None:
        subst = {}
    if subst == "fail":
        return "fail"
    if x == y:
        return subst
    if is_variable(x):
        return unify_var(x, y, subst)
    if is_variable(y):
        return unify_var(y, x, subst)
    if isinstance(x, tuple) and isinstance(y, tuple) and len(x) == len(y):
        for a, b in zip(x, y):
            subst = unify(a, b, subst)
            if subst == "fail":
                return "fail"
        return subst
    return "fail"

def unify_var(var, x, subst):
    if var in subst:
        return unify(subst[var], x, subst)
    elif x in subst:
        return unify(var, subst[x], subst)
    else:
        subst2 = deepcopy(subst)
        subst2[var] = x
        return subst2

def substitute(expr, subst):
    """Apply substitution θ to an expression"""
    if isinstance(expr, tuple):
        return tuple(substitute(e, subst) for e in expr)
    if is_variable(expr) and expr in subst:
        return subst[expr]
    return expr

def standardize_variables(rule, counter):
    """Rename rule variables to avoid conflicts"""
    mapping = {}
    p_list, q = rule
    new_p = []
    for p in p_list:
        new_tuple = []
        for item in p:
            if is_variable(item):
                if item not in mapping:
                    mapping[item] = item + str(counter)
                new_tuple.append(mapping[item])
            else:
                new_tuple.append(item)
        new_p.append(tuple(new_tuple))

    new_q = []
    for item in q:
        if is_variable(item):
            if item not in mapping:
                mapping[item] = item + str(counter)
            new_q.append(mapping[item])
        else:
            new_q.append(item)

    return new_p, tuple(new_q)


# --------------------------------------------------------
# FOL-FC-ASK(KB, query) 
# --------------------------------------------------------

def fol_fc_ask(KB, query):
    new_facts = set()
    counter = 1  # variable renaming counter

    while True:
        new_facts = set()

        for rule in KB["rules"]:
            premises, conclusion = standardize_variables(rule, counter)
            counter += 1

            # try to find θ such that all premises unify with facts
            for fact_set in match_premises(KB["facts"], premises):
                θ = fact_set
                q_prime = substitute(conclusion, θ)

                if q_prime not in KB["facts"] and q_prime not in new_facts:
                    # Check if this new fact solves the query
                    φ = unify(q_prime, query)
                    if φ != "fail":
                        return φ  # Found answer!

                    new_facts.add(q_prime)

        if not new_facts:
            return False

        KB["facts"].update(new_facts)

# --------------------------------------------------------
# Helper to unify all premises
# --------------------------------------------------------

def match_premises(facts, premises):
    """Returns all substitutions θ that satisfy p1θ ... pnθ"""
    if not premises:
        return [ {} ]

    first, rest = premises[0], premises[1:]
    matches = []

    for fact in facts:
        θ = unify(first, fact)
        if θ != "fail":
            for next_subst in match_premises(
                {substitute(f, θ) for f in facts}, 
                [substitute(p, θ) for p in rest]
            ):
                combined = { **θ, **next_subst }
                matches.append(combined)

    return matches


# --------------------------------------------------------
# Example Usage
# --------------------------------------------------------

KB = {
    "facts": {
        ("Parent", "John", "Mary"),
        ("Parent", "Mary", "Alice"),
    },
    "rules": [
        ( [("Parent","x","y"), ("Parent","y","z")], ("Grandparent", "x", "z") )
    ]
}

query = ("Grandparent", "John", "z")

result = fol_fc_ask(KB, query)
print("ANSWER:", result)

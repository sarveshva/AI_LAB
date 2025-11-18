from copy import deepcopy

# ------------------------------------------
# Basic helper functions
# ------------------------------------------

def is_variable(x):
    return isinstance(x, str) and x[0].islower()

def substitute(expr, subst):
    if isinstance(expr, tuple):
        return tuple(substitute(e, subst) for e in expr)
    if expr in subst:
        return subst[expr]
    return expr

def unify(x, y, subst=None):
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
    elif is_variable(x) and x in subst:
        return unify(var, subst[x], subst)
    else:
        subst2 = deepcopy(subst)
        subst2[var] = x
        return subst2

# ------------------------------------------
# Check if two literals are complementary  
# L and NOT(M)
# literal = ('Pred', args...) or ('NOT', ('Pred', args...))
# ------------------------------------------

def negate(lit):
    if lit[0] == "NOT":
        return lit[1]
    return ("NOT", lit)

def complementary(l1, l2):
    return unify(l1, negate(l2))  # returns substitution or fail


# ------------------------------------------
# Resolution algorithm
# ------------------------------------------

def resolve_pair(Ci, Cj):
    """Return all resolvents of clause pair Ci, Cj"""
    resolvents = []

    for L in Ci:
        for M in Cj:

            θ = complementary(L, M)
            if θ != "fail":
                # Remove resolved literals
                Ci_part = [substitute(x, θ) for x in Ci if x != L]
                Cj_part = [substitute(x, θ) for x in Cj if x != M]

                # Combine
                new_clause = Ci_part + Cj_part

                # Remove duplicates
                new_clause = list(set(new_clause))

                resolvents.append(new_clause)

    return resolvents


# ------------------------------------------
# Main resolution loop
# ------------------------------------------

def resolution(KB, query):
    # Negate query and add to KB
    neg_query = [negate(query)]
    clauses = KB + [neg_query]

    new = []

    while True:
        new = []

        # Try all pairs
        for i in range(len(clauses)):
            for j in range(i+1, len(clauses)):
                Ci = clauses[i]
                Cj = clauses[j]

                resolvents = resolve_pair(Ci, Cj)

                for r in resolvents:
                    if r == []:       # empty clause -> success
                        return True
                    new.append(r)

        # No progress
        if all(c in clauses for c in new):
            return False

        # Add new clauses
        for c in new:
            if c not in clauses:
                clauses.append(c)


# ------------------------------------------
# Example
# (P ∨ Q), (¬Q ∨ R), (¬R)
# Query: P ?
# ------------------------------------------

KB = [
    [("P",), ("Q",)],
    [("NOT", ("Q",)), ("R",)],
    [("NOT", ("R",))]
]

query = ("P",)

print("Entails?", resolution(KB, query))

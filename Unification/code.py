def occurs_check(var, expr, subst):
    """
    Check if variable 'var' occurs anywhere inside 'expr' (with substitutions applied).
    Prevents infinite loops in substitution.
    """
    if var == expr:
        return True
    elif isinstance(expr, tuple):
        return any(occurs_check(var, e, subst) for e in expr)
    elif isinstance(expr, str) and expr in subst:
        return occurs_check(var, subst[expr], subst)
    else:
        return False


def unify(x, y, subst=None):
    """
    Unify expressions x and y with current substitution subst.
    Returns a substitution dict or None if unification fails.
    """
    if subst is None:
        subst = {}

    # Apply current substitutions
    if isinstance(x, str) and x in subst:
        x = subst[x]
    if isinstance(y, str) and y in subst:
        y = subst[y]

    # Step 1a: If x and y are identical
    if x == y:
        return subst

    # Step 1b: If x is a variable
    if isinstance(x, str) and x.islower():  # assuming variables are lowercase strings
        if occurs_check(x, y, subst):
            return None  # Failure due to occurs check
        else:
            subst[x] = y
            return subst

    # Step 1c: If y is a variable
    if isinstance(y, str) and y.islower():
        if occurs_check(y, x, subst):
            return None  # Failure due to occurs check
        else:
            subst[y] = x
            return subst

    # Step 2: If both are compound expressions (tuples), check predicate and arity
    if isinstance(x, tuple) and isinstance(y, tuple):
        if x[0] != y[0]:  # predicate symbols differ
            return None
        if len(x) != len(y):  # different number of arguments
            return None
        # Step 4 & 5: unify each element in order
        for xi, yi in zip(x[1:], y[1:]):
            subst = unify(xi, yi, subst)
            if subst is None:
                return None
        return subst

    # Step 1d: all other cases failure
    return None


# Example usage:

# Constants and variables:
# Variables are lowercase strings, constants uppercase strings.
# Predicates as tuples: ('Predicate', arg1, arg2, ...)

x1 = ('P', 'x', 'F')    # P(x, F)
x2 = ('P', 'a', 'y')    # P(a, y)

result = unify(x1, x2)

print("Substitution:", result)

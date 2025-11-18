# Evaluate a sentence under a given model
def model_satisfies(sentence, model):
    # sentence is a lambda function using symbols in model
    return sentence(model)

# Truth-table enumeration algorithm
def tt_check_all(KB, alpha, symbols, model):
    if not symbols:  # Base case: all symbols assigned
        if model_satisfies(KB, model):
            return model_satisfies(alpha, model)
        else:
            return True  # ignore models where KB is false
    else:
        P = symbols[0]
        rest = symbols[1:]
        
        # Assign True to P
        model_true = model.copy()
        model_true[P] = True
        # Assign False to P
        model_false = model.copy()
        model_false[P] = False
        
        # Recursively check both branches
        return (tt_check_all(KB, alpha, rest, model_true) and
                tt_check_all(KB, alpha, rest, model_false))

# Main function
def tt_entails(KB, alpha, symbols):
    return tt_check_all(KB, alpha, symbols, {})

# -------------------------------
# Example usage:
# Symbols: P, Q
# KB: P AND Q
# Alpha: P

symbols = ['P', 'Q']

# Represent sentences as functions taking a model dict
KB = lambda m: m['P'] and m['Q']
alpha = lambda m: m['P']

result = tt_entails(KB, alpha, symbols)
print("KB entails alpha?" , result)

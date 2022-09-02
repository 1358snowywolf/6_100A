# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    
    key = (egg_weights, target_weight)
    key = str(key)
    
    if key in memo:
        return memo[key]
    
    if(target_weight < 0):
        return 1000000000
    
    if(target_weight == 0):
        return 0
    
    list_egg_weight = list(egg_weights)
    trueAnswer = 1000000000 #sys.maxsize
    
    for i in range(len(list_egg_weight)):
        answer1 = dp_make_weight(list_egg_weight, target_weight - list_egg_weight[i], memo)
        answer2 = dp_make_weight(tuple(list_egg_weight[:i] + list_egg_weight[i + 1:]), target_weight - list_egg_weight[i], memo)
        trueAnswer = min(trueAnswer, min(answer1, answer2))
    
    memo[key] = trueAnswer + 1
    return memo[key]

# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    # egg_weights = (1, 2, 5)
    n = 99
    # n = 10
    print("Egg weights =", egg_weights)
    print("n =", n)
    # print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()
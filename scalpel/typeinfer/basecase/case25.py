def fibonacci(num):
    """
    Use fibonacci as test case for int variable names
    """
    count = 0
    if num < 0:
        return None
    elif num == 0:
        return 0
    elif num == 1 or num == 2:
        return 1
    else:
        return fibonacci(num - 1) + fibonacci(num - 2)

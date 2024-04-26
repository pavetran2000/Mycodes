import timeit

def bruteforce_solution(input, input_size, target):
    """
    Given a list of numbers sorted in increasing order and a target number, find the target number in the list.
    If the target number is found in the list, return True. Otherwise, return False.
    """
    for i in range(input_size):
        if input[i] == target:
            print("Target found at index:", i)
            return
            
    print("Target not found")
    return

def optimal_solution(input, input_size, target):
    """
    Given a list of numbers sorted in increasing order and a target number, find the target number in the list.
    If the target number is found in the list, return True. Otherwise, return False.
    """
    low = 0
    high = len(input) - 1

    while low <= high:
        mid = (low + high) // 2
        if input[mid] == target:
            return True
        elif input[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return False

input_size = 1000000000
target = 999999999
input = [i for i in range(0, input_size + 1)]

print("Array size:", input_size)
print("Target:", target)

print("bruteforce_solution")
print("Execution Time:", timeit.timeit(lambda: bruteforce_solution(input, input_size, target), number=1))

print("optimal_solution")
print("Execution Time:", timeit.timeit(lambda: optimal_solution(input, input_size, target), number=1))

print("-" * 30)

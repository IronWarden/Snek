import random

if __name__ == "__main__":
    nums = []
    for i in range(1, 100):
        nums.append(i)
    low = 0
    high = len(nums) - 1
    guess = random.randint(1, 100)
    print(guess)
    iterations = 0
    while low <= high:
        iterations += 1
        mid = (high - low) // 2 + low
        if nums[mid] == guess:
            print(iterations)
            break
        elif nums[mid] > guess:
            high = mid + 1
        else:
            low = mid - 1

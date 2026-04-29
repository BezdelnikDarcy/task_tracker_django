from functools import lru_cache


@lru_cache
def get_sum(numbers):
    if numbers:
        return numbers[0]+get_sum(numbers[1:])
    return 0


nums = (1, 2, 3)
print(get_sum(nums))
print("work cache")
print(get_sum(nums))
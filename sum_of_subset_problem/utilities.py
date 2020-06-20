import random
from typing import Dict, List


def generate_problem_with_solution(length_of_set: int, length_of_subset: int) -> Dict[Dict, List]:
    if length_of_subset > length_of_set:
        raise ValueError("Length of subset cannot be bigger than length of set")

    if length_of_set <= 0:
        raise ValueError("Length of set must be positive number")

    if length_of_subset <= 0:
        raise ValueError("Length of subset must be positive number")

    set_of_numbers = [number for number in range(1, length_of_set)]
    subset_of_numbers = random.sample(set_of_numbers, length_of_subset)
    number = sum(subset_of_numbers)

    problem_dict = {"set": set_of_numbers, "number": number}

    return {"problem": problem_dict, "solution": subset_of_numbers}

import sys
import os

import pytest

from problem_sumy_podzbioru.problem import BruteforceSumOfSubsetProblem
from problem_sumy_podzbioru.utilities import generate_problem_with_solution

# probably less than second
SHORT_PROBLEM_LENGTHS = [(10, 1), (100, 1), (1000, 1), (10, 2), (100, 2)]

# up to a minute
MEDIUM_PROBLEM_LENGTHS = [(1000, 2), (100, 3)]


@pytest.mark.parametrize("length_of_set, length_of_subset", SHORT_PROBLEM_LENGTHS)
def test_bruteforce_with_short_problems(length_of_set, length_of_subset):
    problem_with_solution = generate_problem_with_solution(
        length_of_set, length_of_subset
    )
    problem = BruteforceSumOfSubsetProblem(problem_with_solution["problem"])
    solution = problem.solve()

    assert solution


@pytest.mark.parametrize("length_of_set, length_of_subset", MEDIUM_PROBLEM_LENGTHS)
def test_bruteforce_with_medium_problems(length_of_set, length_of_subset):
    problem_with_solution = generate_problem_with_solution(
        length_of_set, length_of_subset
    )
    problem = BruteforceSumOfSubsetProblem(problem_with_solution["problem"])
    solution = problem.solve()

    assert solution

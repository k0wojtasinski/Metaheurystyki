import sys
import os

import pytest

from sum_of_subset_problem.problem import (
    SumOfSubsetSolution,
    SumOfSubsetProblem,
    BruteforceSumOfSubsetSolver,
)
from sum_of_subset_problem.utilities import generate_problem_with_solution

# probably less than second
SHORT_PROBLEM_LENGTHS = [(10, 1), (100, 1), (1000, 1), (10, 2), (100, 2)]

# up to a minute
MEDIUM_PROBLEM_LENGTHS = [(1000, 2), (100, 3)]


@pytest.mark.parametrize("length_of_set, length_of_subset", SHORT_PROBLEM_LENGTHS)
def test_bruteforce_with_short_problems(length_of_set, length_of_subset):
    problem_with_solution = generate_problem_with_solution(
        length_of_set, length_of_subset
    )
    problem = SumOfSubsetProblem(problem_with_solution["problem"])
    solver = BruteforceSumOfSubsetSolver(problem)
    solution = solver.solve(verbose=True)

    assert solution.goal() == 0


@pytest.mark.parametrize("length_of_set, length_of_subset", MEDIUM_PROBLEM_LENGTHS)
def test_bruteforce_with_medium_problems(length_of_set, length_of_subset):
    problem_with_solution = generate_problem_with_solution(
        length_of_set, length_of_subset
    )
    problem = SumOfSubsetProblem(problem_with_solution["problem"])
    solver = BruteforceSumOfSubsetSolver(problem)
    solution = solver.solve(verbose=True)

    assert solution.goal() == 0


@pytest.mark.parametrize("length_of_set, length_of_subset", SHORT_PROBLEM_LENGTHS)
def test_problem_should_generate_random_solution(length_of_set, length_of_subset):
    problem_with_solution = generate_problem_with_solution(
        length_of_set, length_of_subset
    )
    problem = SumOfSubsetProblem(problem_with_solution["problem"])
    random_solution = problem.generate_random_solution()

    assert isinstance(random_solution, SumOfSubsetSolution)
    assert len(random_solution["subset"]) > 0

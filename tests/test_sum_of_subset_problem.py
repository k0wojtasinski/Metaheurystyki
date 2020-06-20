import pytest

from sum_of_subset_problem.problem import (
    SumOfSubsetSolution,
    SumOfSubsetProblem,
    BruteforceSumOfSubsetSolver,
)
from sum_of_subset_problem.utilities import generate_problem_with_solution

SHORT_PROBLEM_LENGTHS = [(10, 1), (100, 1), (1000, 1), (10, 2), (100, 2)]


@pytest.mark.parametrize("length_of_set, length_of_subset", SHORT_PROBLEM_LENGTHS)
def test_problem_can_generate_random_solution(length_of_set, length_of_subset):
    problem_with_solution = generate_problem_with_solution(length_of_set, length_of_subset)
    problem = SumOfSubsetProblem(problem_with_solution["problem"])
    random_solution = problem.generate_random_solution()

    assert isinstance(random_solution, SumOfSubsetSolution)
    assert len(random_solution["subset"]) > 0
    assert random_solution.goal() >= 0


@pytest.mark.parametrize("length_of_set, length_of_subset", SHORT_PROBLEM_LENGTHS)
def test_problem_can_find_close_neighbour(length_of_set, length_of_subset):
    problem_with_solution = generate_problem_with_solution(length_of_set, length_of_subset)
    problem = SumOfSubsetProblem(problem_with_solution["problem"])
    random_solution = problem.generate_random_solution()
    close_neighbour = problem.find_close_neighbor(random_solution)

    assert isinstance(close_neighbour, SumOfSubsetSolution)
    assert len(close_neighbour["subset"]) > 0
    assert close_neighbour.goal() >= 0


def test_solutions_can_be_compared():
    problem = SumOfSubsetProblem({"set": [x for x in range(10)], "number": 15})
    correct_solution = SumOfSubsetSolution({"subset": [6, 9]}, problem)
    wrong_solution = SumOfSubsetSolution({"subset": [0, 2]}, problem)
    wrong_but_slightly_better_solution = SumOfSubsetSolution({"subset": [5, 2]}, problem)

    wrong_and_incorrect_solution = SumOfSubsetSolution({"subset": [20]}, problem)

    assert (
        correct_solution
        > wrong_but_slightly_better_solution
        > wrong_solution
        > wrong_and_incorrect_solution
    )

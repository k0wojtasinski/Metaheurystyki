import itertools
import random
import time
import math
from typing import List, Optional, Union

from sum_of_subset_problem import logger
from sum_of_subset_problem.base import Problem, Solution, Solver, Experiment


class SumOfSubsetSolution(Solution):
    def __init__(self, data, problem):
        super().__init__(data, problem)
        self.subset = data["subset"]
        self.set = problem.set
        self.number = problem.number

    def goal(self) -> int:
        """ returns goal function value for SumOfSubsetSolution """
        if self.check_correctness(self.set, self.subset, self.number):
            return abs(sum(self.subset) - self.number)

        return -1

    @staticmethod
    def check_correctness(set_of_numbers, subset, number) -> bool:
        """ check correctness of solution """
        return all([number in set_of_numbers for number in subset])


class BruteforceSumOfSubsetSolver(Solver):
    def solve(self, **kwargs):
        """ class to solve SumOfSubsetProblem using bruteforce """
        self.log_welcome()
        limit = kwargs.get("limit")
        verbose = kwargs.get("verbose", False)

        if limit:
            logger.info(f"Set limit to {limit}")

        logger.info(f"Set verbose to {verbose} (default=False)")

        start_time = time.time()

        for i in range(1, len(self.problem.set) + 1):

            # trying all the combinations from set, of size i
            for combination in itertools.combinations(self.problem.set, i):
                self.add_attempt()
                solution = SumOfSubsetSolution(
                    {"subset": combination,}, problem=self.problem
                )

                if verbose:
                    logger.info(solution)

                if solution.is_correct():
                    self.set_time(start_time)
                    self.log_solution(solution)
                    self.solutions.append(solution)
                    return solution

                if limit and self.report["attempts"] == limit:
                    self.set_time(start_time)
                    logger.warning(f"Runned out of tries (limit={limit})")
                    self.log_solution(solution)
                    return solution

        self.set_time(start_time)

        logger.warning(
            f"Solution cannot be found (time={self.report['time']}, attempts={self.report['attempts']})"
        )

        return None


class ClimbingSumOfSubsetSolver(Solver):
    DEFAULT_LIMIT = 1000000

    def solve(self, **kwargs):
        """ class to solve SumOfSubsetProblem using bruteforce """
        self.log_welcome()

        limit = kwargs.get("limit", self.DEFAULT_LIMIT)
        verbose = kwargs.get("verbose", False)
        size = kwargs.get("size", random.randint(1, len(self.problem.set) // 2))

        logger.info(f"Set limit to {limit} (default={self.DEFAULT_LIMIT})")
        logger.info(f"Set verbose to {verbose} (default=False)")
        logger.info(f"Set size to {size}")

        start_time = time.time()
        random_solution = self.problem.generate_random_solution(size)

        self.add_attempt()

        if random_solution.is_correct():
            self.set_time(start_time)
            self.log_solution(random_solution)
            return random_solution

        for _ in range(limit):
            self.add_attempt()
            close_neighbor = self.problem.find_close_neighbor(random_solution)

            logger.info(close_neighbor)

            if close_neighbor.is_correct():
                self.set_time(start_time)
                self.log_solution(close_neighbor)
                return close_neighbor

            if close_neighbor > random_solution:
                random_solution = close_neighbor

        self.set_time(start_time)

        self.log_solution(random_solution)
        return random_solution


class SimulatedAnnealingSumOfSubsetSolver(Solver):
    DEFAULT_LIMIT = 1000000

    def solve(self, **kwargs):
        self.log_welcome()

        limit = kwargs.get("limit", self.DEFAULT_LIMIT)
        verbose = kwargs.get("verbose", False)
        temperature = kwargs.get("temperature", lambda i: 1 / i)
        size = kwargs.get("size", random.randint(1, len(self.problem.set) // 2))

        logger.info(f"Set limit to {limit} (default={self.DEFAULT_LIMIT})")
        logger.info(f"Set verbose to {verbose} (default=False)")
        logger.info(f"Set size to {size}")

        start_time = time.time()
        random_solution = self.problem.generate_random_solution(size)

        self.add_attempt()

        if random_solution.is_correct():
            self.set_time(start_time)
            return random_solution

        for _ in range(1, limit):
            self.add_attempt()
            close_neighbor = self.problem.find_close_neighbor(random_solution)

            if close_neighbor.is_correct():
                self.set_time(start_time)
                self.log_solution(close_neighbor)
                return close_neighbor

            if close_neighbor > random_solution:
                random_solution = close_neighbor
            else:
                i = self.report.get("attempts")
                random_number = random.random()
                sa_condition = math.exp(
                    -(
                        abs(close_neighbor.goal() - random_solution.goal())
                        / temperature(i)
                    )
                )

                if random_number < sa_condition:
                    random_solution = close_neighbor

        self.log_solution(random_solution)
        return random_solution


class SumOfSubsetProblem(Problem):
    solvers = {
        "bruteforce": BruteforceSumOfSubsetSolver,
        "climbing": ClimbingSumOfSubsetSolver,
        "sa": SimulatedAnnealingSumOfSubsetSolver,
    }

    def __init__(self, data):
        super().__init__(data)
        self.set = self.data["set"]
        self.number = self.data["number"]

    def generate_random_solution(self, size_of_subset=None) -> SumOfSubsetSolution:
        if not size_of_subset or size_of_subset > len(self.set) or size_of_subset < 0:
            size_of_subset = random.randint(1, len(self.set))

            logger.warning(
                f'"size_of_subset" is not provided or it is not correct, set to {size_of_subset}'
            )

        return SumOfSubsetSolution(
            data={"subset": random.sample(self.set, size_of_subset)}, problem=self
        )

    def find_close_neighbor(self, solution: SumOfSubsetSolution):
        copy_of_data = solution.data.copy()

        first_element, second_element = random.choices(self.set, k=2)

        if first_element in solution.subset:
            copy_of_data.get("subset").remove(first_element)
        else:
            copy_of_data.get("subset").append(first_element)

        if second_element in solution.subset:
            if random.randint(1, 2) == 1:
                copy_of_data.get("subset").remove(second_element)
        else:
            if random.randint(1, 2) == 1:
                copy_of_data.get("subset").append(second_element)

        return SumOfSubsetSolution(copy_of_data, self)

class SumOfSubsetExperiment(Experiment):
    def __init__(self, data=None):
        super().__init__(data)
        self.problem_class = SumOfSubsetProblem

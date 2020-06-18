import abc
from collections import UserDict
import itertools
import json
import logging
import random
import time
import math
from typing import List, Optional, Union

FORMAT = "%(levelname)s | %(asctime)s | %(funcName)s | %(msg)s"

logging.basicConfig(format=FORMAT)
logger = logging.getLogger("Problem")
logger.setLevel("INFO")


class Solution(abc.ABC, UserDict):
    """ abstract class representing single solution
        provides comparison, is_correct and __str__
        goal method needs to be implemented
    """

    def __init__(self, data: dict, problem: "Problem"):
        self.data = data

    def __eq__(self, solution: "Solution"):
        if isinstance(solution, self.__class__):
            return self.data == solution.data

    def __lt__(self, solution: "Solution"):
        if self.goal() < 0 and solution.goal() < 0:
            return False

        if self.goal() < 0:
            return True

        if solution.goal() < 0:
            return False

        return self.goal() > solution.goal()

    def __gt__(self, solution: "Solution"):
        if self.goal() < 0 and solution.goal() < 0:
            return False

        if self.goal() < 0:
            return False

        if solution.goal() < 0:
            return True

        return self.goal() < solution.goal()

    @abc.abstractmethod
    def goal(self) -> int:
        ...

    def is_correct(self) -> bool:
        return self.goal() == 0

    def __str__(self):
        return f"{self.__class__.__name__} (data={self.data}, goal={self.goal()}, is_correct={self.is_correct()})"

    def __repr__(self):
        return str(self)


class Problem(abc.ABC, UserDict):
    def __init__(self, data: dict):
        self.data = data

    @abc.abstractmethod
    def generate_random_solution(self) -> Solution:
        ...

    @abc.abstractmethod
    def find_close_neighbor(self, solution: Solution) -> Solution:
        ...

    @classmethod
    def from_json(cls, file_path: str) -> Union["Problem", List["Problem"]]:
        """ method to import problem data from JSON file
            each problem is defined in a single dict
            it returns Problem or list of Problems based on input data
        """
        with open(file_path) as input_file:
            data = json.load(input_file)
            if isinstance(data, dict):
                return cls(data)
            elif isinstance(data, list):
                return [cls(item) for item in data]
            else:
                raise TypeError("Expected list or dict")

    def export_to_json(self, file_path: str):
        with open(file_path, "w") as output_file:
            output_file.write(json.dumps(self.data))

    def __str__(self):
        return f"{self.__class__.__name__} (data={self.data})"

    def __repr__(self):
        return str(self)


class Solver(abc.ABC):
    def __init__(self, problem: Problem):
        self.name = self.__class__.__name__
        self.problem = problem
        self.report = {"attempts": 0, "time": 0}
        self.solutions = []

    @abc.abstractmethod
    def solve(self) -> Solution:
        ...

    def add_attempt(self):
        self.report["attempts"] += 1

    def set_time(self, start_time):
        self.report["time"] = time.time() - start_time

    def found_correct_solution(self, solution):
        logger.info(
            f"Found correct solution ({solution}) (time={self.report['time']}, attempts={self.report['attempts']})"
        )

    def did_not_find_correct_solution(self, solution):
        logger.info(
            f"Did not find correct solution ({solution}) (time={self.report['time']}, attempts={self.report['attempts']})"
        )

    def log_solution(self, solution):
        if solution.is_correct():
            self.found_correct_solution(solution)
        else:
            self.did_not_find_correct_solution(solution)

    def log_welcome(self):
        logger.info(f"Running {self.__class__.__name__}")
        logger.info(f"Trying to solve {self.problem}")

    @staticmethod
    def export_solutions_to_json(solutions: list, file_path):
        """ static method to save data of given solutions
            to JSON file
        """
        with open(file_path, "w") as output_file:
            output_file.write(json.dumps(solutions, indent="  "))

    def export_all_solutions_to_json(self, file_path):
        """ method to export all solutions to JSON file """
        solutions = [solution.data for solution in self.solutions]
        self.export_solutions_to_json(solutions, file_path)

    def export_correct_solutions_to_json(self, file_path):
        """ method to export all correct solutions to JSON file """
        solutions = [
            solution.data for solution in self.solutions if solution.is_correct()
        ]
        self.export_solutions_to_json(solutions, file_path)

    def export_incorrect_solutions_to_json(self, file_path):
        """ method to export all incorrect solutions to JSON file """
        solutions = [
            solution.data for solution in self.solutions if not solution.is_correct()
        ]
        self.export_solutions_to_json(solutions, file_path)


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
    def solve(self, verbose=False, **kwargs):
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

        logger.info(f"Set limit to {limit} (default={self.DEFAULT_LIMIT})")
        logger.info(f"Set verbose to {verbose} (default=False)")

        start_time = time.time()
        random_solution = self.problem.generate_random_solution()

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

    def solve(self, verbose=False, **kwargs):
        self.log_welcome()

        limit = kwargs.get("limit", self.DEFAULT_LIMIT)
        verbose = kwargs.get("verbose", False)
        temperature = kwargs.get("temperature", lambda i: 1 / i)

        logger.info(f"Set limit to {limit} (default={self.DEFAULT_LIMIT})")
        logger.info(f"Set verbose to {verbose} (default=False)")

        limit = kwargs.get("limit", self.DEFAULT_LIMIT)

        start_time = time.time()
        random_solution = self.problem.generate_random_solution()
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

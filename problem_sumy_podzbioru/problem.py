import abc

import json

import itertools
import logging

import time
from typing import List, Optional, Union

FORMAT = "%(asctime)s %(msg)s"

logging.basicConfig(format=FORMAT)
logger = logging.getLogger("Problem")
logger.setLevel("INFO")


class Solution(abc.ABC):
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
            return False

        if solution.goal() < 0:
            return True

        return self.goal() < solution.goal()

    def __gt__(self, solution: "Solution"):
        if self.goal() < 0 and solution.goal() < 0:
            return False

        if self.goal() < 0:
            return True

        if solution.goal() < 0:
            return False

        return self.goal() > solution.goal()

    @abc.abstractmethod
    def goal(self) -> int:
        ...

    def is_correct(self) -> bool:
        return self.goal() == 0

    def __str__(self):
        return f"{self.__class__.__name__} (data={self.data}, goal={self.goal()}, is_correct={self.is_correct()})"

    def __repr__(self):
        return str(self)


class Problem(abc.ABC):
    def __init__(self, data: dict):
        self.data = data

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
        self.problem = problem
        self.report = {"attempts": 0, "time": 0}
        self.solutions = []

    @abc.abstractmethod
    def solve(self) -> Solution:
        ...

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
    def solve(self, verbose=False):
        """ class to solve SumOfSubsetProblem using bruteforce """
        logger.info(f"Trying to solve {self.problem}")
        logger.info("Running brute-force")

        if verbose:
            logger.info("Activated verbose mode")

        start_time = time.time()

        for i in range(1, len(self.problem.set) + 1):

            # trying all the combinations from set, of size i
            for combination in itertools.combinations(self.problem.set, i):
                self.report["attempts"] += 1
                solution = SumOfSubsetSolution(
                    {"subset": combination,}, problem=self.problem
                )

                if verbose:
                    logger.info(solution)

                if solution.is_correct():
                    self.report["time"] = time.time() - start_time
                    logger.info(
                        f"Found solution ({solution}) (time={self.report['time']}, attempts={self.report['attempts']})"
                    )
                    self.solutions.append(solution)
                    return solution

        self.report["time"] = time.time() - start_time

        logger.warn(
            f"Solution cannot be found (time={self.report['time']}, attempts={self.report['attempts']})"
        )

        return None


class SumOfSubsetProblem(Problem):
    def __init__(self, data):
        super().__init__(data)
        self.set = self.data["set"]
        self.number = self.data["number"]

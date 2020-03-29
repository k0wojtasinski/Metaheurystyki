import abc

import json

import itertools
import logging

import time

FORMAT = "%(msg)s"

logging.basicConfig(format=FORMAT)
logger = logging.getLogger("Problem")
logger.setLevel("INFO")


class Solution(abc.ABC):
    """ abstract class representing single solution
        provides comparison, is_correct and __str__
        goal method needs to be implemented
    """
    def __init__(self, data: dict):
        self.data = data

    def __eq__(self, solution: "Solution"):
        if isinstance(solution, self):
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
        pass

    def is_correct(self) -> bool:
        return self.goal() == 0

    def __str__(self):
        return f"{self.__class__.__name__} (data={self.data}, goal={self.goal()}, is_correct={self.is_correct()})"

    def __repr__(self):
        return str(self)


class Problem:
    def __init__(self, data: dict):
        self.data = data
        self.solutions = []

    def clear_solution(self):
        self.solutions = []

    @classmethod
    def from_json(cls, file_path: str):
        """ method to import problems' data from JSON file
            each problem is defined in a single dict
            it returns list of Problems based on input data
        """
        with open(file_path) as input_file:
            content = json.load(input_file)
            results = []
            for item in content:
                results.append(cls(item))

        logger.info(
            f"Loading input from json file (file_name: {file_path}, content: {content})"
        )
        return results

    def __str__(self):
        return f"{self.__class__.__name__} (data={self.data})"

    def __repr__(self):
        return str(self)

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
    def __init__(self, data):
        super().__init__(data)
        self.set = data["set"]
        self.subset = data["subset"]
        self.number = data["number"]
        self.tries = self.data.get("tries", 0)
        self.time = self.data.get("time", 0)

    def goal(self) -> int:
        if self.check_correctness(self.set, self.subset, self.number):
            return abs(sum(self.subset) - self.number)

        return -1

    @staticmethod
    def check_correctness(set_of_numbers, subset, number) -> bool:
        return all([number in set_of_numbers for number in subset])


class SumOfSubsetProblem(Problem):
    def __init__(self, data):
        super().__init__(data)
        self.set = self.data["set"]
        self.number = self.data["number"]

    def bruteforce(self):
        logger.info("Running brute-force")
        start_time = time.time()

        for i in range(1, len(self.set) + 1):

            for combination in itertools.combinations(self.set, i):

                solution = SumOfSubsetSolution(
                    {
                        "number": self.number,
                        "subset": combination,
                        "set": self.set,
                        "tries": len(self.solutions),
                        "time": time.time() - start_time,
                    }
                )
                solution.data["tries"] = len(self.solutions)

                self.solutions.append(solution)

                if solution.is_correct():
                    logger.info(
                        f"Found solution (time={solution.time}, tries={solution.tries})"
                    )
                    return solution

        end_time = time.time() - start_time
        logger.warn(
            f"Solution cannot be found (time={end_time}, tries={len(self.solutions)})"
        )

        return []

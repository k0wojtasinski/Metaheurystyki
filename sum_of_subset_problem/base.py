""" module with all the base classes """
import abc
from collections import UserDict
import json
import time
from typing import List, Union
from types import FunctionType
import math # pylint: disable=unused-import

from sum_of_subset_problem import logger


class Solution(abc.ABC, UserDict):
    """ abstract class representing single solution
        provides comparison, is_optimal and __str__
        goal method needs to be implemented
    """

    def __init__(self, data: dict, problem: "Problem"):
        super().__init__(data)
        self.problem = problem

    def __eq__(self, solution: "Solution"):
        if isinstance(solution, self.__class__):
            return self.goal() == solution.goal()
        return False

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
        """ abstract method to evaluate quality of solution
            less is better
            0 means optimal
        """
        ...

    def is_optimal(self) -> bool:
        """ checks if found optimal solution """
        return self.goal() == 0

    def __str__(self):
        return f"{self.__class__.__name__} (data={self.data}, goal={self.goal()}, is_optimal={self.is_optimal()})"

    def __repr__(self):
        return str(self)

    def export_to_json(self, file_path: str):
        """ method to export solution to JSON file """
        with open(file_path, "w") as output_file:
            output_file.write(json.dumps(self.data))


class Problem(abc.ABC, UserDict):
    """ abstract class to encapsulate problem data
        and provide helper methods
    """

    def __init__(self, data: dict):
        super().__init__(data)

    @abc.abstractmethod
    def generate_random_solution(self, **kwargs) -> Solution:
        """ method to generate random solution of problem """
        ...

    @abc.abstractmethod
    def find_close_neighbor(self, solution: Solution) -> Solution:
        """ method to find random neighbor of solution """
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
            if isinstance(data, list):
                return [cls(item) for item in data]
            raise TypeError("Expected list or dict")

    def export_to_json(self, file_path: str):
        """ method to export problem to JSON file """
        with open(file_path, "w") as output_file:
            output_file.write(json.dumps(self.data))

    def __str__(self):
        return f"{self.__class__.__name__} (data={self.data})"

    def __repr__(self):
        return str(self)


class Solver(abc.ABC):
    """ abstract class to solve problem using given algorithm
        provides solve method and helper methods
    """

    def __init__(self, problem: Problem):
        self.name = self.__class__.__name__
        self.problem = problem
        self.report = {"attempts": 0, "time": 0}
        self.solutions = []

    @abc.abstractmethod
    def solve(self) -> Solution:
        """ method to get optimal solution of problem """
        ...

    def add_attempt(self):
        """ increment "attempts" counter of report """
        self.report["attempts"] += 1

    def set_time(self, start_time: float):
        """ update "time" of report """
        self.report["time"] = time.time() - start_time

    def log_solution(self, solution: Solution, start_time: float):
        """ update "time" and log solution """
        self.set_time(start_time)
        logger.info(
            f"Found solution ({solution}) (time={self.report['time']}, attempts={self.report['attempts']})"
        )

    def log_welcome(self):
        """ log welcome message """
        logger.info(f"Running {self.__class__.__name__}")
        logger.info(f"Trying to solve {self.problem}")


class Experiment(abc.ABC, UserDict):
    """ abstract class to solve several problems using different solvers and params """

    def __init__(self, data=None):
        self.name = self.__class__.__name__
        super().__init__(data)
        self.data["problems"] = self.data.get("problems", [])
        self.data["solvers"] = self.data.get("solvers", [])
        self.data["report"] = {}
        self.problems = []

    @property
    @abc.abstractmethod
    def problem_class(self) -> Problem:
        """ property with problem class to be used """
        ...

    def add_solver(self, solver_name: str, params=None) -> "Experiment":
        """ method to add solver by its name and params """
        self.data["solvers"].append({"solver_name": solver_name, "params": params})
        return self

    def add_problem(self, problem: Problem) -> "Experiment":
        """ method to add problem """
        self.data["problems"].append(problem.data)
        return self

    def _add_to_report(
            self, idx_of_problem: int, idx_of_solver: int, solver: Solver, solution: Solution,
    ):
        """ method to add report for given solver and problem """
        if idx_of_problem not in self.data["report"]:
            self.data["report"][idx_of_problem] = []
        self.data["report"][idx_of_problem].append(
            {
                "solver_id": idx_of_solver,
                "report": solver.report,
                "solution": solution.data,
                "goal": solution.goal(),
            }
        )

    def _prepare_problems(self):
        """ method to transform problems from json into class instances """
        self.problems = [
            self.problem_class(problem_data) for problem_data in self.data.get("problems")
        ]

    @staticmethod
    def _prepare_lambda_argument(argument):
        if isinstance(argument, FunctionType):
            return argument

        if "lambda" in argument:
            logger.warning(f"Evaluating {argument}. Potentially dangerous")
            return eval(argument)

        logger.warning(f"Cannot evaluate {argument}. Ignored")
        return None

    def export_to_json(self, file_path: str):
        """ method to export experiment to JSON file """
        with open(file_path, "w") as output_file:
            output_file.write(json.dumps(self.data))

    def _sort_report(self):
        """ method to sort report by solutions quality and taken time """
        for problem_idx in self.data.get("report").keys():
            self.data.get("report").get(problem_idx).sort(
                key=lambda report: (
                    report.get("report").get("goal"),
                    report.get("report").get("time"),
                )
            )

    def run(self):
        """ method to solve all the problems with solvers """
        self._prepare_problems()
        for idx_of_problem, problem in enumerate(self.problems):
            for idx_of_solver, solver_item in enumerate(self.data["solvers"]):
                solver = self.problem_class.solvers.get(solver_item.get("solver_name"))(problem)
                params = solver_item.get("params", {})

                logger.info(f"Working on {problem}")
                logger.info(f"Running {solver.__class__.__name__} with params ({params})")

                if params:
                    processed_params = params.copy()
                    for key in processed_params.keys():
                        if "lambda" in str(processed_params[key]):
                            processed_params[key] = self._prepare_lambda_argument(
                                processed_params[key]
                            )
                    solution = solver.solve(**processed_params)
                else:
                    solution = solver.solve()

                logger.info("Adding results to report")
                self._add_to_report(idx_of_problem, idx_of_solver, solver, solution)

        self._sort_report()
        logger.info(f"{self.__class__.__name__} result:\n{json.dumps(self.data, indent=4)}")

    @classmethod
    def from_json(cls, file_path: str) -> "Experiment":
        """ method to import Experiment from JSON file
            it returns Experiment
        """
        with open(file_path) as input_file:
            data = json.load(input_file)
            if isinstance(data, dict):
                return cls(data)
            raise TypeError("Expected dict")

    def __call__(self):
        self.run()

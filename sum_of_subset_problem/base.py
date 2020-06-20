import abc
from collections import UserDict
import json
import time
from typing import List, Optional, Union

from sum_of_subset_problem import logger


class Solution(abc.ABC, UserDict):
    """ abstract class representing single solution
        provides comparison, is_correct and __str__
        goal method needs to be implemented
    """

    def __init__(self, data: dict, problem: "Problem"):
        self.data = data

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
        ...

    def is_correct(self) -> bool:
        return self.goal() == 0

    def __str__(self):
        return f"{self.__class__.__name__} (data={self.data}, goal={self.goal()}, is_correct={self.is_correct()})"

    def __repr__(self):
        return str(self)

    def export_to_json(self, file_path: str):
        with open(file_path, "w") as output_file:
            output_file.write(json.dumps(self.data))


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

    def log_solution(self, solution, start_time):
        self.set_time(start_time)
        logger.info(
            f"Found solution ({solution}) (time={self.report['time']}, attempts={self.report['attempts']})"
        )

    def log_welcome(self):
        logger.info(f"Running {self.__class__.__name__}")
        logger.info(f"Trying to solve {self.problem}")


class Experiment(abc.ABC, UserDict):
    def __init__(self, data=None):
        self.name = self.__class__.__name__
        self.data = data or {}
        self.data["problems"] = self.data.get("problems", [])
        self.data["solvers"] = self.data.get("solvers", [])
        self.data["report"] = {}
        self.problems = []

    def add_solver(self, solver_name: str, params=None):
        self.data["solvers"].append({"solver_name": solver_name, "params": params})
        return self

    def add_problem(self, problem: Problem):
        self.data["problems"].append(problem.data)
        return self

    def _add_to_report(
        self,
        idx_of_problem: int,
        idx_of_solver: int,
        solver: Solver,
        solution: Solution,
    ):
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
        self.problems = [
            self.problem_class(problem_data)
            for problem_data in self.data.get("problems")
        ]

    def export_to_json(self, file_path: str):
        with open(file_path, "w") as output_file:
            output_file.write(json.dumps(self.data))

    def _sort_report(self):
        for problem_idx in self.data.get("report").keys():
            self.data.get("report")[problem_idx].sort(
                key=lambda report: (
                    report.get("report").get("goal"),
                    report.get("report").get("time"),
                )
            )

    def run(self):
        self._prepare_problems()
        for idx_of_problem, problem in enumerate(self.problems):
            for idx_of_solver, solver_item in enumerate(self.data["solvers"]):
                solver = self.problem_class.solvers.get(solver_item.get("solver_name"))(
                    problem
                )
                params = solver_item.get("params", {})

                logger.info(f"Working on {problem}")
                logger.info(
                    f"Running {solver.__class__.__name__} with params ({params})"
                )

                if params:
                    solution = solver.solve(**params)
                else:
                    solution = solver.solve()

                logger.info(f"Adding results to report")
                self._add_to_report(idx_of_problem, idx_of_solver, solver, solution)

        self._sort_report()
        logger.info(
            f"{self.__class__.__name__} result:\n{json.dumps(self.data, indent=4)}"
        )

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

""" module with SumOfSubset related classes """
import os
import itertools
import random
import time
import math

import jinja2
import matplotlib.pyplot as plt

from sum_of_subset_problem import logger
from sum_of_subset_problem.base import Problem, Solution, Solver, Experiment


class SumOfSubsetSolution(Solution):
    """ class implementing SumOfSubset solution """

    def __init__(self, data, problem):
        super().__init__(data, problem)
        self.subset = data["subset"]
        self.set = self.problem.set
        self.number = self.problem.number

    def goal(self) -> int:
        """ returns goal function value for SumOfSubsetSolution """
        if self.check_correctness(self.set, self.subset):
            return abs(sum(self.subset) - self.number)

        return -1

    @staticmethod
    def check_correctness(set_of_numbers, subset) -> bool:
        """ check correctness of solution """
        return all([number in set_of_numbers for number in subset])


class BruteforceSumOfSubsetSolver(Solver):
    """ class to solve SumOfSubsetProblem using bruteforce """

    def solve(self, **kwargs):
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

                solution = SumOfSubsetSolution({"subset": combination,}, problem=self.problem)

                if solution.is_optimal():
                    self.log_solution(solution, start_time)
                    return solution

                if limit and self.report["attempts"] == limit:
                    logger.warning(f"Runned out of tries (limit={limit})")
                    self.log_solution(solution, start_time)
                    return solution

                if verbose:
                    self.log_solution(solution, start_time)

        self.set_time(start_time)

        logger.warning(
            f"Solution cannot be found (time={self.report['time']}, attempts={self.report['attempts']})",
        )

        return None


class ClimbingSumOfSubsetSolver(Solver):
    """ class which implements Climbing algorithm for SumOfSubset"""

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
        random_solution = self.problem.generate_random_solution(size_of_subset=size)

        self.add_attempt()

        if random_solution.is_optimal():
            self.log_solution(random_solution, start_time)
            return random_solution

        for _ in range(1, limit):
            self.add_attempt()

            close_neighbor = self.problem.find_close_neighbor(random_solution)

            if close_neighbor.is_optimal():
                self.log_solution(close_neighbor, start_time)
                return close_neighbor

            if close_neighbor > random_solution:
                random_solution = close_neighbor

            if verbose:
                self.log_solution(close_neighbor, start_time)

        self.log_solution(random_solution, start_time)
        return random_solution


class SimulatedAnnealingSumOfSubsetSolver(Solver):
    """ class which implements SimulatedAnnealing algorithm for SumOfSubset"""

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
        random_solution = self.problem.generate_random_solution(size_of_subset=size)

        self.add_attempt()

        if random_solution.is_optimal():
            self.log_solution(random, start_time)
            return random_solution

        for _ in range(1, limit):
            self.add_attempt()
            close_neighbor = self.problem.find_close_neighbor(random_solution)

            if close_neighbor.is_optimal():
                self.log_solution(close_neighbor, start_time)
                return close_neighbor

            if close_neighbor > random_solution:
                random_solution = close_neighbor
            else:
                i = self.report.get("attempts")
                random_number = random.random()
                sa_condition = math.exp(
                    -(abs(close_neighbor.goal() - random_solution.goal()) / temperature(i))
                )

                if random_number < sa_condition:
                    random_solution = close_neighbor

            if verbose:
                self.log_solution(close_neighbor, start_time)

        self.log_solution(random_solution, start_time)
        return random_solution


class TabuSumOfSubsetSolver(Solver):
    """ class which implements TabuSumOfSubsetSolver algorithm for SumOfSubset """

    DEFAULT_LIMIT = 1000000
    DEFAULT_SIZE_OF_TABU = 1000
    DEFAULT_TABU_COUNT = 100

    def solve(self, **kwargs):
        self.log_welcome()

        verbose = kwargs.get("verbose", False)
        limit = kwargs.get("limit", self.DEFAULT_LIMIT)
        size = kwargs.get("size", random.randint(1, len(self.problem.set) // 2))
        size_of_tabu = kwargs.get("size_of_tabu", self.DEFAULT_SIZE_OF_TABU)
        tabu_count = kwargs.get("tabu_count", self.DEFAULT_TABU_COUNT)

        logger.info(f"Set size_of_tabu to {size_of_tabu} (default={self.DEFAULT_SIZE_OF_TABU})")
        logger.info(f"Set tabu_count to {tabu_count} (default={self.DEFAULT_TABU_COUNT})")
        logger.info(f"Set limit to {limit} (default={self.DEFAULT_LIMIT})")
        logger.info(f"Set verbose to {verbose} (default=False)")
        logger.info(f"Set size to {size}")

        current_tabu_count = 0

        start_time = time.time()

        random_solution = self.problem.generate_random_solution(size_of_subset=size)
        self.add_attempt()

        tabu_list = []

        if random_solution.is_optimal():
            self.log_solution(random_solution, start_time)
            return random_solution

        for _ in range(1, limit):
            self.add_attempt()
            if tabu_list and current_tabu_count == tabu_count:
                logger.info("Removed item from tabu_list")
                tabu_list.pop()
                current_tabu_count = 0

            if len(tabu_list) == size_of_tabu:
                logger.info("Removed item from tabu_list")
                tabu_list.pop()

            current_tabu_count += 1

            close_neighbor = self.problem.find_close_neighbor(random_solution)

            if close_neighbor.is_optimal():
                self.log_solution(close_neighbor, start_time)
                return close_neighbor

            if close_neighbor > random_solution:
                logger.info("Added item to tabu_list")
                current_tabu_count += 1
                tabu_list.append(random_solution)
                random_solution = close_neighbor

            if verbose:
                self.log_solution(close_neighbor, start_time)

        self.log_solution(random_solution, start_time)
        return random_solution


class SumOfSubsetProblem(Problem):
    """ class implementing SumOfSubset problem """

    solvers = {
        "bruteforce": BruteforceSumOfSubsetSolver,
        "climbing": ClimbingSumOfSubsetSolver,
        "sa": SimulatedAnnealingSumOfSubsetSolver,
        "tabu": TabuSumOfSubsetSolver,
    }

    def __init__(self, data):
        super().__init__(data)
        self.set = self.data["set"]
        self.number = self.data["number"]

    def generate_random_solution(self, **kwargs) -> SumOfSubsetSolution:
        size_of_subset = kwargs.get("size_of_subset")
        if not size_of_subset or size_of_subset > len(self.set) or size_of_subset < 0:
            size_of_subset = random.randint(1, len(self.set))

            logger.warning(
                f'"size_of_subset" is not provided or it is not correct, set to {size_of_subset}'
            )

        return SumOfSubsetSolution(
            data={"subset": random.sample(self.set, size_of_subset)}, problem=self
        )

    def find_close_neighbor(self, solution: SumOfSubsetSolution) -> SumOfSubsetSolution:
        new_subset = solution.subset[:]

        first_element, second_element = random.choices(self.set, k=2)

        if first_element in solution.subset:
            new_subset.remove(first_element)
        else:
            new_subset.append(first_element)

        if second_element in solution.subset and second_element in new_subset:
            if random.randint(1, 2) == 1:
                new_subset.remove(second_element)
        else:
            if random.randint(1, 2) == 1:
                new_subset.append(second_element)

        return SumOfSubsetSolution({"subset": new_subset}, self)


class SumOfSubsetExperiment(Experiment):
    """ class implementing SumOfSubset experiment """

    def __init__(self, data=None):
        super().__init__(data)

    @property
    def problem_class(self) -> SumOfSubsetProblem:
        """ returns SumOfSubsetProblem"""
        return SumOfSubsetProblem

    @staticmethod
    def _prepare_bar_plot(bars, values, matplotlib_ax):
        """ helper method to prepare extended bar plot """
        for idx, rect in enumerate(bars):
            height = rect.get_height()
            matplotlib_ax.text(
                rect.get_x() + rect.get_width() / 2,
                0.5 * height,
                values[idx],
                ha="center",
                va="bottom",
                rotation=90,
            )

    def _prepare_plots(self, path):
        """ helper method to prepare plots """
        data = self.data.get("report")
        times_for_problems = {}
        solvers_for_problems = {}

        for problem_idx, _ in enumerate(data):
            for report in data[problem_idx]:
                if not problem_idx in times_for_problems:
                    times_for_problems[problem_idx] = []
                if not problem_idx in solvers_for_problems:
                    solvers_for_problems[problem_idx] = []

                times_for_problems[problem_idx].append(report["report"]["time"])
                solvers_for_problems[problem_idx].append(f"{report['solver_id'] + 1}: {self.data['solvers'][report.get('solver_id')].get('solver_name')}")


        for problem_idx, results in times_for_problems.items():
            plt.figure()

            _, matplotlib_ax = plt.subplots()
            y_values = [str(n) for n in range(len(results))]

            bars = plt.bar(y_values, results)

            plt.title(f"Performance for {problem_idx + 1} problem")
            plt.ylabel("Time (in s)")

            labels = []

            for idx, _ in enumerate(results):
                labels.append(
                    f"{round(results[idx], 5)}  (solver {solvers_for_problems.get(problem_idx)[idx]})"
                )

            self._prepare_bar_plot(bars, labels, matplotlib_ax)
            plt.savefig(os.path.join(path, f"{problem_idx}.png"))

    def build_html_report(self, path: str):
        """ method to build HTML report """
        logger.info("Building HTML report")
        env = jinja2.Environment(loader=jinja2.PackageLoader("sum_of_subset_problem", "static"))

        template = env.get_template("report.html")

        with open(os.path.join(path, "report.html"), "w") as report_html:
            report_html.write(template.render(report=self.data))

        self._prepare_plots(path)

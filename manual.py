import os

import click

from sum_of_subset_problem import logger

from sum_of_subset_problem.utilities import generate_problem_with_solution
from sum_of_subset_problem.problem import (
    SumOfSubsetExperiment,
    SumOfSubsetProblem,
    BruteforceSumOfSubsetSolver,
    ClimbingSumOfSubsetSolver,
)


@click.group()
def cli():
    ...


@cli.command()
@click.option(
    "--method",
    default="bruteforce",
    help="Method to solve problem (bruteforce, climbing, sa, tabu)",
    prompt="Method to solve problem (bruteforce, climbing, sa, tabu)",
)
@click.option("--set", default=10, help="Size of set", prompt="Size of set")
@click.option("--subset", default=5, help="Size of subset", prompt="Size of subset")
@click.option(
    "--to_file",
    default=False,
    help="Path to output JSON file",
    prompt="Path to output JSON file",
)
@click.option("--verbose", default=False, help="Verbose mode", prompt="Verbose mode")
def random(method, set, subset, to_file, verbose):
    """ command to solve problem created randomly """
    problem_with_solution = generate_problem_with_solution(set, subset)
    problem = SumOfSubsetProblem(problem_with_solution["problem"])
    solver = problem.solvers.get(method)(problem)
    solution = solver.solve(verbose=verbose)

    if to_file:
        solution.export_to_json(to_file)


@cli.command()
@click.option(
    "--method",
    default="bruteforce",
    help="Method to solve problem (bruteforce, climbing, sa, tabu)",
    prompt="Method to solve problem (bruteforce, climbing, sa, tabu)",
)
@click.option(
    "--path",
    help="Path to JSON file with problem",
    prompt="Path to JSON file with problem",
    required=True,
)
@click.option(
    "--to_file",
    default=False,
    help="Path to output JSON file",
    prompt="Path to output JSON file",
)
@click.option("--verbose", default=False, help="Verbose mode", prompt="Verbose mode")
def from_file(method, path, to_file, verbose):
    """ command to solve problem/problems imported from json file """
    problem = SumOfSubsetProblem.from_json(path)

    if isinstance(problem, list):
        for idx, single_problem in enumerate(problem):
            solver = single_problem.solvers.get(method)(single_problem)
            solution = solver.solve(verbose=verbose)

            if to_file:
                solution.export_to_json(os.path.join(to_file, f"from_file{idx}.json"))

    else:
        solver = problem.solvers.get(method)(problem)
        solution = solver.solve(verbose=verbose)

        if to_file:
            solution.export_json(os.path.join(to_file, "from_file.json"))


@cli.command()
@click.option("--path", help="Path to experiment", prompt="Path to experiment")
@click.option(
    "--to_file",
    default=False,
    help="Path to output JSON file",
    prompt="Path to output JSON file",
)
def run_experiment(path, to_file):
    experiment = SumOfSubsetExperiment.from_json(path)
    experiment.run()

    if to_file:
        experiment.export_to_json(to_file)


if __name__ == "__main__":
    cli()

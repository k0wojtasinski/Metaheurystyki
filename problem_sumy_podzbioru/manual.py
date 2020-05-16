import os

import click

from utilities import generate_problem_with_solution
from problem import SumOfSubsetProblem, BruteforceSumOfSubsetSolver

SOLVERS = {"bruteforce": BruteforceSumOfSubsetSolver}


@click.group()
def cli():
    ...


@cli.command()
@click.option(
    "--method",
    default="bruteforce",
    help="Method to solve problem",
    prompt="Method to solve problem",
)
@click.option("--set", default=10, help="Size of set", prompt="Size of set")
@click.option("--subset", default=5, help="Size of subset", prompt="Size of subset")
@click.option(
    "--to_file",
    default=False,
    help="Path to output JSON file",
    prompt="Path to output JSON file",
)
@click.option("--verbose", default=False, help="Verbose mode")
def random(method, set, subset, to_file, verbose):
    """ command to solve problem created randomly """
    problem_with_solution = generate_problem_with_solution(set, subset)
    problem = SumOfSubsetProblem(problem_with_solution["problem"])
    solver = SOLVERS.get(method)(problem)
    solver.solve(verbose)

    if to_file:
        solver.export_correct_solutions_to_json(os.path.join(to_file, "random.json"))


@cli.command()
@click.option(
    "--method",
    default="bruteforce",
    help="Method to solve problem",
    prompt="Method to solve problem",
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
@click.option("--verbose", default=False, help="Verbose mode")
def from_file(method, path, to_file, verbose):
    """ command to solve problem/problems imported from json file """
    problem = SumOfSubsetProblem.from_json(path)

    if isinstance(problem, list):
        for idx, single_problem in enumerate(problem):
            solver = SOLVERS.get(method)(single_problem)
            solver.solve(verbose)

            if to_file:
                solver.export_correct_solutions_to_json(
                    os.path.join(to_file, f"from_file{idx}.json")
                )

    else:
        solver = SOLVERS.get(method)(problem)
        solver.solve(verbose)

        if to_file:
            solver.export_all_solutions_to_json(os.path.join(to_file, "from_file.json"))


if __name__ == "__main__":
    cli()

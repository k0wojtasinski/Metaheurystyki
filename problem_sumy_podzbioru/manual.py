import os

import click

from utilities import generate_problem_with_solution
from problem import BruteforceSumOfSubsetProblem


@click.group()
def cli():
    ...


@cli.command()
@click.option("--set", default=10, help="Size of set", prompt="Size of set")
@click.option("--subset", default=5, help="Size of subset", prompt="Size of subset")
@click.option("--to_file", help="Path to output JSON file", prompt="Path to output JSON file")
@click.option("--verbose", default=False, help="Verbose mode")
def random(set, subset, to_file, verbose):
    """ command to solve problem created randomly """
    problem_with_solution = generate_problem_with_solution(set, subset)
    problem = BruteforceSumOfSubsetProblem(problem_with_solution["problem"])
    problem.solve(verbose)
    
    if to_file:
        problem.export_correct_solutions_to_json(os.path.join(to_file, "random.json"))


@cli.command()
@click.option(
    "--path",
    help="Path to JSON file with problem",
    prompt="Path to JSON file with problem",
    required=True,
)
@click.option("--to_file", help="Path to output JSON file", prompt="Path to output JSON file")
@click.option("--verbose", default=False, help="Verbose mode")
def from_file(path, to_file, verbose):
    """ command to solve problem/problems imported from json file """
    problem = BruteforceSumOfSubsetProblem.from_json(path)
    
    if isinstance(problem, list):
        for idx, single_problem in enumerate(problem):
            single_problem.solve(verbose)

            if to_file:
                single_problem.export_correct_solutions_to_json(os.path.join(to_file, f"from_file{idx}.json"))
    else:
        problem.solve(verbose)
        if to_file:
            problem.export_all_solutions_to_json(os.path.join(to_file, "from_file.json"))

if __name__ == "__main__":
    cli()

import click

from utilities import generate_problem_with_solution
from problem import BruteforceSumOfSubsetProblem


@click.group()
def cli():
    ...


@cli.command()
@click.option("--set", default=10, help="Size of set", prompt="Size of set")
@click.option("--subset", default=5, help="Size of subset", prompt="Size of subset")
@click.option("--verbose", default=False, help="Verbose mode")
def random(set, subset, verbose):
    """ command to solve problem created randomly """
    problem_with_solution = generate_problem_with_solution(set, subset)
    problem = BruteforceSumOfSubsetProblem(problem_with_solution["problem"])
    problem.solve(verbose)


@cli.command()
@click.option(
    "--path",
    help="Path to JSON file with problem",
    prompt="Path to JSON file with problem",
    required=True,
)
@click.option("--verbose", default=False, help="Verbose mode")
def from_file(path, verbose):
    """ command to solve problem/problems imported from json file """
    problem = BruteforceSumOfSubsetProblem.from_json(path)
    
    if isinstance(problem, list):
        for single_problem in problem:
            single_problem.solve(verbose)
    else:
        problem.solve(verbose)

if __name__ == "__main__":
    cli()

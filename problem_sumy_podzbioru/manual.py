import click

from utilities import generate_problem_with_solution
from problem import BruteforceSumOfSubsetProblem


@click.group()
def cli():
    ...


@cli.command()
@click.option("--set", default=10, help="Size of set", prompt="Size of set")
@click.option("--subset", default=5, help="Size of subset", prompt="Size of subset")
def random(set, subset):
    problem_with_solution = generate_problem_with_solution(set, subset)
    problem = BruteforceSumOfSubsetProblem(problem_with_solution["problem"])
    print(problem.solve())


@cli.command()
@click.option(
    "--path",
    help="Path to JSON file with problem",
    prompt="Path to JSON file with problem",
    required=True,
)
def from_file(path):
    problem = BruteforceSumOfSubsetProblem.from_json(path)
    print(problem.solve())


if __name__ == "__main__":
    cli()

import click
import os

from typing import Union
from git import Repo


@click.command()
@click.option("--input", help="The file you'd like to see a timeline of")
@click.option(
    "--output", default="timeline.html", help="An optional name for the output file"
)
def code_timeline(input: str, output: str) -> None:
    git_path = get_nearest_git_repo(input)
    repository = Repo(git_path)
    if repository.is_dirty():
        click.echo(
            "It looks like some files in this repo haven't had their changes committed. Please get the repository into a clean state before running CodeTimeline"
        )
        exit
    click.echo(f"git directory is {git_path}")
    click.echo(repository)


def get_nearest_git_repo(directory: str) -> Union[str, None]:
    click.echo(f"current directory is {directory}")
    click.echo(f"is .git a subdirectory? {os.path.isdir('.git')}")

    if os.path.isdir(os.path.join(directory, ".git")) is True:
        return directory

    head, tail = os.path.split(directory)
    if tail != "":
        return get_nearest_git_repo(head)
    else:
        return None


if __name__ == "__main__":
    code_timeline()

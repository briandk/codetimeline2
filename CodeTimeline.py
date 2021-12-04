import click
import os

from git import Repo
from typing import Union


@click.command()
@click.option("--input", help="The file you'd like to see a timeline of")
@click.option(
    "--output", default="timeline.html", help="An optional name for the output file"
)
def code_timeline(input: str, output: str) -> None:
    git_path = get_nearest_git_repo(input)
    repository = Repo(git_path)
    report_if_repository_is_dirty(repository)
    click.echo(f"git directory is {git_path}")


def get_nearest_git_repo(directory: str) -> Union[str, None]:
def get_nearest_git_repo(filepath: str) -> Union[str, None]:
    """
    Takes a filepath and recursively searches upward to find
    the nearest git repository
    """
    # click.echo(f"current directory is {directory}")
    # click.echo(f"is .git a subdirectory? {os.path.isdir('.git')}")

    if os.path.isdir(os.path.join(filepath, ".git")) is True:
        return filepath

    head, tail = os.path.split(filepath)
    if tail != "":
        return get_nearest_git_repo(head)
    else:
        return None


def report_if_repository_is_dirty(repo: Repo) -> None:
    if repo.is_dirty():
        click.echo(
            "ERROR: Repo not clean. It looks like some files in this repo haven't had their changes committed. Please get the repository into a clean state before running CodeTimeline"
        )
        exit


def sanitizeFilepath(filepath: str) -> str:
    """
    Takes a path to a file, however the user wants to specify it,
    and "cleans" it by normalizing, expanding home directories, and making it an absolute path.
    """
    filepath = os.path.expanduser(filepath)
    if os.path.isabs(filepath) == False:
        filepath = os.path.join(os.getcwd(), filepath)
    filepath = os.path.normpath(filepath)
    return filepath


if __name__ == "__main__":
    code_timeline()

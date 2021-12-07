import click
import os
import sys
from typing import Union

from git import Repo


def find_nearest_git_repo(filepath: str) -> Union[str, None]:
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
        return find_nearest_git_repo(head)
    else:
        return None


def git_data(filepath: str) -> dict:
    """Takes the path to a file and returns a
    data object that can be injected into the
    timeline_view template
    """
    pass


def report_if_repository_is_dirty(repo: Repo) -> None:
    if repo.is_dirty():
        click.echo(
            """
ERROR: Repo not clean.
It looks like some files in this repo haven't had their changes committed.
Please get the repository into a clean state before running CodeTimeline
"""
        )
        sys.exit()
    else:
        return None

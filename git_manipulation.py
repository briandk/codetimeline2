import click
import os
import sys
from typing import Union

from git import Repo


def git_data(filepath: str) -> dict:
    """Takes the path to a file and returns a
    data object that can be injected into the
    timeline_view template
    """
    repo = Repo(find_nearest_git_repo(filepath))
    report_if_repository_is_dirty(repo)


def find_nearest_git_repo(filepath: str) -> Union[str, None]:
    """
    Takes a filepath and recursively searches upward to find
    the nearest git repository
    """
    if os.path.isdir(os.path.join(filepath, ".git")) is True:
        click.echo(f"repo path is {filepath}")
        return filepath

    head, tail = os.path.split(filepath)
    if tail != "":
        return find_nearest_git_repo(head)
    else:
        return None


def report_if_repository_is_dirty(repo: Repo) -> None:
    click.echo("checking whether repository is dirty...")
    if repo.is_dirty():
        click.echo(
            """ERROR: Repo not clean.
It looks like some files in this repo haven't had their changes committed.
Please get the repository into a clean state before running CodeTimeline
"""
        )
        sys.exit()
    else:
        return None

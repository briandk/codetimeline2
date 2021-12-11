import click
import os
import sys
from typing import Union

from git import Repo


def git_data(filepath: str) -> list[str]:
    """Takes the path to a file and returns a
    data object about that file that can be injected into the
    timeline_view template
    """
    repo = find_nearest_git_repo(filepath)
    blame_data = repo.blame(rev=repo.active_branch, file=filepath)
    return blame_data


def find_nearest_git_repo(filepath: str) -> Union[Repo, None]:
    """
    Takes a filepath and recursively searches upward to find
    the nearest git repository
    """
    is_git_repo = os.path.isdir(os.path.join(filepath, ".git"))
    if is_git_repo:
        os.chdir(filepath)
        my_repo = Repo(path=filepath)
        report_if_repository_is_dirty(my_repo)
        return my_repo

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

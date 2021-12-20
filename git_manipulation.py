import click
import os
import sys
from typing import Union

from git import Repo

from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import guess_lexer
from pygments.lexers import guess_lexer_for_filename


def git_data(filepath: str) -> list[str]:
    """Takes the path to a file and returns a
    data object about that file that can be injected into the
    timeline_view template
    """
    repo = find_nearest_git_repo(filepath)
    blame_data = repo.blame(rev=repo.active_branch, file=filepath)
    raw_source_code = source_code(blame_data)
    lexer = guess_lexer_for_filename(filepath, raw_source_code)
    highlighted_code = highlight(
        raw_source_code,
        lexer,
        HtmlFormatter(linenos=True, hl_lines=[1, 2, 3, 11], wrapcode=True),
    )
    return [highlighted_code]


# def highlighted_source_code


def source_code(blame_data) -> list[str]:
    """
    Takes a blame view (list of [commit, [lines]]) and extracts out raw source code lines
    """

    raw_lines: list[str] = list()

    for entry in blame_data:
        lines = entry[1]
        for line in lines:
            raw_lines.append(line)

    return "\n".join(raw_lines).strip()
    # return "\n".join([line for line in blamelet[1]])


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

import click
import os
import sys

from typing import Any
from typing import Union

from git import Repo
from git import Commit

from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import guess_lexer
from pygments.lexers import guess_lexer_for_filename


def revisions_of_file(repo: Repo, filepath: str) -> tuple[str]:
    revisons = [
        commit.hexsha
        for commit in repo.iter_commits(rev=repo.active_branch, paths=filepath)
    ]

    return tuple(revisons)


def git_data(filepath: str) -> tuple[Any]:
    """Takes the path to a file and returns a
    data object about that file that can be injected into the
    timeline_view template
    """
    repo = find_nearest_git_repo(filepath)
    revisions = revisions_of_file(repo, filepath)
    snapshots = [compose_snapshot(repo, filepath, rev) for rev in revisions]

    # so the left-most snapshot is the earliest in the timeline
    snapshots.reverse()

    return tuple(snapshots)


def compose_snapshot(repo: Repo, filepath: str, revision: str) -> str:
    """
    Takes a repo, a filepath, and a hexsha for a revision, then returns
    an HTML string representing the entire tokenized source code
    for that file at that revision.
    """
    blame_data = extract_blamelets(repo, filepath, revision)
    raw_source_code = source_code(blame_data)
    lexer = guess_lexer_for_filename(filepath, raw_source_code)
    highlighted_code = highlight(
        raw_source_code,
        lexer,
        HtmlFormatter(
            linenos=True,
            wrapcode=True,
            hl_lines=line_numbers_to_highlight(blame_data, revision),
        ),
    )
    return {"highlighted_code": highlighted_code, "short_sha": revision[0:9]}


def line_numbers_to_highlight(blame_data, revision: str):
    return [
        blamelet["line_number"]
        for blamelet in blame_data
        if blamelet["commit"].hexsha == revision
    ]


def extract_blamelets(repo: Repo, filepath: str, revision: str):
    """
    Takes GitPython's compactified blame representation,
    which is list[<commit>, list[source_lines]]
    and expands out to tuple[<commit>, source_line] for each line in the source code.
    """
    compact_blame_data = repo.blame(rev=revision, file=filepath)
    blame_data = list()

    for entry in compact_blame_data:
        for line in entry[1]:
            blame_data.append({"commit": entry[0], "code": line, "line_number": None})

    # Why are we doing `index + 1` instead of index?
    #
    # Because the blame view is zero-indexed, but pygments's `hl_lines`
    #    argument assumes lines start at number 1
    for (index, value) in enumerate(blame_data):
        blame_data[index]["line_number"] = index + 1

    return tuple(blame_data)


def source_code(blame_data) -> str:
    """
    Takes a blame view (list of [<commit>, [lines]]) and extracts out raw source code lines
    """

    source_code = [blamelet["code"] for blamelet in blame_data]

    return "\n".join(source_code)


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

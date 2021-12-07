import click
import os
import sys

from git import Repo
from pybars import Compiler
from typing import Union


@click.command()
@click.option("--input", help="The file you'd like to see a timeline of")
@click.option(
    "--output",
    default="timeline.html",
    help="An optional name for the output file",
)
def code_timeline(input: str, output: str) -> None:
    repository = Repo(get_nearest_git_repo(input))
    # click.echo(f"git directory is {repository}")
    report_if_repository_is_dirty(repository)
    writeTimelineToFile(output, compile_timeline_template())
    click.echo("All done!")


def external_files() -> dict:
    with open(os.path.join("external_files", "bootstrap.css")) as f:
        bootstrap_css = f.read()
    with open(os.path.join("external_files", "bootstrap.js")) as f:
        bootstrap_script = f.read()
    with open(os.path.join("external_files", "jQuery.js")) as f:
        jquery_script = f.read()

    return {
        "bootstrap_css": bootstrap_css,
        "bootstrap_js": bootstrap_script,
        "jquery_js": jquery_script,
    }


def timeline_template() -> dict:
    """Returns a data object that can then be
    passed to a Handlebars compiler
    """
    return external_files()


def compile_timeline_template():
    """Injects the CodeTimeline data into the template
    and returns a single HTML document
    """
    compiler = Compiler()
    with open("timeline_view.handlebars", "r", encoding="utf8") as f:
        raw_template = f.read()
    template = compiler.compile(raw_template)
    return str(template(timeline_template()))


def writeTimelineToFile(output_path: str, timeline: str) -> None:
    """
    Writes the CodeTimeline HTML out to a file
    """
    print(f"Output path is {output_path}")
    with open(output_path, "w", encoding="utf8") as f:
        f.write(timeline)


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
            """
ERROR: Repo not clean.
It looks like some files in this repo haven't had their changes committed.
Please get the repository into a clean state before running CodeTimeline
"""
        )
        sys.exit()
    else:
        return None


def sanitize_filepath(filepath: str) -> str:
    """
    Takes a path to a file, however the user wants to specify it,
    and "cleans" it by normalizing, expanding home directories, and making it an absolute path.
    """
    filepath = os.path.expanduser(filepath)
    if not os.path.isabs(filepath):
        filepath = os.path.join(os.getcwd(), filepath)
    filepath = os.path.normpath(filepath)
    return filepath


if __name__ == "__main__":
    code_timeline()

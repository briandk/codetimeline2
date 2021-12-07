import click
import os

from pybars import Compiler
from typing import Union
from git_manipulation import git_data


@click.command()
@click.option("--input", help="The file you'd like to see a timeline of")
@click.option(
    "--output",
    default="timeline.html",
    help="An optional name for the output file",
)
def code_timeline(input: str, output: str) -> None:
    git_data(input)
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
    return {"external_files": external_files()}


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

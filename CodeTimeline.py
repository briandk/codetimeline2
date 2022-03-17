import click
import os

from pybars import Compiler

from git_manipulation import git_data
from pygments.formatters import HtmlFormatter


@click.command()
@click.option("--input", help="The file you'd like to see a timeline of")
@click.option(
    "--output",
    default="timeline.html",
    help="An optional name for the output file",
)
def code_timeline(input: str, output: str) -> None:
    external_js_and_css = external_files()
    template = timeline_template()
    input_file = sanitize_filepath(input)
    template_data = {
        "snapshots": git_data(input_file),
        "external_files": external_js_and_css,
    }
    timeline = template(template_data)
    writeTimelineToFile(output, timeline)
    click.echo("All done!")


def external_files() -> dict[str:str]:
    with open(os.path.join("external_files", "bootstrap.css")) as f:
        bootstrap_css = f.read()
    with open(os.path.join("external_files", "bootstrap.bundle.js")) as f:
        bootstrap_js = f.read()
    with open(os.path.join("external_files", "TimelineStyle.css")) as f:
        timeline_style_css = f.read()
    with open(os.path.join("external_files", "Timeline.js")) as f:
        timeline_js = f.read()

    pygments_css = HtmlFormatter().get_style_defs(".highlight")

    return {
        "css": [
            bootstrap_css,
            pygments_css,
            timeline_style_css,
        ],
        "js": [bootstrap_js, timeline_js],
    }


def timeline_template():
    """Returns a compiled handlebars template (as a function),
    which can be called on an input data object to produce HTML
    """
    compiler = Compiler()
    with open("timeline_view.handlebars", "r", encoding="utf8") as f:
        raw_template = f.read()
    template = compiler.compile(raw_template)
    return template


def writeTimelineToFile(output_path: str, timeline: str) -> None:
    """
    Writes the CodeTimeline HTML out to a file
    """
    click.echo(f"Output path is {output_path}")
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
    filepath = os.path.realpath(os.path.normpath(filepath))
    return filepath


if __name__ == "__main__":
    code_timeline()

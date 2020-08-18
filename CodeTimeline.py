import click
import os


@click.command()
def code_timeline():
    git_path = get_nearest_git_repo(os.getcwd())
    click.echo(f"git directory is {git_path}")


def get_nearest_git_repo(directory):
    click.echo(f"current directory is {directory}")
    click.echo(f"is .git a subdirectory? {os.path.isdir('.git')}")

    if os.path.isdir(os.path.join(directory, ".git")) is True:
        return directorycd
    head, tail = os.path.split(directory)
    click.echo(f"head is {head}")
    if tail is not "":
        return get_nearest_git_repo(head)
    else:
        return None


if __name__ == "__main__":
    code_timeline()

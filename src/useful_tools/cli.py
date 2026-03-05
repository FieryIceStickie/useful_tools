import typer
from importlib.resources import files, as_file
from .misc.misc import obsidian_to_quora

app = typer.Typer(no_args_is_help=True)


@app.command()
def otq(filename: str):
    target = files('useful_tools') / 'storage/ob' / filename
    with as_file(target) as path:
        with open(path, 'r') as file:
            print(obsidian_to_quora(file.read()))

@app.callback()
def callback():
    """
    Useful tools CLI
    """



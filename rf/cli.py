import tomllib
import typer

app = typer.Typer(no_args_is_help=True)

with open("pyproject.toml", "rb") as f:
    pyprojecttoml = tomllib.load(f)

data = {
    "version": pyprojecttoml["project"]["version"],
    "instruments": {},
    "books": {},
    "constants": {
        "c": 3e8,
    },
}


@app.command()
def calculate() -> None:
    """
    Perform essential RF computations such as Friis transmission equations and impedance matching.
    """
    typer.echo("calculating done")


@app.command()
def visualize() -> None:
    """
    Get a dashboard of visualizations by inputting a csv- or s2p-file.
    """
    typer.echo("visualizing done")


@app.command()
def measure() -> None:
    """
    Perform common measurements for RF design using instruments connected by LAN or USB. Get a screen dump, raw data or simply setup your spectrum analyzer with your favorite presets. Use with rf visualize for an extremely efficient workflow.
    """
    typer.echo("visualizing done")


@app.command()
def learn() -> None:
    """
    Manage, search and organize books, slides, urls and more. Think Elsevier meets bookmarks meets terminal
    """
    typer.echo("learning done")


@app.command()
def template() -> None:
    """
    Interactively construct templates and scripts for commonly used software in RF engineering.
    """
    typer.echo("templating done")


@app.command()
def station() -> None:
    """
    Data in path for 'rf' to use.
    """
    typer.echo(data)


@app.command()
def version():
    """
    Show version of the the "rf-cli" tool in path
    """
    typer.echo(data["version"])


if __name__ == "__main__":
    app()

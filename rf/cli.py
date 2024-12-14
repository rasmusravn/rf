import subprocess
import sys
import tempfile
from importlib.resources import files
from typing import Annotated, Optional

import tomllib
import typer

app = typer.Typer(no_args_is_help=True)

pyproject_path = files("rf").joinpath("../pyproject.toml")

with pyproject_path.open("rb") as f:
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
def visualize(
    file_type: str = typer.Option(
        "s2p", help="Type of file to process (s2p or csv)", case_sensitive=False
    ),
    file: Annotated[Optional[str], typer.Argument()] = None,
) -> None:
    """
    Launch a Streamlit visualization app.
    """
    valid_file_types = {"s2p", "csv"}
    if file_type.lower() not in valid_file_types:
        raise typer.BadParameter(
            f"Invalid file type '{file_type}'. Must be one of {valid_file_types}."
        )
    # Determine input source
    if file:
        typer.echo(f"Visualizing data from file: {file}")
        data_source = file
    elif not sys.stdin.isatty():  # Check if stdin has input
        typer.echo("Reading data from stdin...")  # Validate file type
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=f".{file_type.lower()}", mode="wb"
        ) as temp_file:
            data = sys.stdin.read()
            temp_file.write(data.encode("utf-8"))
            data_source = temp_file.name
            typer.echo(data_source)

    # Locate the visualizer script
    visualizer_script = files("rf").joinpath("visualize/page1.py")

    # Pass the file and file type to the Streamlit app
    typer.echo(f"Launching Streamlit app with {file_type}")
    subprocess.run(
        ["streamlit", "run", str(visualizer_script), "--", data_source, file_type]
    )


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

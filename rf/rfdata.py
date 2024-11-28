import json
from pathlib import Path

import typer
from platformdirs import user_config_dir

APP_NAME = "rf"

config_dir = Path(user_config_dir(APP_NAME))
config_dir.mkdir(parents=True, exist_ok=True)
config_file = config_dir / "config.json"


def load_config():
    if config_file.exists():
        with open(config_file, "r") as f:
            return json.load(f)
    return {}


def save_config(config: dict):
    with open(config_file, "w") as f:
        json.dump(config, f, indent=4)


def get_data_dir():
    config = load_config()
    data_dir = config.get("data_dir")

    if not data_dir or not Path(data_dir).exists():
        typer.echo("No valid data directory found")
        data_dir = typer.prompt("Please input a directory for storing user data")
        data_path = Path(data_dir).expanduser()

        if not data_path.exists():
            data_path.mkdir(parents=True, exist_ok=True)
            typer.echo(f"Created directory: {data_path}")

            config["data_dir"] = str(data_path)
            save_config(config)

    return Path(config["data_dir"]).expanduser()

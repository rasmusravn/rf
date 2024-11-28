from datetime import datetime
from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class Ressource(BaseModel):
    title: str
    type: str
    author: Optional[str] = None
    tags: Optional[List[str]] = Field(default_factory=list)
    date: Optional[str]
    path: Path

    @validator("type")
    def validate_type(cls, v):
        valid_types = {"book", "article", "slides"}
        if v not in valid_types:
            raise ValueError(f"Type must be of one of {valid_types}")

    @validator("date", pre=True, always=True)
    def validate_date(cls, v):
        if v is None:
            return v
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            ValueError("Date must be in YYYY-MM-DD format")
        return v

    @validator
    def validate_path(cls, v):
        if not v.is_file() or v.suffix.lower() != ".pdf":
            raise ValueError(f"Path '{v}' is not a valid PDF file")
        return v


@app.command()
def add_resource(title: str, type: str) -> None:
    """
    Add a new resource to a user defined directory
    """
    data_dir = get_data_dir()
    typer.echo(f"Using data directory: {data_dir}")

    resource_dir = data_dir / type
    resource_dir.mkdir(parents=True, exist_ok=True)

    metadata_file = resource_dir / f"{title}.json"
    with open(metadata_file, "w") as f:
        json.dump({"title": title, "type": type}, f, indent=4)

    typer.echo(f"Save resource '{title}' in {resource_dir}")

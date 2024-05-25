"""Console script for todoist_interlingua."""
import todoist_interlingua

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for todoist_interlingua."""
    console.print("Replace this message by putting your code into "
               "todoist_interlingua.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    


if __name__ == "__main__":
    app()

import os
import typer
from .todoist_interlingua import pull_data, validate_data, push_data, generate_schema

app = typer.Typer()

@app.command()
def pull(api_token: str = typer.Option(None, envvar='TODOIST_API_TOKEN')):
    """
    Pull the entire state of your Todoist database.
    """
    pull_data(api_token)

@app.command()
def validate():
    """
    Validate the Todoist data in the local JSON file.
    """
    validate_data()

@app.command()
def push(api_token: str = typer.Option(None, envvar='TODOIST_API_TOKEN')):
    """
    Push the modified Todoist data back to Todoist.
    """
    push_data(api_token)

@app.command()
def generate_schema():
    """
    Generate JSON Schema from the Pydantic models.
    """
    generate_schema()

if __name__ == "__main__":
    app()

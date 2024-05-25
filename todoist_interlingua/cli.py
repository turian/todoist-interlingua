import typer

# Try both relative and absolute imports for compatibility
try:
    from todoist_interlingua.interlingua import (
        pull_data,
        validate_data,
        generate_schema,
    )  # Removed push_data import
except ImportError:
    from .interlingua import pull_data, validate_data, generate_schema

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


app = typer.Typer()


@app.command()
def pull(api_token: str = typer.Option(None, envvar="TODOIST_API_TOKEN")):
    """
    Pull the entire state of your Todoist database.
    """
    if not api_token:
        typer.echo("Error: API token is required")
        raise typer.Exit(code=1)
    try:
        pull_data(api_token)
        typer.echo("Data pulled successfully")
    except Exception as e:
        typer.echo(f"Error pulling data: {e}")
        raise typer.Exit(code=1)


@app.command()
def validate():
    """
    Validate the Todoist data in the local JSON file.
    """
    try:
        validate_data()
        typer.echo("Data is valid!")
    except Exception as e:
        typer.echo(f"Error validating data: {e}")
        raise typer.Exit(code=1)


# Disabling the push command
# @app.command()
# def push(api_token: str = typer.Option(None, envvar='TODOIST_API_TOKEN')):
#     """
#     Push the modified Todoist data back to Todoist.
#     """
#     if not api_token:
#         typer.echo("Error: API token is required")
#         raise typer.Exit(code=1)
#     try:
#         push_data(api_token)
#         typer.echo("Data pushed successfully")
#     except Exception as e:
#         typer.echo(f"Error pushing data: {e}")
#         raise typer.Exit(code=1)


@app.command()
def generate_schema():
    """
    Generate JSON Schema from the Pydantic models.
    """
    try:
        generate_schema()
        typer.echo("Schema generated successfully")
    except Exception as e:
        typer.echo(f"Error generating schema: {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()

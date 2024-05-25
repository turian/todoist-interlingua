import subprocess
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def run_cli_command(command):
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.abspath("src")  # Ensure src/ is in the Python path
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True, env=env
    )
    return result.stdout, result.stderr, result.returncode


def test_pull_command():
    command = "python todoist_interlingua/cli.py pull"
    stdout, stderr, returncode = run_cli_command(command)
    print("stdout:", stdout)
    print("stderr:", stderr)
    assert returncode == 0
    assert "Data pulled successfully" in stdout or "Data is valid!" in stdout


def test_validate_command():
    command = "python todoist_interlingua/cli.py validate"
    stdout, stderr, returncode = run_cli_command(command)
    print("stdout:", stdout)
    print("stderr:", stderr)
    assert returncode == 0
    assert "Data is valid!" in stdout


"""
def test_push_command():
    command = "python todoist_interlingua/cli.py push"
    stdout, stderr, returncode = run_cli_command(command)
    print("stdout:", stdout)
    print("stderr:", stderr)
    assert returncode == 0
    assert "Data pushed successfully" in stdout
"""


def test_generate_schema_command():
    command = "python todoist_interlingua/cli.py generate_schema"
    stdout, stderr, returncode = run_cli_command(command)
    print("stdout:", stdout)
    print("stderr:", stderr)
    assert returncode == 0
    assert os.path.exists("todoist_schema.json")
    with open("todoist_schema.json", "r") as f:
        schema = json.load(f)
    assert "title" in schema and schema["title"] == "Project"

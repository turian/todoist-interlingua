import subprocess
import json
import pytest
import os

def run_cli_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True, env=os.environ)
    return result.stdout, result.stderr, result.returncode

def test_pull_command():
    command = "python src/todoist_interlingua/cli.py pull"
    stdout, stderr, returncode = run_cli_command(command)
    assert returncode == 0
    assert "Data pulled successfully" in stdout

def test_validate_command():
    command = "python src/todoist_interlingua/cli.py validate"
    stdout, stderr, returncode = run_cli_command(command)
    assert returncode == 0
    assert "Data is valid!" in stdout

def test_push_command():
    command = "python src/todoist_interlingua/cli.py push"
    stdout, stderr, returncode = run_cli_command(command)
    assert returncode == 0
    assert "Data pushed successfully" in stdout

def test_generate_schema_command():
    command = "python src/todoist_interlingua/cli.py generate_schema"
    stdout, stderr, returncode = run_cli_command(command)
    assert returncode == 0
    assert os.path.exists("todoist_schema.json")
    with open("todoist_schema.json", "r") as f:
        schema = json.load(f)
    assert "title" in schema and schema["title"] == "Project"


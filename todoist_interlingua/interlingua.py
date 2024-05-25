import requests
import json
import time
from pydantic import ValidationError
from tqdm import tqdm

try:
    from todoist_interlingua.models import Project, Section, Task, Label, Comment
except ImportError:
    from .models import Project, Section, Task, Label

API_BASE_URL = "https://api.todoist.com/rest/v2"


def get_headers(api_token: str):
    return {"Authorization": f"Bearer {api_token}", "Content-Type": "application/json"}


def make_request_with_retry(url, headers, retries=5, backoff_factor=1):
    for i in range(retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:  # Rate limit error
                wait_time = backoff_factor * (2**i)
                print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise e
    raise Exception("Max retries exceeded")


def pull_data(api_token: str):
    try:
        print("Pulling projects...")
        projects_data = make_request_with_retry(
            f"{API_BASE_URL}/projects", get_headers(api_token)
        )

        print("Pulling sections...")
        sections_data = make_request_with_retry(
            f"{API_BASE_URL}/sections", get_headers(api_token)
        )

        print("Pulling tasks...")
        tasks_data = make_request_with_retry(
            f"{API_BASE_URL}/tasks", get_headers(api_token)
        )

        print("Pulling labels...")
        labels_data = make_request_with_retry(
            f"{API_BASE_URL}/labels", get_headers(api_token)
        )

        print("Processing data...")
        projects = [
            Project(**project)
            for project in tqdm(projects_data, desc="Processing projects")
        ]
        sections = [
            Section(**section)
            for section in tqdm(sections_data, desc="Processing sections")
        ]
        tasks = [Task(**task) for task in tqdm(tasks_data, desc="Processing tasks")]
        labels = [
            Label(**label) for label in tqdm(labels_data, desc="Processing labels")
        ]

        project_dict = {project.id: project for project in projects}
        section_dict = {section.id: section for section in sections}

        # Nest sections within projects
        for section in sections:
            if section.project_id in project_dict:
                project_dict[section.project_id].sections.append(section)

        # Nest tasks within sections and projects
        for task in tasks:
            if task.section_id and task.section_id in section_dict:
                section_dict[task.section_id].tasks.append(task)
            elif task.project_id and task.project_id in project_dict:
                project_dict[task.project_id].tasks.append(task)

        print("Saving data to file...")
        with open("todoist_data.json", "w") as f:
            json.dump([project.dict() for project in projects], f, indent=4)

        print("Data pulled successfully")

    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
    except ValidationError as e:
        print(e.json())
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")


def validate_data():
    try:
        with open("todoist_data.json", "r") as f:
            data = json.load(f)
        projects = [Project(**item) for item in data]
        print("Data is valid!")
    except ValidationError as e:
        print("Validation failed!")
        print(e.json())
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")


def generate_schema():
    try:
        schema = Project.schema_json(indent=2)
        with open("todoist_schema.json", "w") as f:
            f.write(schema)
        print("Schema generated successfully")
    except ValidationError as e:
        print("Validation failed!")
        print(e.json())

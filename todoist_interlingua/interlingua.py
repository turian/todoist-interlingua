import requests
import json
from pydantic import ValidationError
from tqdm import tqdm

try:
    from todoist_interlingua.models import Project, Section, Task, Label, Comment
except ImportError:
    from .models import Project, Section, Task, Label, Comment

API_BASE_URL = "https://api.todoist.com/rest/v2"


def get_headers(api_token: str):
    return {"Authorization": f"Bearer {api_token}", "Content-Type": "application/json"}


def pull_data(api_token: str):
    try:
        print("Pulling projects...")
        projects_response = requests.get(
            f"{API_BASE_URL}/projects", headers=get_headers(api_token)
        )
        projects_response.raise_for_status()
        projects_data = projects_response.json()

        print("Pulling sections...")
        sections_response = requests.get(
            f"{API_BASE_URL}/sections", headers=get_headers(api_token)
        )
        sections_response.raise_for_status()
        sections_data = sections_response.json()

        print("Pulling tasks...")
        tasks_response = requests.get(
            f"{API_BASE_URL}/tasks", headers=get_headers(api_token)
        )
        tasks_response.raise_for_status()
        tasks_data = tasks_response.json()

        print("Pulling labels...")
        labels_response = requests.get(
            f"{API_BASE_URL}/labels", headers=get_headers(api_token)
        )
        labels_response.raise_for_status()
        labels_data = labels_response.json()

        print("Pulling comments for projects...")
        project_comments_data = []
        for project in tqdm(projects_data, desc="Fetching project comments"):
            comments_response = requests.get(
                f"{API_BASE_URL}/comments?project_id={project['id']}",
                headers=get_headers(api_token),
            )
            if comments_response.status_code == 200:
                project_comments_data.extend(comments_response.json())
            else:
                print(
                    f"Failed to fetch comments for project {project['id']}: {comments_response.text}"
                )

        print("Pulling comments for tasks...")
        task_comments_data = []
        for task in tqdm(tasks_data, desc="Fetching task comments"):
            comments_response = requests.get(
                f"{API_BASE_URL}/comments?task_id={task['id']}",
                headers=get_headers(api_token),
            )
            if comments_response.status_code == 200:
                task_comments_data.extend(comments_response.json())
            else:
                print(
                    f"Failed to fetch comments for task {task['id']}: {comments_response.text}"
                )

        comments_data = project_comments_data + task_comments_data

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
        comments = [
            Comment(**comment)
            for comment in tqdm(comments_data, desc="Processing comments")
        ]

        for project in projects:
            project.sections = [
                section for section in sections if section.project_id == project.id
            ]
            for section in project.sections:
                section.tasks = [
                    task for task in tasks if task.section_id == section.id
                ]

        print("Saving data to file...")
        with open("todoist_data.json", "w") as f:
            json.dump([project.dict() for project in projects], f, indent=4)
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

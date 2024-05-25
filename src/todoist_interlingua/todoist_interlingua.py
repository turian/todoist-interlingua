import requests
import json
from pydantic import ValidationError
from .models import Project, Section, Task, Label, Comment

API_BASE_URL = "https://api.todoist.com/rest/v2"

def get_headers(api_token: str):
    return {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

def pull_data(api_token: str):
    projects_response = requests.get(f"{API_BASE_URL}/projects", headers=get_headers(api_token))
    projects_data = projects_response.json()
    
    sections_response = requests.get(f"{API_BASE_URL}/sections", headers=get_headers(api_token))
    sections_data = sections_response.json()
    
    tasks_response = requests.get(f"{API_BASE_URL}/tasks", headers=get_headers(api_token))
    tasks_data = tasks_response.json()

    labels_response = requests.get(f"{API_BASE_URL}/labels", headers=get_headers(api_token))
    labels_data = labels_response.json()

    comments_response = requests.get(f"{API_BASE_URL}/comments", headers=get_headers(api_token))
    comments_data = comments_response.json()
    
    try:
        projects = [Project(**project) for project in projects_data]
        sections = [Section(**section) for section in sections_data]
        tasks = [Task(**task) for task in tasks_data]
        labels = [Label(**label) for label in labels_data]
        comments = [Comment(**comment) for comment in comments_data]

        for project in projects:
            project.sections = [section for section in sections if section.project_id == project.id]
            for section in project.sections:
                section.tasks = [task for task in tasks if task.section_id == section.id]

        with open('todoist_data.json', 'w') as f:
            json.dump([project.dict() for project in projects], f, indent=4)
    except ValidationError as e:
        print(e.json())

def validate_data():
    with open('todoist_data.json', 'r') as f:
        data = json.load(f)
    try:
        projects = [Project(**item) for item in data]
        print("Data is valid!")
    except ValidationError as e:
        print("Validation failed!")
        print(e.json())

def push_data(api_token: str):
    with open('todoist_data.json', 'r') as f:
        data = json.load(f)
    try:
        projects = [Project(**item) for item in data]
        for project in projects:
            project_data = project.dict(exclude={"sections"})
            response = requests.post(f"{API_BASE_URL}/projects", headers=get_headers(api_token), json=project_data)
            print(response.status_code, response.json())
            
            for section in project.sections:
                section_data = section.dict(exclude={"tasks"})
                response = requests.post(f"{API_BASE_URL}/sections", headers=get_headers(api_token), json=section_data)
                print(response.status_code, response.json())
                
                for task in section.tasks:
                    task_data = task.dict()
                    response = requests.post(f"{API_BASE_URL}/tasks", headers=get_headers(api_token), json=task_data)
                    print(response.status_code, response.json())
    except ValidationError as e:
        print("Validation failed!")
        print(e.json())

def generate_schema():
    schema = Project.schema_json(indent=2)
    with open('todoist_schema.json', 'w') as f:
        f.write(schema)

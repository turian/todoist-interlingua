from pydantic import BaseModel, Field
from typing import List, Optional


class Label(BaseModel):
    id: str
    name: str = Field(..., max_length=255)
    color: Optional[str] = Field(None, max_length=255)
    order: Optional[int] = None
    is_favorite: Optional[bool] = False


class DueDate(BaseModel):
    string: str
    date: str
    is_recurring: bool
    datetime: Optional[str] = None
    timezone: Optional[str] = None


class Duration(BaseModel):
    amount: int
    unit: str


class Task(BaseModel):
    id: str
    creator_id: str
    created_at: str
    assignee_id: Optional[str] = None
    assigner_id: Optional[str] = None
    comment_count: int
    is_completed: bool
    content: str
    description: Optional[str] = None
    due: Optional[DueDate] = None
    duration: Optional[Duration] = None
    labels: List[str]
    order: int
    priority: int
    project_id: str
    section_id: Optional[str] = None
    parent_id: Optional[str] = None
    url: str
    subtasks: List["Task"] = []  # Added relationship to subtasks


class Section(BaseModel):
    id: str
    project_id: str
    order: int
    name: str = Field(..., max_length=255)
    tasks: List[Task] = []  # Added relationship to tasks


class Project(BaseModel):
    id: str
    name: str = Field(..., max_length=255)
    comment_count: int
    order: int
    color: str
    is_shared: bool
    is_favorite: bool
    parent_id: Optional[str] = None
    is_inbox_project: bool
    is_team_inbox: bool
    view_style: str
    url: str
    sections: List[Section] = []  # Added relationship to sections


class Attachment(BaseModel):
    file_name: str
    file_type: str
    file_url: str
    resource_type: str


class Comment(BaseModel):
    id: str
    task_id: Optional[str] = None
    project_id: Optional[str] = None
    posted_at: str
    content: str
    attachment: Optional[Attachment] = None

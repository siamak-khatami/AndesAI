import datetime
import pytz
import jwt
import pandas as pd
from fastapi import Depends, status, Response, HTTPException, APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy import and_, func
from . import ProjectsRequestSchemas as ReqSchem
from . import ProjectsResponseSchemas as ResSchem
import Routers.Users.UserResponseSchemas as userResSchema
from sqlalchemy.orm import Session
from Database.db import get_db
from . import ProjectsDbModels
from Routers.Users.UserEndpoints import check_user_existence
from General.error_details import ErrorDetails, Msg
from General.response_contents import ResponseMessage as ResMsg
from General.constants import FieldNames as FldNames
from General.constants import EndPoints
from General.SecurityFunctions import auth, Oauth2, token_schemas
from sqlalchemy.exc import IntegrityError
from typing import List, Dict, Optional
from dotenv import load_dotenv, find_dotenv, dotenv_values

load_dotenv()
config = dotenv_values(".env")
user_router = APIRouter(
    prefix=EndPoints.Projects,  # by adding this, there is no need to have prefixed in all endpoint urls
    # In doc root, this tag will be used to show this router's documents
    tags=['Projects']
)


@user_router.get(EndPoints.Projects,
                 status_code=status.HTTP_200_OK,
                 response_model=List[ResSchem.Project],
                 )
def get_projects_list(user: userResSchema.UserExistence = Depends(check_user_existence),
                      db: Session = Depends(get_db)):
    """
    This endpoint returns the list of projects.
    """
    project_query = db.query(ProjectsDbModels.ProjectsTbModel).filter(
        ProjectsDbModels.ProjectsTbModel.user_id == user.user_id)
    projects = project_query.all()
    # Check whether there is user with this email
    if not projects:
        # There is no user with this email
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="No project could be found.")
    return projects


@user_router.post(EndPoints.Projects,
                  status_code=status.HTTP_201_OK,
                  response_model=ResSchem.Project,
                  )
def create_project(new_project: ReqSchem.Project,
                   user: userResSchema.UserExistence = Depends(check_user_existence),
                   db: Session = Depends(get_db)):
    """
    This endpoint receives the information and initiates a project
    """
    try:  # try to add new project
        new_project = ProjectsDbModels.ProjectsTbModel(**new_project.dict())
        db.add(new_project)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Could not init the project")
    db.refresh(new_project)
    return new_project


@user_router.post(EndPoints.ChatLLM,
                  status_code=status.HTTP_201_OK,
                  response_model=ResSchem.ClarifyProject,
                  )
def clarify_project(chat: ReqSchem.ClarifyProject,
                    user: userResSchema.UserExistence = Depends(check_user_existence),
                    db: Session = Depends(get_db)):
    """
    This function receives the query from the user.
    We ask user to give the list of tasks to us and extract the task
    Per each task, we ask user to tell us what resources they need from the resource matrix. If it is not there,
    we ask them to provide information of the resource as well. What is the resource
    """
    # Communicate with the LLM
    return

def get_project_tasks(project_id, session):
    """
    Retrieve tasks for a given project and compute the total duration for each task.

    The total duration is defined as:
        total_duration = waiting_time + max(resource durations)

    If no resources are assigned to a task, resource time defaults to 0.
    """
    # Query all tasks for the project.
    tasks = session.query(ProjectsDbModels.TasksTB).filter(ProjectsDbModels.TasksTB.project_id == project_id).all()

    # Gather the task IDs.
    task_ids = [t.tasks_id for t in tasks]

    # Query the task-resource assignments for these tasks.
    task_resources = session.query(ProjectsDbModels.TaskResourcesTB).filter(ProjectsDbModels.TaskResourcesTB.task_id.in_(task_ids)).all()

    # For each task, compute the maximum resource duration.
    task_resource_max = {}
    for tr in task_resources:
        # Update with the maximum duration found so far.
        if tr.task_id not in task_resource_max or tr.task_resource_duration > task_resource_max[tr.task_id]:
            task_resource_max[tr.task_id] = tr.task_resource_duration

    # Build a dictionary of task information.
    tasks_data = {}
    for task in tasks:
        resource_max = task_resource_max.get(task.tasks_id, 0)
        # Total duration = waiting time + maximum resource duration.
        total_duration = task.task_waiting_times + resource_max
        tasks_data[task.tasks_id] = {
            'name': task.task_name,
            'waiting_time': task.task_waiting_times,
            'resource_time': resource_max,
            'total_duration': total_duration
        }
    return tasks_data


def get_task_dependencies(project_id, session):
    """
    Retrieve the dependency mapping for tasks in the project.

    Returns a dictionary mapping each dependent task_id to a list of the task_ids it depends on.
    """
    # Join TasksDependencies with TasksTB so that only dependencies for tasks in this project are retrieved.
    dependencies = (
        session.query(ProjectsDbModels.TasksDependencies)
        .join(ProjectsDbModels.TasksTB,
              ProjectsDbModels.TasksDependencies.dependent_task_id == ProjectsDbModels.TasksTB.tasks_id)
        .filter(ProjectsDbModels.TasksTB.project_id == project_id)
        .all()
    )

    # Build mapping: dependent task_id -> list of independent task_ids.
    dep_mapping = {}
    for dep in dependencies:
        dep_mapping.setdefault(dep.dependent_task_id, []).append(dep.independent_task_id)
    return dep_mapping

def compute_schedule(tasks_data, dep_mapping):
    """
    Compute the start and finish times for each task.

    Each task's finish time is computed as:
        finish_time = start_time + total_duration
    where total_duration already includes waiting time plus the maximum resource time.

    A task can start only after all tasks it depends on are finished.
    """
    scheduled = {}

    # Count the number of dependencies (incoming edges) for each task.
    indegree = {tid: 0 for tid in tasks_data.keys()}
    for dependent, dependencies in dep_mapping.items():
        indegree[dependent] = len(dependencies)

    # Tasks with no dependencies are ready to be scheduled.
    ready = [tid for tid, count in indegree.items() if count == 0]

    # Process tasks in a simple topological order.
    while ready:
        tid = ready.pop(0)
        task = tasks_data[tid]

        # The task cannot start until all its dependencies are finished.
        if tid in dep_mapping:
            # Only include dependencies that have been scheduled.
            dep_finish_times = [scheduled[dep]['finish'] for dep in dep_mapping[tid] if dep in scheduled]
            max_dep_finish = max(dep_finish_times) if dep_finish_times else 0
        else:
            max_dep_finish = 0

        # The task starts as soon as its dependencies are done.
        start_time = max_dep_finish
        finish_time = start_time + task['total_duration']

        scheduled[tid] = {
            'name': task['name'],
            'start': start_time,
            'finish': finish_time,
            'waiting_time': task['waiting_time'],
            'resource_time': task['resource_time'],
            'total_duration': task['total_duration']
        }

        # “Release” tasks that depend on the current task.
        for other, dependencies in dep_mapping.items():
            if tid in dependencies:
                indegree[other] -= 1
                if indegree[other] == 0:
                    ready.append(other)

    return scheduled


@user_router.post(EndPoints.Gantt,
                  status_code=status.HTTP_201_OK,
                  response_model=List[ResSchem.Schedule],
                  )
def gantt(gantt_info: ReqSchem.GanttInfo,
          user: userResSchema.UserExistence = Depends(check_user_existence),
          db: Session = Depends(get_db)):
    tasks_data = get_project_tasks(gantt_info.project_id, db)
    dep_mapping = get_task_dependencies(gantt_info.project_id, db)

    # Compute schedule (start & finish times).
    scheduled = compute_schedule(tasks_data, dep_mapping)
    return scheduled





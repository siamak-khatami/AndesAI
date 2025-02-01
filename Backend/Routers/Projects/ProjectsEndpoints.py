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
    # Extract Tasks list
    # for each task ask information
    # Extract Task info and Resource Info
    # We can also
    return



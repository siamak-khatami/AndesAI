import json
import os
from fastapi import Depends, status, Response, HTTPException, APIRouter
from dotenv import load_dotenv, find_dotenv, dotenv_values
from sqlalchemy.orm import Session
from . import RequestSchemas as ReqSchemas
from . import ResponseSchemas as ResSchemas
import time
from . import BookDB as BookDB
from General.constants import EndPoints
from Database.db import get_db
load_dotenv()
config = dotenv_values(".env")
docker_router = APIRouter(
    prefix='/docker',  # by adding this, there is no need to have prefixed in all endpoint urls
    # In doc root, this tag will be used to show this router's documents
)


@docker_router.get(EndPoints.Books,
                   status_code=status.HTTP_200_OK)
def get_books(db: Session = Depends(get_db)):
    print("hi")
    books = db.query(BookDB.Books).all()
    return books

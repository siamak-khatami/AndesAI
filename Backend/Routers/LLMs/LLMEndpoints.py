import datetime
import pytz
import jwt
import pandas as pd
from fastapi import Depends, status, Response, HTTPException, APIRouter, Request
from fastapi.responses import JSONResponse

from . import LLMsRequestSchemas as ReqSchem
from . import LLMsResponseSchemas as ResSchem
from sqlalchemy.orm import Session
from Database.db import get_db
from Routers.Users.UserEndpoints import check_user_existence
from General.constants import LLMS
from General.constants import EndPoints
from General.SecurityFunctions import auth, Oauth2, token_schemas
from dotenv import load_dotenv, find_dotenv, dotenv_values
from Routers.Users.UserResponseSchemas import UserExistence
from . LLMFunctions import load_model, build_the_chain, QA

load_dotenv()
config = dotenv_values(".env")
llm_router = APIRouter(
    prefix=EndPoints.LLMs,  # by adding this, there is no need to have prefixed in all endpoint urls
    # In doc root, this tag will be used to show this router's documents
    tags=['LLMs']
)


# General Functions

@llm_router.post(EndPoints.LLMModels,
                 status_code=status.HTTP_201_CREATED,
                 tags=['LLMs']
                 )
def add_llm_model(tour_info: str,
                  db: Session = Depends(get_db),
                  token: token_schemas.AdminTokenDecodedData = Depends(Oauth2.validate_admin_user)
                  ):
    return


@llm_router.get(EndPoints.LLMModels,
                status_code=status.HTTP_200_OK,
                tags=['LLMs']
                )
def get_llm_models(
        db: Session = Depends(get_db),
        token: token_schemas.TokenDecodedData = Depends(Oauth2.validate_user),
        user: UserExistence = Depends(check_user_existence)):
    """
    Is used to subscribe a plan for a user. The product, plan, user should exist and if there is similar plan,
    then that won't be happening.
    This function depends on the Token.
    :return:
    """
    return LLMS.LLMModels


@llm_router.post(EndPoints.ChatLLM,
                status_code=status.HTTP_200_OK,
                tags=['Chats']
                )
def chat_llm(chat_info: ReqSchem.ChatLLM,
             db: Session = Depends(get_db),
             token: token_schemas.TokenDecodedData = Depends(Oauth2.validate_user),
             user: UserExistence = Depends(check_user_existence)):
    """
    Is used to subscribe a plan for a user. The product, plan, user should exist and if there is similar plan,
    then that won't be happening.
    This function depends on the Token.
    :return:
    """
    # These 2 lines including model and the tokenizer is better to be loaded once outside of the function.
    # The model will be cached in the first run and it will be loaded locally the process is already a heavy process.
    # llm_model = 'NousResearch/Llama-2-7b-chat-hf'
    model, tokenizer, stop_criteria = load_model(chat_info.llm_model)
    print("LLM loaded!")
    llm_chain, memory = build_the_chain(model, tokenizer, "", stop_criteria, 0.1)
    qa_result, llm_chain, chat_history = QA(llm_chain, chat_info.prompt, chat_info.chat_history)
    chat_history.append([chat_info.prompt, qa_result])
    return chat_history


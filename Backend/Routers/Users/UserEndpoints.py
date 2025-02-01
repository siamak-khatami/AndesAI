import datetime
import pytz
import jwt
import pandas as pd
from fastapi import Depends, status, Response, HTTPException, APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy import and_, func
from . import UserRequestSchemas as ReqSchem
from . import UserResponseSchemas as ResSchem
from sqlalchemy.orm import Session
from Database.db import get_db
from . import UserDbModels as UserDbModels
from General.error_details import ErrorDetails, Msg
from General.response_contents import ResponseMessage as ResMsg
from General.Functions import registration_email, public_id_encoder, public_id_decoder
from General.Functions import user_reset_password_email
from General.constants import FieldNames as FldNames
from General.constants import EndPoints
from General.SecurityFunctions import auth, Oauth2, token_schemas
from sqlalchemy.exc import IntegrityError
from typing import List, Dict, Optional
from dotenv import load_dotenv, find_dotenv, dotenv_values

load_dotenv()
config = dotenv_values(".env")
user_router = APIRouter(
    prefix=EndPoints.Users,  # by adding this, there is no need to have prefixed in all endpoint urls
    # In doc root, this tag will be used to show this router's documents
    tags=['Users']
)


# General Functions


def generate_token(user):
    access_token = Oauth2.create_access_token(data={'email': user.email,
                                                    'name': user.name})
    res = {
        "access_token": access_token,
        "token_type": 'bearer',
        "user": {
            "user_id": user.user_public_id,  # Public id should be returned.
            "first_name": user.name,
            "last_name": user.family,
            "email": user.email,
            "role": "user"
        },
        "status": 200
    }
    return res  # {'access_token': access_token, 'token_type': 'bearer'}


def check_user_existence(token: token_schemas.TokenDecodedData = Depends(Oauth2.validate_user),
                         db: Session = Depends(get_db)):
    """
    Checks to see whether there is a user with the requested email or not. If yes, then it returns the user model.
    It also returns users subscribed plan and products
    :param token:
    :param db:
    :return:
    """
    user = db.query(UserDbModels.UserTbModel).filter(
        UserDbModels.UserTbModel.email == token.email
    ).first()
    if user:
        # Check its active product-plans and related features.
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=ErrorDetails.User_Not_Found)


@user_router.post(EndPoints.Login,
                  status_code=status.HTTP_200_OK,
                  # response_model=token_schemas.Token
                  )
def login_user(response: Response,
               user_login_info: OAuth2PasswordRequestForm = Depends(),
               db: Session = Depends(get_db)):
    """
    This endpoint gets credentials to login user.
    """
    # Todo: Limit false tries within 10 minuets.
    # instead of using UserLoginInfoRequest, we used fastapi oauth2 method.
    # This method gets login info in the form of username and password. So, fields name, in our case
    # holds email as username.
    # Also, the request should be sent not in a json format, but a form data.
    user_query = db.query(UserDbModels.UserTbModel).filter(
        UserDbModels.UserTbModel.email == user_login_info.username)
    user = user_query.first()
    # Check whether there is user with this email
    if not user:
        # There is no user with this email
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=ErrorDetails.Wrong_Credentials)
    if not auth.verify_password(user_login_info.password, user.password):
        # Password is wrong
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=ErrorDetails.Wrong_Credentials)
    if not user.is_enabled:
        raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED,
                            detail=ErrorDetails.ActivateUser)

    login_info = generate_token(user)
    print(login_info)
    return login_info  # {'access_token': access_token, 'token_type': 'bearer'}


@user_router.post(EndPoints.RegisterUser,
                  status_code=status.HTTP_201_CREATED,
                  )
def register_user(new_user_info: ReqSchem.UserRegistrationInfoRequest,
                  db: Session = Depends(get_db)):
    """
    This function receives credentials for the new user and register it in the system.
    Both email and user id are unique so, it will send an error msg if the email exists in the db.
    """
    new_user = UserDbModels.UserTbModel(**new_user_info.dict())
    try:
        hashed_pass = auth.hash_pass(new_user.password)
        new_user.password = hashed_pass
        db.add(new_user)
        db.commit()
    except Exception as e:  # IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED,
                            detail=ErrorDetails.Email_Exists)
    db.refresh(new_user)
    user_query = db.query(UserDbModels.UserTbModel).filter(
        UserDbModels.UserTbModel.user_id == new_user.user_id)
    user_query.update({FldNames.UserPubID: public_id_encoder(new_user.user_id)},
                      synchronize_session=False)
    db.commit()

    # this token is needed for the validation.
    validation_token = Oauth2.create_access_token_activate_email(data={'email': new_user.email})
    # validation_token = token_schemas.Token(access_token=validation_token,
    #                                        token_type='bearer')
    # registration_email(new_user.name, new_user.email, validation_token)
    return  # login_info


@user_router.post(EndPoints.UserActivationRoot,
                  status_code=status.HTTP_200_OK)
def activate_user(userEmail: token_schemas.ActivationTokenDecode = Depends(Oauth2.activate_user_token),
                  db: Session = Depends(get_db)):
    """
    This end point receives the encoded message and validates the account.
    If it is ok, then 200.
    User should send the token in the header as a bearer code.
    """

    user_query = db.query(UserDbModels.UserTbModel).filter(
        UserDbModels.UserTbModel.email == userEmail
    )
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=ErrorDetails.User_Not_Found)
    else:
        if user.is_enabled:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=ErrorDetails.ActivatedUser)
        else:
            user_query.update({FldNames.IsEnabled: True}, synchronize_session=False)
            db.commit()
    return


@user_router.post(EndPoints.ResendUserActivation,
                  status_code=status.HTTP_200_OK,
                  )
def resend_activation_code(email: ReqSchem.UserResendActivation,
                           db: Session = Depends(get_db)):
    """
    This function receives email and if it exists and not activated it resends the activation code.
    """

    user_query = db.query(UserDbModels.UserTbModel).filter(
        UserDbModels.UserTbModel.email == email.email)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=ErrorDetails.User_Not_Found)
    if user.is_enabled:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=ErrorDetails.ActivatedUser)

    # this token is needed for the validation.
    validation_token = Oauth2.create_access_token_activate_email(data={'email': user.email})
    registration_email(user.name, user.email, validation_token)
    return  # login_info


@user_router.post(EndPoints.CheckLogin)
def check_login(token: token_schemas.TokenDecodedData = Depends(Oauth2.validate_user)):
    """
    This endpoint just validates the token. If token is validated, it returns email and name.
    """

    return token


@user_router.post(EndPoints.UpdatePassToken)
def update_password_request_token_generator(user_email: ReqSchem.UserPassUpdateRequest,
                                            db: Session = Depends(get_db)):
    """
    This generates a limited token for the password resting. It should be passed to the server with
    the update_password()
    :param user_email: email
    :return: 15 minutes valid token
    """
    user = db.query(UserDbModels.UserTbModel).filter(
        UserDbModels.UserTbModel.email == user_email.email).first()
    if not user:
        # There is no user with this email
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=ErrorDetails.Wrong_Email)

    access_token = Oauth2.create_access_token_update_password(data={'email': user.email,
                                                                    'name': user.name})
    token = token_schemas.Token(access_token=access_token,
                                token_type='bearer')
    return token  # {'access_token': access_token, 'token_type': 'bearer'}


@user_router.post(EndPoints.UpdatePass,
                  status_code=status.HTTP_202_ACCEPTED)
def update_password(new_password: ReqSchem.UserNewPassWord,
                    db: Session = Depends(get_db),
                    user: ResSchem.UserExistence = Depends(check_user_existence),
                    token: token_schemas.TokenDecodedData = Depends(Oauth2.validate_password_reset_user)):
    """
    This function
    :param new_password: New password schema, Front end should check the password repeater
    :param token: A request to /users/update-password-token should be sent to get a 15-min token.
    :return: Json
    """
    user_query = db.query(UserDbModels.UserTbModel).filter(UserDbModels.UserTbModel.email == token.email)
    user = user_query.first()
    if not user:
        # There is no user with this email
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=ErrorDetails.User_Not_Found)
    else:
        new_password.password = auth.hash_pass(new_password.password)
        user_query.update({FldNames.Password: new_password.password},
                          synchronize_session=False)
        db.commit()
        # db.refresh()
        return


@user_router.post(EndPoints.ResetPass,
                  status_code=status.HTTP_200_OK)
def reset_password(email: ReqSchem.ResetPass,
                   db: Session = Depends(get_db)):
    """
    This function
    :param email: To check the user
    This function receives a user email, if there is an email, it generates a token which contains the password
    information This token should be sent to the user with the password setting page, in that page, if the token is
    valid, user can see the password setup and set up a new password.
    :return: Json
    """
    # Check the user
    user_query = db.query(UserDbModels.UserTbModel).filter(
        UserDbModels.UserTbModel.email == email.email)
    user = user_query.first()
    if not user:
        # There is no user with this email
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=ErrorDetails.User_Not_Found)
    else:
        # Generate the reset token and send it to the user with the link to the password update page
        # Generate the token
        access_token = Oauth2.create_access_token_update_password(data={'email': user.email,
                                                                        'name': user.name})
        user_reset_password_email(client_name=user.name,
                                  client_email=user.email,
                                  validation_token=access_token)
        return ""


@user_router.patch(EndPoints.ResetPass,
                   status_code=status.HTTP_200_OK)
def reset_password(new_password: ReqSchem.UserNewPassWord,
                   db: Session = Depends(get_db),
                   token: token_schemas.TokenDecodedData = Depends(Oauth2.validate_password_reset_user)):
    """
    This function
    :param new_password: New password schema, Front end should check the password repeater
    :param token: A request to /users/update-password-token should be sent to get a 15-min token.
    :return: Json
    """
    user_query = db.query(UserDbModels.UserTbModel).filter(
        UserDbModels.UserTbModel.email == token.email)
    user = user_query.first()
    if not user:
        # There is no user with this email
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=ErrorDetails.User_Not_Found)
    else:
        new_password.password = auth.hash_pass(new_password.password)
        user_query.update({FldNames.Password: new_password.password},
                          synchronize_session=False)
        db.commit()
        # db.refresh()
        return


@user_router.post(EndPoints.UpdateUser)
def update_user(db: Session = Depends(get_db),
                token: token_schemas.TokenDecodedData = Depends(Oauth2.validate_user)):
    # TODO: Update User
    return


@user_router.post(EndPoints.DeleteUser,
                  status_code=status.HTTP_200_OK, )
def delete_user(db: Session = Depends(get_db),
                token: token_schemas.TokenDecodedData = Depends(Oauth2.validate_user)):
    # TODO: delete the user
    user_query = db.query(UserDbModels.UserTbModel).filter(
        UserDbModels.UserTbModel.email == token.email)

    user = user_query.first()
    if not user:
        # There is no user with this email
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=ErrorDetails.User_Not_Found)
    else:
        user_query.delete(synchronize_session=False)
        db.commit()

# ======================= User Tour Endpoints ======================= #


@user_router.post(EndPoints.UserTours,
                  status_code=status.HTTP_201_CREATED,
                  tags=['tours']
                  )
def add_tour(tour_info: ReqSchem.TourInfo,
             db: Session = Depends(get_db),
             token: token_schemas.AdminTokenDecodedData = Depends(Oauth2.validate_admin_user)
             ):
    """
    Is used to subscribe a plan for a user. The product, plan, user should exist and if there is similar plan,
    then that won't be happening.
    This function depends on the Token.
    :return:
    """
    new_tour = UserDbModels.UserTours(**tour_info.dict())
    try:
        db.add(new_tour)
        db.commit()
    except Exception as e:  # IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=ErrorDetails.Tour_Exists)
    db.refresh(new_tour)
    return new_tour


@user_router.get(EndPoints.UserTours,
                 status_code=status.HTTP_200_OK,
                 tags=['tours']
                 )
def disable_user_tour(
        tour_id: int = None,
        db: Session = Depends(get_db),
        token: token_schemas.TokenDecodedData = Depends(Oauth2.validate_user),
        user: ResSchem.UserExistence = Depends(check_user_existence),
):
    """
    Is used to subscribe a plan for a user. The product, plan, user should exist and if there is similar plan,
    then that won't be happening.
    This function depends on the Token.
    :return:
    """
    #
    if tour_id:
        tour_query = db.query(UserDbModels.UserTourVisibility).filter(
            and_(
                UserDbModels.UserTourVisibility.user_id == user.user_id,
                UserDbModels.UserTourVisibility.tour_id == tour_id
            )
        )
        tour = tour_query.first()
        if tour:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=ErrorDetails.TourAlreadyDisabled)
        else:
            new_tour = UserDbModels.UserTourVisibility(tour_id=tour_id,
                                                       user_id=user.user_id)
            try:
                db.add(new_tour)
                db.commit()
            except Exception as e:  # IntegrityError:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail=ErrorDetails.CouldNotDisableTour)
            db.refresh(new_tour)
            return
    else:
        tours = db.query(UserDbModels.UserTourVisibility).filter(
            UserDbModels.UserTourVisibility.user_id == user.user_id
        ).all()
        tour_ids = [t.tour_id for t in tours]
        return tour_ids

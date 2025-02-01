from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import EmailStr
from sqlalchemy.orm import Session
from . import token_schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from General.error_details import ErrorDetails
from General.constants import Consts, EndPoints
from Database.db import get_db
from dotenv import load_dotenv, dotenv_values

load_dotenv()
config = dotenv_values(".env")


def create_access_token(data: dict):
    """
    This function creates access tokens for the server communication.
    """
    data_copy = data.copy()
    expire_time = datetime.utcnow() + timedelta(minutes=Consts.UserActivationTime)
    data_copy.update({'exp': expire_time})
    token = jwt.encode(data_copy, config["SECRET_KEY"], algorithm=config["ALGORITHM"])
    return token


def create_access_token_update_password(data: dict):
    """
    This function creates access tokens for the server communication.
    """
    data_copy = data.copy()
    expire_time = datetime.utcnow() + timedelta(minutes=int(Consts.ResetPassTokenTime))
    data_copy.update({'exp': expire_time})
    token = jwt.encode(data_copy, config["SECRET_KEY"], algorithm=config["ALGORITHM"])
    return token


def create_access_token_activate_email(data: dict):
    """
    This function creates access tokens for account activation.
    """
    data_copy = data.copy()
    expire_time = datetime.utcnow() + timedelta(minutes=Consts.UserEmailActivation)
    data_copy.update({'exp': expire_time})
    token = jwt.encode(data_copy, config["SECRET_KEY"], algorithm=config["ALGORITHM"])
    return token


"""
OAuth2PasswordBearer takes the token, and validates it. 
If token is validated, it returns the token again, 
Else, it returns the Authentication error.
"""
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=EndPoints.Users+EndPoints.Login)  # This login is the login we used for our users
# When the validate_user function receives the token (str) in Authenticate field, it sends the token to
# the OAth2PasswordBearer function. This function has the access to the function in which can do the login operation.
# So, it checks the input access token with the function again, and if it is ok, it returns the same token.


def validate_user(token: str = Depends(oauth2_scheme),
                  db: Session = Depends(get_db)):
    """
    This function receives the token from the user as string.
    The field which contains the token in the request is "Authorization" in headers.
    the content of the field is "Bearer token_string"
    Then it passes the token to the oauth2_scheme which does the validation using the tokenUrl setup.
    If the token is valid, it returns the token again, else, it raises an authentication error.
    returns:
    Token
    """
    try:

        payload = jwt.decode(token, config["SECRET_KEY"], algorithms=[config["ALGORITHM"]])
        email: EmailStr = payload.get('email')  # In request schemas, we have sent email as data into the token.
        name: str = payload.get('name')

        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=ErrorDetails.Wrong_Credentials,
                                headers={'WWW-Authenticate': 'Bearer'})
        token_data = token_schemas.TokenDecodedData(email=email, name=name)
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=ErrorDetails.Wrong_Credentials,
                            headers={'WWW-Authenticate': 'Bearer'})
    # TODO(1): return user object instead of token extracted object.
    # Instead of token data, we can run a query, and check whether user exists or not,
    # and then return it
    return token_data



oauth2_user_activation = OAuth2PasswordBearer(tokenUrl=EndPoints.UserActivationRoot)
# When the validate_user function receives the token (str) in Authenticate field, it sends the token to
# the OAth2PasswordBearer function. This function has the access to the function in which can do the login operation.
# So, it checks the input access token with the function again, and if it is ok, it returns the same token.


def activate_user_token(token: str = Depends(oauth2_user_activation),
                        db: Session = Depends(get_db)):
    """
    This function receives the token from the user as string.
    The field which contains the token in the request is "Authorization" in headers.
    the content of the field is "Bearer token_string"
    Then it passes the token to the oauth2_scheme which does the validation using the tokenUrl setup.
    If the token is valid, it returns the token again, else, it raises an authentication error.
    returns:
    Token
    """
    try:
        payload = jwt.decode(token, config["SECRET_KEY"], algorithms=[config["ALGORITHM"]])
        mail: EmailStr = payload.get('email')  # In request schemas, we have sent email as data into the token.
        if not mail:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=ErrorDetails.InValid_Token,
                                headers={'WWW-Authenticate': 'Bearer'})
    except JWTError as e:
        err = ErrorDetails.CustomError
        err["msg"] = str(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=err,
                            headers={'WWW-Authenticate': 'Bearer'})
    return mail


oauth2_scheme_admin_login = OAuth2PasswordBearer(tokenUrl='login-admin-user')


def validate_admin_user(token: str = Depends(oauth2_scheme_admin_login),
                        db: Session = Depends(get_db)):
    """
    This function receives the token from the user as string.
    The field which contains the token in the request is "Authorization" in headers.
    the content of the field is "Bearer token_string"
    Then it passes the token to the oauth2_scheme which does the validation using the tokenUrl setup.
    If the token is valid, it returns the token again, else, it raises an authentication error.
    """
    try:
        payload = jwt.decode(token, config["SECRET_KEY"], algorithms=[config["ALGORITHM"]])
        email: EmailStr = payload.get('email')  # In request schemas, we have sent email as data into the token.
        first_name: str = payload.get('first_name')
        last_name: str = payload.get('last_name')
        roles: str = payload.get('roles')
        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=ErrorDetails.Wrong_Credentials,
                                headers={'WWW-Authenticate': 'Bearer'})
        token_data = token_schemas.AdminTokenDecodedData(email=email,
                                                         first_name=first_name,
                                                         last_name=last_name,
                                                         roles=roles)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=ErrorDetails.Wrong_Credentials,
                            headers={'WWW-Authenticate': 'Bearer'})
    # TODO(1): return user object instead of token extracted object.
    # Instead of token data, we can run a query, and check whether user exists or not,
    # and then return it
    return token_data


oauth2_scheme_password_reset = OAuth2PasswordBearer(tokenUrl='update_password')
def validate_password_reset_user(token: str = Depends(oauth2_scheme_password_reset),
                                 db: Session = Depends(get_db)):
    """
    This function receives the token from the user as string.
    The field which contains the token in the request is "Authorization" in headers.
    the content of the field is "Bearer token_string"
    Then it passes the token to the oauth2_scheme which does the validation using the tokenUrl setup.
    If the token is valid, it returns the token again, else, it raises an authentication error.
    """
    try:
        payload = jwt.decode(token, config["SECRET_KEY"], algorithms=[config["ALGORITHM"]])
        email: EmailStr = payload.get('email')  # In request schemas, we have sent email as data into the token.
        name: str = payload.get('name')
        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=ErrorDetails.Wrong_Credentials,
                                headers={'WWW-Authenticate': 'Bearer'})
        token_data = token_schemas.TokenDecodedData(email=email, name=name)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=ErrorDetails.Wrong_Credentials,
                            headers={'WWW-Authenticate': 'Bearer'})
    return token_data

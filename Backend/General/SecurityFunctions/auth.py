from passlib.context import CryptContext


def hash_pass(password: str):
    """
    This function hashes the input password to store in the database
    """
    password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    """
    This function gets plain pass and hashed pass and validates it.
    """
    password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    return password_context.verify(plain_password, hashed_password)

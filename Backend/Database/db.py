from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv, find_dotenv, dotenv_values
load_dotenv()
config = dotenv_values(".env")
SQLALCHEMY_DATABASE_URL = 'postgresql://{username}:{password}@{hostname}:{port}/{db_name}'.format(
    username=config["DATABASE_USERNAME"],
    password=config["DATABASE_PASSWORD"],
    hostname=config["DATABASE_HOSTNAME"],
    port=config["DATABASE_PORT"],
    db_name=config["DATABASE_NAME"]
)
Db_engine = create_engine(SQLALCHEMY_DATABASE_URL)
Db_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Db_engine)
Db_Base = declarative_base()


# Dependency
def get_db():
    db = Db_SessionLocal()
    try:
        yield db
    finally:
        db.close()
